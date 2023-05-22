import os
import requests
import time
import subprocess
import datetime
import concurrent.futures

def check_url(i):
    base_url = "https://live-edge{}.bcvcdn.com/hls/stream_{channel-name}/playlist.m3u8"
    url = base_url.format(i)
    try:
        response = requests.get(url)
        if response.status_code == 200:
            return url
    except requests.exceptions.RequestException as err:
        print(f"Error: Could not connect to {url}. Details: {err}")
    return None

def get_url_of_day():
    with concurrent.futures.ThreadPoolExecutor(max_workers=100) as executor:
        future_to_url = {executor.submit(check_url, i): i for i in range(100)}
        for future in concurrent.futures.as_completed(future_to_url):
            url = future.result()
            if url is not None:
                print(f"Live URL of the day: {url}")
                return url

    print("No live URL found today.")
    return None

def is_stream_live(url):
    try:
        response = requests.get(url, stream=True)
        return response.status_code == 200
    except requests.exceptions.RequestException as e:
        print(f'Exception occurred: {e}')
        return False

def start_recording(url, output_file):
    # run ffmpeg command here
    # it should block until the stream ends
    subprocess.run(['ffmpeg', '-i', url, '-c', 'copy', output_file])

def get_next_filename():
    index = 1
    while os.path.exists(f'output{index}.mp4'):
        index += 1
    return f'output{index}.mp4'

def monitor_stream():
    start_time = datetime.datetime.now()
    url = None

    # Try to fetch the URL for up to 120 minutes
    while datetime.datetime.now() - start_time < datetime.timedelta(minutes=120):
        url = get_url_of_day()  # try to get the initial URL
        if url is not None:
            break
        print(f'{datetime.datetime.now()}: No live URL found. Retrying in 1 minute.')
        time.sleep(60)  # wait for 1 minute before trying again

    if url is None:
        print(f'{datetime.datetime.now()}: No live URL found within 120 minutes. Ending program.')
        return

    time_stream_was_last_live = datetime.datetime.now()

    while True:
        if is_stream_live(url):
            print(f'{datetime.datetime.now()}: Stream is live. Starting recording.')
            output_file = get_next_filename()
            start_recording(url, output_file)
            print(f'{datetime.datetime.now()}: Stream ended. Waiting for it to become live again.')
            time_stream_was_last_live = datetime.datetime.now()
        else:
            print(f'{datetime.datetime.now()}: Stream is not live. Waiting before checking again.')
            if (datetime.datetime.now() - time_stream_was_last_live).total_seconds() > 2700:  # 45 minutes
                print("Stream has been offline for more than 30 minutes. Ending program.")
                break

        time.sleep(10)  # wait for 10 seconds before checking again

monitor_stream()

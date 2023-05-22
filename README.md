# LiveRecording

A simple program to Check & Record the Live stream on BCs.

You should install python3(including requests module) and ffmpeg to use this.

You can replace {channel-name} with the channel you interest in.

When you run the program, it will first check the channel whether on Live or not. In this step, the program is to find the live stream url, if it find an active url, it means the model is on live at this moment, and the recording will start.It will continue to check in next 2 hours if channel is not on live, you can adjust this attribute value.
If model has temporaily leave for a while, the program will continue to check every 10 seconds whether the model has come back to live, if come back, the recording will re-start; If the model has left over 45 minutes, we suppose it reach to the end of the daily live, and the program will end. You can also adjust the value of this attribute.

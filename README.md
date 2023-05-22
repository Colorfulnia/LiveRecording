# LiveRecording
a program to recording the living on one website
A simple program to Check & Record the Live on BCs.

You should install python3(including requests module) and ffmpeg to use this.

You can change "Swetty-Pie" with the model you want to record.

When you run the program, it will first check the model whether on Live or not, in this step, the program is find the live stream url, if it find the active url, it means the model is on live at this moment, and the recording will start.It will continue to check in next 2 hours if model not on live, you can modify this attribute value.
if model has temporaily leave for a while, the program will continue to check every 10 seconds whether the model has come back to live, if come back, the recording will re-start. if the model has left over 45 minutes, we suppose it reach to the end of the daily live, and the program will end. You can also adjust the value of this attribute.

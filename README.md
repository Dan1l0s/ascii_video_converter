# ASCII video converter

## About this project

This project allows you to convert any mp4 video to ascii video and play it in terminal.

## Usage example

<p align="center">
  <img src="https://github.com/Dan1l0s/ascii_video_converter/assets/47472342/fbbdaa8d-f860-4c44-a9b1-7546b04b8c2d" alt="Usage example"/>
</p>

## How to install and launch

1. Download or clone this repository
2. Rename your target video file to `video.mp4`
3. Proceed to `res/video.mp4` and replace existing file with your target video
4. Execute [runner.bat](runner.bat) or [runner.sh](runner.sh) on Windows or Linux machine respectively
5. (Optional) Change the playback mode from preprocessing to realtime if needed in [script.py](script.py)
6. (Optional) If the result video looks weird you can modify symbols in `ascii_chars` variable in [script.py](script.py) to create a different look
7. (Optional) If an error `_curses.error: addwstr() returned ERR` occurs then adjust `ascii_width` and `ascii_height` variables in [script.py](script.py) and the window size in your `runner` file
8. (Optional) Use `save_ascii_frames_to_file` function to save your generated frames to a text file
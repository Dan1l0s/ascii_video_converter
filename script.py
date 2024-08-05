import cv2
import numpy as np
import curses
import threading
import time

# Choose the mode of playback: realtime or preprocessing (realtime mode may have different fps compared to original video => be careful)
MODE = "PREPROCESSING"  # "REALTIME" or "PREPROCESSING"

# Modify this string to change the display of colors
# The hue changes from left to right, where the left is black and the right is white
ascii_chars = "N@#W$9876543210?!abc;:+=-,._              "

# Modify these values if you get "_curses.error: addwstr() returned ERR" error
# If these parameters are changed, check if there's enough space in the terminal to display the frames
ascii_width = 200
ascii_height = 75

video_path = "res/video.mp4" # The path to the video file
fps = 30 # Auto-lookup parameter

# Generate ascii frame
def frame_to_ascii(frame, width: int, height: int) -> str:
    frame = cv2.resize(frame, (width, height))
    gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    normalized_frame = np.interp(gray_frame, (0, 255), (0, len(ascii_chars) - 1))
    ascii_frame = ""
    for row in normalized_frame:
        for pixel_value in row:
            ascii_frame += ascii_chars[int(pixel_value)]
        ascii_frame += "\n"
    return ascii_frame


# Realtime frames-processing function (running in thread)
def video_processing_realtime(video_path: str, width: int, height: int, frame_ready_event: threading.Event, frame_callback) -> None:
    cap = cv2.VideoCapture(video_path)
    fps = int(cap.get(cv2.CAP_PROP_FPS))
    while True:
        ret, frame = cap.read()
        if not ret:
            break

        ascii_frame = frame_to_ascii(frame, width, height)
        frame_callback(ascii_frame)
        frame_ready_event.set()
        time.sleep(1 / fps)

    cap.release()

# Preprocessing frames-processing function
def video_processing_preprocessing(video_path: str, width: int, height: int):
    cap = cv2.VideoCapture(video_path)
    fps = int(cap.get(cv2.CAP_PROP_FPS))

    ascii_frames = []

    while True:
        ret, frame = cap.read()
        if not ret:
            break
        
        ascii_frame = frame_to_ascii(frame, width, height)
        ascii_frames.append(ascii_frame)

    cap.release()
    return ascii_frames, fps


# Display generated ascii frames for realtime mode
def play_ascii_frames_realtime(stdscr, frame_ready_event: threading.Event, frame_callback) -> None:
    while True:
        frame_ready_event.wait()
        frame_ready_event.clear()

        frame = frame_callback()
        stdscr.clear()
        stdscr.addstr(0, 0, frame)
        stdscr.refresh()

# Display generated ascii frames for preprocessing mode
def play_ascii_frames_preprocessing(stdscr, ascii_frames):
    global fps
    for frame in ascii_frames:
        stdscr.clear()
        stdscr.addstr(0, 0, frame)
        stdscr.refresh()
        time.sleep(1 / fps)

# Save generated frames to a file
def save_ascii_frames_to_file(ascii_frames, output_file):
    with open(output_file, "w") as file:
        for frame in ascii_frames:
            file.write(frame)
            file.write("\n\n")  # Add a newline between frames


# Main function
def main():
    global video_path
    global ascii_width
    global ascii_height
    global fps

    if MODE == "PREPROCESSING":
        print("Processing...")

        ascii_frames, fps = video_processing_preprocessing(video_path, ascii_width, ascii_height)

        curses.wrapper(play_ascii_frames_preprocessing, ascii_frames)

    else:
        frame_ready_event = threading.Event()

        def frame_callback():
            if not hasattr(frame_callback, 'frame'):
                return ''
            return frame_callback.frame

        def update_frame(frame) -> None:
            setattr(frame_callback, 'frame', frame)

        video_thread = threading.Thread(
            target=video_processing_realtime,
            args=(video_path, ascii_width, ascii_height, frame_ready_event, update_frame)
        )
        video_thread.start()
        curses.wrapper(play_ascii_frames_realtime, frame_ready_event, frame_callback)
        video_thread.join()


if __name__ == "__main__":
    main()
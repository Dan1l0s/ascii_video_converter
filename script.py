import cv2
import numpy as np
import curses
import threading
import time

# Modify this string to change the display of colors
# The hue changes from left to right, where the left is black and the right is white
ascii_chars = "N@#W$9876543210?!abc;:+=-,._              "


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
def video_processor(video_path: str, width: int, height: int, frame_ready_event: threading.Event, frame_callback):
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


# Display generated ascii frames
def play_ascii_frames(stdscr, frame_ready_event: threading.Event, frame_callback) -> None:
    while True:
        frame_ready_event.wait()
        frame_ready_event.clear()

        frame = frame_callback()
        stdscr.clear()
        stdscr.addstr(0, 0, frame)
        stdscr.refresh()


def main():
    video_path = "res/video.mp4"

    # If these parameters are changed, check if there's enough space in the terminal to display the frames
    ascii_width = 200
    ascii_height = 75

    frame_ready_event = threading.Event()

    def frame_callback():
        if not hasattr(frame_callback, 'frame'):
            return ''
        return frame_callback.frame

    def update_frame(frame):
        setattr(frame_callback, 'frame', frame)

    video_thread = threading.Thread(
        target=video_processor,
        args=(video_path, ascii_width, ascii_height, frame_ready_event, update_frame)
    )
    video_thread.start()

    curses.wrapper(play_ascii_frames, frame_ready_event, frame_callback)

    video_thread.join()


if __name__ == "__main__":
    main()

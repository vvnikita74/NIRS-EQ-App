import tkinter as tk
import threading
import pyaudio
import wave
import time
import filters
from tkinter import filedialog
from scipy import signal 
import numpy as np

# Define the main window
root = tk.Tk()
root.title("WAV Player")
root.geometry("800x600")

# Define variables to store the file path and playback status, default audio_format and list of all pyAudio formats
file_path = ""
playing = False
buf_size = 2048

filter_on = False

file_label = tk.Label(root, text='Selected file: None', font=("Bahnschrift", 16))
file_label.place(relx=0.5, rely=0.1, anchor="center", y=10)

buf_label = tk.Label(root, text="Buffer size: " + str(buf_size), font=("Bahnschrift", 16))
buf_label.place(relx=0.5, rely=0.5, anchor="center")


def update_buf_size(val):
    global buf_size
    buf_label.configure(text="Buffer size: "+str(val))
    buf_size = int(val)


scale = tk.Scale(root, from_=64, to=2048, orient=tk.HORIZONTAL)
scale.set(buf_size)
scale.bind("<ButtonRelease-1>", lambda event: update_buf_size(scale.get()))
scale.place(relx = 0.5, rely=0.5, anchor="center", y=40)

def get_file_name(path):
    # Find the index of the last slash in the path
    last_slash = path.rfind("/")
    # Find the index of the last dot in the path
    last_dot = path.rfind(".")
    # Extract the file name substring from the path
    file_name = path[last_slash+1:last_dot]
    return file_name

def select_file():
    global file_path
    file_path = filedialog.askopenfilename(title="Select WAV File", filetypes=(("WAV files", "*.wav"),))
    if file_path:
        file_label.configure(text="Selected File: " + get_file_name(file_path))
        print("Selected file:", file_path)


# Define function for playing/stopping the WAV file
def play_stop():
    global playing
    if not playing:
        playing = True
        t = threading.Thread(target=play_audio)
        t.start()
        play_btn.configure(text="Stop")
    else:
        play_btn.configure(text="Play")
        playing = False


def play_audio():
    wf = wave.open(file_path, 'rb')
    p = pyaudio.PyAudio()
    
    def callback(in_data, frame_count, time_info, status):
        if filter_on:
            data = np.frombuffer(wf.readframes(frame_count), dtype=np.int16)
            # БИХ
            data = filters.cheby_filter_lowpass(data)
            # КИХ
        else:
            data = wf.readframes(frame_count)
        if playing:
            return data, pyaudio.paContinue
        else:
            return data, pyaudio.paComplete

    stream = p.open(format=p.get_format_from_width(wf.getsampwidth()),
                    channels=wf.getnchannels(),
                    rate=wf.getframerate(),
                    output=True,
                    stream_callback=callback,
                    frames_per_buffer=buf_size*24)
    
    while stream.is_active():
        time.sleep(0.1)


# Define a function for filter button
def toggle_filter():
    global filter_on
    filter_on = not filter_on
    if filter_on:
        filter_btn.configure(text="Filter: ON")
    else:
        filter_btn.configure(text="Filter: OFF")


# Define the file selection button
file_btn = tk.Button(root, text="Select File", command=select_file, font=("Bahnschrift", 16))
file_btn.place(relx=0.5, rely=0.2, anchor="center")

# Define the play/stop button
play_btn = tk.Button(root, text="Play", command=play_stop, font=("Bahnschrift", 16))
play_btn.place(relx=0.5, rely=0.8, anchor="center")

# Define the filter_on button
filter_btn = tk.Button(root, text="Filter: OFF", command=toggle_filter, font=("Bahnschrift", 16))
filter_btn.place(relx=0.5, rely=0.35, anchor="center")

# Run the main loop
root.mainloop()
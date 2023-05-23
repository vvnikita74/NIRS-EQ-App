import tkinter as tk
import threading
import pyaudio
import wave
import time
from tkinter import filedialog
from functions import *

# Define the main window
root = tk.Tk()
root.title("WAV Player")
root.geometry("800x600")

# Define variables to store the file path and playback status, default audio_format and list of all pyAudio formats
file_path = ""
playing = False
buf_size = 1024

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
        data = wf.readframes(frame_count)
        if frame_count < 128:
            data = data[:-1] + bytes(1)
        if playing:
            return data, pyaudio.paContinue
        else:
            return data, pyaudio.paComplete

    stream = p.open(format=p.get_format_from_width(wf.getsampwidth()),
                    channels=wf.getnchannels(),
                    rate=wf.getframerate(),
                    output=True,
                    stream_callback=callback,
                    frames_per_buffer=buf_size)
    
    while stream.is_active():
        time.sleep(0.1)


# Define the file selection button
file_btn = tk.Button(root, text="Select File", command=select_file, font=("Bahnschrift", 16))
file_btn.place(relx=0.5, rely=0.2, anchor="center")

# Define the play/stop button
play_btn = tk.Button(root, text="Play", command=play_stop, font=("Bahnschrift", 16))
play_btn.place(relx=0.5, rely=0.8, anchor="center")

# Run the main loop
root.mainloop()

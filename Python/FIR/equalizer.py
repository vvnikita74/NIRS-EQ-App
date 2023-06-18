from filters import apply_equalizer
from filters import apply_delay
from filters import apply_distortion
from tkinter import filedialog
from scipy import signal
import tkinter as tk
import numpy as np
import threading
import pyaudio
import wave
import time

# Define the main window
root = tk.Tk()
root.title("Equalizer")
root.geometry("1366x600")

# Define variables to store the file path and playback/filter status, default buffer size
file_path = ""
playing = False
buf_size = 2048
filter_on = False
delay_on = False
distortion_on = False

# Number of bands
coefficients = [1 for i in range(8)]

# Frequency list
frequency = [100, 300, 700, 1500, 3100, 6300, 12700]

# Creating variables to store slider values
slider_vars = [tk.DoubleVar() for _ in range(len(coefficients))]

# Creating variables to store slider labels
slider_label = [i for i in range(len(coefficients))]
for i in range(len(coefficients)):
    if i == 0:
        slider_label[i] = f"0 - {frequency[i]}"
    else:
        if i == len(coefficients) - 1:
            slider_label[i] = f"{frequency[i-1]} - 20000"
        else:
            slider_label[i] = f"{frequency[i-1]} - {frequency[i]}"


file_label = tk.Label(root, text='', font=("Bahnschrift", 16))
file_label.place(relx=0.15, rely=0.1, anchor="center", y=10)

buf_label = tk.Label(root, text="Buffer size: " + str(buf_size), font=("Bahnschrift", 16))
buf_label.place(relx=0.1, rely=0.5, anchor="center")

scale = tk.Scale(root, from_=64, to=2048, orient=tk.HORIZONTAL)
scale.set(buf_size)
scale.bind("<ButtonRelease-1>", lambda event: update_buf_size(scale.get()))
scale.place(relx = 0.1, rely=0.5, anchor="center", y=40)


def update_coefficients(value):
    for i in range(len(coefficients)):
        coefficients[i] = 1.0 + slider_vars[i].get()


# Creating and placing sliders and its labels
for i in range(len(coefficients)):
    label = tk.Label(root, text=f"{slider_label[i]}", font=("Bahnschrift", 12))
    label.place(relx=0.21+i/10, rely=0.9, anchor="center")
    slider = tk.Scale(root, from_=0, to=-1, resolution=0.1, orient=tk.VERTICAL, variable=slider_vars[i], command=update_coefficients, length=400)
    slider.set(10 - coefficients[i] * 10)  # Setting the initial value
    slider.place(relx=0.2+i/10, rely=0.5, anchor="center")


def update_buf_size(val):
    global buf_size
    buf_label.configure(text="Buffer size: "+str(val))
    buf_size = int(val)


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
    sample_rate = wf.getframerate()
    def callback(in_data, frame_count, time_info, status):
        data = np.frombuffer(wf.readframes(frame_count), dtype=np.int16)
        
        if filter_on:
            data = apply_equalizer(coefficients, data, 5001, frequency, 44100)
        
        if delay_on:
            data = data + apply_delay(data, 0.2)[:len(data)]

        if distortion_on:
            data = apply_distortion(data, 0.1)

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

# Define a function for delay button
def toggle_delay():
    global delay_on
    delay_on = not delay_on
    if delay_on:
        delay_btn.configure(text="Delay: ON")
    else:
        delay_btn.configure(text="Delay: OFF")

# Define a function for distortion button
def toggle_distortion():
    global distortion_on
    distortion_on = not distortion_on
    if distortion_on:
        distortion_btn.configure(text="Distortion: ON")
    else:
        distortion_btn.configure(text="Distortion: OFF")


# Define the file selection button
file_btn = tk.Button(root, text="Select File", command=select_file, font=("Bahnschrift", 16))
file_btn.place(relx=0.1, rely=0.2, anchor="center")

# Define the play/stop button
play_btn = tk.Button(root, text="Play", command=play_stop, font=("Bahnschrift", 16))
play_btn.place(relx=0.1, rely=0.8, anchor="center")

# Define the filter_on button
filter_btn = tk.Button(root, text="Filter: OFF", command=toggle_filter, font=("Bahnschrift", 10))
filter_btn.place(relx=0.1, rely=0.3, anchor="center")

# Define the filter_on button
delay_btn = tk.Button(root, text="Delay: OFF", command=toggle_delay, font=("Bahnschrift", 10))
delay_btn.place(relx=0.1, rely=0.35, anchor="center")

# Define the filter_on button
distortion_btn = tk.Button(root, text="Distortion: OFF", command=toggle_distortion, font=("Bahnschrift", 10))
distortion_btn.place(relx=0.1, rely=0.4, anchor="center")


# Run the main loop
root.mainloop()
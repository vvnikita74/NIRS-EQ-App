from tkinter import filedialog
from scipy import signal
import tkinter as tk
import numpy as np
import threading
import filters
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

file_label = tk.Label(root, text='Selected file: None', font=("Bahnschrift", 16))
file_label.place(relx=0.1, rely=0.1, anchor="center", y=10)

buf_label = tk.Label(root, text="Buffer size: " + str(buf_size), font=("Bahnschrift", 16))
buf_label.place(relx=0.1, rely=0.5, anchor="center")

scale = tk.Scale(root, from_=64, to=2048, orient=tk.HORIZONTAL)
scale.set(buf_size)
scale.bind("<ButtonRelease-1>", lambda event: update_buf_size(scale.get()))
scale.place(relx = 0.1, rely=0.5, anchor="center", y=40)

coefficients = [1 for i in range(8)]


def update_coefficients(value):
    for i in range(8):
        coefficients[i] = 1.0 - slider_vars[i].get()

# Создание переменных для хранения значений слайдеров
slider_vars = [tk.DoubleVar() for _ in range(8)]

# Создание и размещение слайдеров
for i in range(8):
    slider = tk.Scale(root, from_=0, to=1, resolution=0.1, orient=tk.VERTICAL, variable=slider_vars[i], command=update_coefficients, length=400)
    slider.set(10 - coefficients[i] * 10)  # Установка начального значения слайдера
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


def apply_equalizer(coefficients, data):
    filtered_data = np.zeros_like(data, dtype=np.int16)

    b = signal.firwin(5001, 100, pass_zero='lowpass', fs=44100)
    filtered_data = np.float32((filtered_data + coefficients[0] * signal.convolve(data, b, mode='same')))

    b = signal.firwin(5001, [100, 300], pass_zero='bandpass', fs=44100)
    filtered_data = np.float32((filtered_data + coefficients[1] * signal.convolve(data, b, mode='same')))

    b = signal.firwin(5001, [300, 700], pass_zero='bandpass', fs=44100)
    filtered_data = np.float32((filtered_data + coefficients[2] * signal.convolve(data, b, mode='same')))

    b = signal.firwin(5001, [700, 1500], pass_zero='bandpass', fs=44100)
    filtered_data = np.float32((filtered_data + coefficients[3] * signal.convolve(data, b, mode='same')))
    
    b = signal.firwin(5001, [1500, 3100], pass_zero='bandpass', fs=44100)
    filtered_data = np.float32((filtered_data + coefficients[4] * signal.convolve(data, b, mode='same')))
    
    b = signal.firwin(5001, [3100, 6300], pass_zero='bandpass', fs=44100)
    filtered_data = np.float32((filtered_data + coefficients[5] * signal.convolve(data, b, mode='same')))
    
    b = signal.firwin(5001, [6300, 12700], pass_zero='bandpass', fs=44100)
    filtered_data = np.float32((filtered_data + coefficients[6] * signal.convolve(data, b, mode='same')))
    
    b = signal.firwin(5001, [12700, 20000], pass_zero='bandpass', fs=44100)
    filtered_data = np.float32((filtered_data + coefficients[7] * signal.convolve(data, b, mode='same')))

    return np.int16(filtered_data / np.max(np.abs(filtered_data)) * 32767)


def play_audio():
    wf = wave.open(file_path, 'rb')
    p = pyaudio.PyAudio()

    def callback(in_data, frame_count, time_info, status):
        if filter_on:
            data = np.frombuffer(wf.readframes(frame_count), dtype=np.int16)
            data = apply_equalizer(coefficients, data)
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
file_btn.place(relx=0.1, rely=0.2, anchor="center")

# Define the play/stop button
play_btn = tk.Button(root, text="Play", command=play_stop, font=("Bahnschrift", 16))
play_btn.place(relx=0.1, rely=0.8, anchor="center")

# Define the filter_on button
filter_btn = tk.Button(root, text="Filter: OFF", command=toggle_filter, font=("Bahnschrift", 16))
filter_btn.place(relx=0.1, rely=0.35, anchor="center")


# Run the main loop
root.mainloop()
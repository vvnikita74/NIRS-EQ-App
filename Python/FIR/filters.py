from scipy import signal
from statistics import mean
import numpy as np

#----------FIR FILTERS-------------

#----BANDPASS-----

# Define a function for rectangle bandpass filter 
def rectangular_window_filter_bandpass(data, order=5001, low_cutoff=1000, high_cutoff=10000):
    
    cutoff_freq = [low_cutoff, high_cutoff]
    
    # coefficients for rectangular window
    b = signal.firwin(order, cutoff_freq, pass_zero='bandpass', fs=44100)
    
    # apply filter to audio signal
    filtered_data = np.float32(signal.convolve(data, b, mode='same'))

    # normalize filter result for playback
    filtered_data = np.int16(filtered_data / np.max(np.abs(filtered_data)) * 32767)
    
    return filtered_data


#----BANDSTOP-----

# Define a function for rectangle bandstop filter 
def rectangular_window_filter_bandstop(data, order=5001, low_cutoff=100, high_cutoff=10000):
    
    cutoff_freq = [low_cutoff, high_cutoff]
    
    # coefficients for rectangular window
    b = signal.firwin(order, cutoff_freq, pass_zero='bandstop', fs=44100)
    
    # apply filter to audio signal
    filtered_data = np.float32(signal.convolve(data, b, mode='same'))

    # normalize filter result for playback
    filtered_data = np.int16(filtered_data / np.max(np.abs(filtered_data)) * 32767)
    
    return filtered_data


#----HIGHPASS-----

# Define a function for rectangle highpass filter 
def rectangular_window_filter_highpass(data, order=5001, cutoff_freq=10000):

    # coefficients for rectangular window
    b = signal.firwin(order, cutoff_freq, pass_zero='highpass', fs=44100)
    
    # apply filter to audio signal
    filtered_data = np.float32(signal.convolve(data, b, mode='same'))

    # normalize filter result for playback
    filtered_data = np.int16(filtered_data / np.max(np.abs(filtered_data)) * 32767)
    
    return filtered_data


#----LOWPASS------

# Define a function for rectangle lowpass filter 
def rectangular_window_filter_lowpass(data, order=5000, cutoff_freq=100):

    # coefficients for rectangular window
    b = signal.firwin(order, cutoff_freq, pass_zero='lowpass', fs=44100)
    
    # apply filter to audio signal
    filtered_data = np.float32(signal.convolve(data, b, mode='same'))

    # normalize filter result for playback
    filtered_data = np.int16(filtered_data / np.max(np.abs(filtered_data)) * 32767)
    
    return filtered_data


#----MULTIPLE BANDS-------

# Define a function for multiple band filters

def apply_equalizer(coefficients, data, order, frequency, fs):
    
    # Checking for the same coefficients -> reducing the overall volume
    if coefficients.count(coefficients[0]) == len(coefficients):
        return (data*coefficients[0]).astype(np.int16).tobytes()

    filtered_data = np.zeros_like(data, dtype=np.int16)

    b = signal.firwin(order, frequency[0], pass_zero='lowpass', fs=fs)
    filtered_data = np.float32((filtered_data + coefficients[0] * signal.convolve(data, b, mode='same')))
    
    for i in range(len(frequency)-1):
        b = signal.firwin(5001, [frequency[i], frequency[i+1]], pass_zero='bandpass', fs=fs)
        filtered_data = np.float32((filtered_data + coefficients[i+1] * signal.convolve(data, b, mode='same')))

    b = signal.firwin(order, frequency[-1], pass_zero='highpass', fs=fs)
    filtered_data = np.float32((filtered_data + coefficients[-1] * signal.convolve(data, b, mode='same')))
    
    return np.int16(filtered_data / np.max(np.abs(filtered_data)) * 32767)

#----EFFECTS--------

def apply_delay(data, delay_amount):
    delay_length = int(delay_amount * 44100)
    delay_signal = np.zeros(delay_length + len(data))

    for i in range(len(data)):
        delay_signal[i + delay_length] = data[i] + np.float64(delay_signal[i]/(i+3))
    
    return np.int16(delay_signal / np.max(np.abs(delay_signal)) * 6000)


'''
def apply_distortion(data, gain):
    distorted_data = np.tanh(gain * data)
    return np.int16(distorted_data / np.max(np.abs(distorted_data)) * 32767 * gain)'''


def apply_vibrato(data, vibrato_rate, vibrato_depth, sample_rate):
    num_samples = len(data)
    time = np.arange(num_samples) / sample_rate  # Временная ось

    # Рассчитайте смещение на основе модуляционной частоты и глубины модуляции
    vibrato_offset = vibrato_depth * np.sin(2 * np.pi * vibrato_rate * time)

    # Примените смещение к частоте сигнала
    vibrato_data = np.interp(time + vibrato_offset, time, data)

    return np.int16(vibrato_data / np.max(np.abs(vibrato_data)) * 8000)
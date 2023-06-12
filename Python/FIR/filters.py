from scipy import signal
import numpy as np

#----------FIR FILTERS-------------

#----BANDPASS-----

# Define a function for rectangle bandpass filter 
def rectangle_window_filter_bandpass(data, order=5001, low_cutoff=100, high_cutoff=10000):
    
    cutoff_freq = [low_cutoff, high_cutoff]
    
    # coefficients for rectangular window
    b = signal.firwin(order, cutoff_freq, window='rectangular', pass_zero='bandpass', fs=44100)

    # apply filter to audio signal
    filtered_data = signal.lfilter(b, 1, data)

    # normalize filter result for playback
    filtered_data = np.int16(filtered_data / np.max(np.abs(filtered_data)) * 32767)
    
    return filtered_data

# Define a function for hamming bandpass filter 
def hamming_window_filter_bandpass(data, order=5001, low_cutoff=100, high_cutoff=10000):
    
    cutoff_freq = [low_cutoff, high_cutoff]
    
    # coefficients for hamming window
    b = signal.firwin(order, cutoff_freq, window='hamming', pass_zero='bandpass', fs=44100)

    # apply filter to audio signal
    filtered_data = signal.lfilter(b, 1, data)

    # normalize filter result for playback
    filtered_data = np.int16(filtered_data / np.max(np.abs(filtered_data)) * 32767)
    
    return filtered_data

#----BANDSTOP-----

# Define a function for rectangle bandstop filter 
def rectangle_window_filter_bandstop(data, order=5001, low_cutoff=100, high_cutoff=10000):
    
    cutoff_freq = [low_cutoff, high_cutoff]
    
    # coefficients for rectangular window
    b = signal.firwin(order, cutoff_freq, window='rectangular', pass_zero='bandstop', fs=44100)

    # apply filter to audio signal
    filtered_data = signal.lfilter(b, 1, data)

    # normalize filter result for playback
    filtered_data = np.int16(filtered_data / np.max(np.abs(filtered_data)) * 32767)
    
    return filtered_data

# Define a function for hamming bandstop filter 
def hamming_window_filter_bandstop(data, order=5001, low_cutoff=100, high_cutoff=10000):
    
    cutoff_freq = [low_cutoff, high_cutoff]
    
    # coefficients for hamming window
    b = signal.firwin(order, cutoff_freq, window='hamming', pass_zero='bandstop', fs=44100)

    # apply filter to audio signal
    filtered_data = signal.lfilter(b, 1, data)

    # normalize filter result for playback
    filtered_data = np.int16(filtered_data / np.max(np.abs(filtered_data)) * 32767)
    
    return filtered_data

#----HIGHPASS-----

# Define a function for rectangle highpass filter 
def rectangle_window_filter_highpass(data, order=5001, cutoff_freq=10000):

    # coefficients for rectangular window
    b = signal.firwin(order, cutoff_freq, window='rectangular', pass_zero='highpass', fs=44100)
    
    # coefficients for hamming window
    # b = signal.firwin(order, cutoff_freq, window='hamming', pass_zero='highpass', fs=44100)

    # apply filter to audio signal
    filtered_data = signal.lfilter(b, 1, data)

    # normalize filter result for playback
    filtered_data = np.int16(filtered_data / np.max(np.abs(filtered_data)) * 32767)
    
    return filtered_data

# Define a function for hamming highpass filter 
def hamming_window_filter_highpass(data, order=5001, cutoff_freq=10000):

    # coefficients for hamming window
    b = signal.firwin(order, cutoff_freq, window='hamming', pass_zero='highpass', fs=44100)

    # apply filter to audio signal
    filtered_data = signal.lfilter(b, 1, data)

    # normalize filter result for playback
    filtered_data = np.int16(filtered_data / np.max(np.abs(filtered_data)) * 32767)
    
    return filtered_data

#----LOWPASS------

# Define a function for rectangle lowpass filter 
def rectangle_window_filter_lowpass(data, order=5000, cutoff_freq=100):

    # coefficients for rectangular window
    b = signal.firwin(order, cutoff_freq, window='rectangular', pass_zero='lowpass', fs=44100)

    # apply filter to audio signal
    filtered_data = signal.lfilter(b, 1, data)

    # normalize filter result for playback
    filtered_data = np.int16(filtered_data / np.max(np.abs(filtered_data)) * 32767)
    
    return filtered_data

# Define a function for hamming lowpass filter 
def hamming_window_filter_lowpass(data, order=5000, cutoff_freq=100):
    
    # coefficients for hamming window
    b = signal.firwin(order, cutoff_freq, window='hamming', pass_zero='lowpass', fs=44100)
    
    # apply filter to audio signal
    filtered_data = signal.lfilter(b, 1, data)

    # normalize filter result for playback
    filtered_data = np.int16(filtered_data / np.max(np.abs(filtered_data)) * 32767)
    
    return filtered_data

# Define a function for multiple band filters
from scipy import signal
import numpy as np

#----------IIR FILTERS-------------

#----BANDPASS-----

# Define a function for cheby filter 
def cheby_filter_bandpass(data):
    
    # define IIR filter parameters
    order = 10 # filter order
    low_cutoff = 150 # Lower cutoff frequency in Hz
    high_cutoff = 6000 # Upper cutoff frequency in Hz
    cutoff_freq = [low_cutoff, high_cutoff]
    
    # coefficients for cheby filter
    b, a = signal.cheby1(order, 3, cutoff_freq, 'bandstop', fs=44100)
    
    # apply filter to audio signal
    filtered_data = signal.filtfilt(b, a, data)
        
    # normalize filter result for playback  
    filtered_data = np.int16(filtered_data / np.max(np.abs(filtered_data)) * 32767)
    return filtered_data

# Define a function for butter filter 
def butter_filter_bandpass(data):
    
    # define IIR filter parameters
    order = 10 # filter order
    low_cutoff = 150 # Lower cutoff frequency in Hz
    high_cutoff = 6000 # Upper cutoff frequency in Hz
    cutoff_freq = [low_cutoff, high_cutoff]
    
    # coefficients for butterworth filter
    b, a = signal.butter(order, cutoff_freq, 'bandstop', fs=44100)
    
    # apply filter to audio signal
    filtered_data = signal.filtfilt(b, a, data)
        
    # normalize filter result for playback  
    filtered_data = np.int16(filtered_data / np.max(np.abs(filtered_data)) * 32767)
    return filtered_data

#----HIGHPASS-----

# Define a function for butter filter 
def cheby_filter_highpass(data):
    
    # define FIR filter parameters
    order = 10 # filter order
    cutoff_freq = 1000 # сutoff frequency in Hz

    # coefficients for chebyshev filter of the 1st kind
    b, a = signal.cheby1(order, 3, cutoff_freq, 'highpass', fs=44100)
    
    # apply filter to audio signal
    filtered_data = signal.filtfilt(b, a, data)
        
    # normalize filter result for playback  
    filtered_data = np.int16(filtered_data / np.max(np.abs(filtered_data)) * 32767)
    return filtered_data

# Define a function for butter filter 
def butter_filter_highpass(data):
    
    # define FIR filter parameters
    order = 10 # filter order
    cutoff_freq = 1000 # сutoff frequency in Hz
    
    # coefficients for butterworth filter
    b, a = signal.butter(order, cutoff_freq, 'highpass', fs=44100)
    
    # apply filter to audio signal
    filtered_data = signal.filtfilt(b, a, data)
        
    # normalize filter result for playback  
    filtered_data = np.int16(filtered_data / np.max(np.abs(filtered_data)) * 32767)
    return filtered_data

#----LOWPASS------

# Define a function for butter filter 
def butter_filter_lowpass(data):
    
    # define IIR filter parameters
    order = 10 # filter order
    cutoff_freq = 1000 # сutoff frequency in Hz
    
    # coefficients for butterworth filter
    b, a = signal.butter(order, cutoff_freq, 'lowpass', fs=44100)
    
    # coefficients for chebyshev filter of the 1st kind
    # b, a = signal.cheby1(order, 3, cutoff_freq, 'lowpass', fs=44100)
    
    # apply filter to audio signal
    filtered_data = signal.filtfilt(b, a, data)
        
    # normalize filter result for playback  
    filtered_data = np.int16(filtered_data / np.max(np.abs(filtered_data)) * 32767)
    return filtered_data

# Define a function for butter filter 
def cheby_filter_lowpass(data):
    
    # define IIR filter parameters
    order = 10 # filter order
    cutoff_freq = 1000 # сutoff frequency in Hz
    
    # coefficients for chebyshev filter of the 1st kind
    b, a = signal.cheby1(order, 3, cutoff_freq, 'lowpass', fs=44100)
    
    # apply filter to audio signal
    filtered_data = signal.filtfilt(b, a, data)
        
    # normalize filter result for playback  
    filtered_data = np.int16(filtered_data / np.max(np.abs(filtered_data)) * 32767)
    return filtered_data
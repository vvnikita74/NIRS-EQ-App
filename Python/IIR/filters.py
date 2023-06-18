from scipy import signal
import numpy as np

#----------IIR FILTERS-------------

#----BANDPASS-----

#----HIGHPASS-----

#----LOWPASS------

# Define a function for butter filter 
def cheby_filter_lowpass(data):
    
    # define FIR filter parameters
    order = 6 # filter order
    cutoff_freq = 100 # сutoff frequency in Hz

    # coefficients for chebyshev filter of the 1st kind
    b, a = signal.cheby1(order, 3, cutoff_freq, btype='lowpass', fs=44100)
    
    # coefficients for butterworth filter
    # b, a = signal.butter(order, cutoff_freq, btype='low', fs=44100)

    # apply filter to audio signal
    filtered_data = signal.lfilter(b, a, data)
        
    # normalize filter result for playback  
    filtered_data = np.int16(filtered_data / np.max(np.abs(filtered_data)) * 32767)
    return filtered_data
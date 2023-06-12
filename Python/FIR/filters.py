from scipy import signal
from statistics import mean
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


#----HIGHPASS-----

# Define a function for rectangle highpass filter 
def rectangle_window_filter_highpass(data, order=5001, cutoff_freq=10000):

    # coefficients for rectangular window
    b = signal.firwin(order, cutoff_freq, window='rectangular', pass_zero='highpass', fs=44100)
    
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


#----MULTIPLE BANDS-------

# Define a function for multiple band filters

def apply_equalizer(coefficients, data, order, frequency, fs):
    filtered_data = np.zeros_like(data, dtype=np.int16)

    b = signal.firwin(order, frequency[0], pass_zero='lowpass', fs=44100)
    filtered_data = np.float32((filtered_data + coefficients[0] * signal.convolve(data, b, mode='same')))
    
    for i in range(len(frequency)-1):
        b = signal.firwin(5001, [frequency[i], frequency[i+1]], pass_zero='bandpass', fs=fs)
        filtered_data = np.float32((filtered_data + coefficients[i+1] * signal.convolve(data, b, mode='same')))

    b = signal.firwin(order, frequency[-1], pass_zero='highpass', fs=44100)
    filtered_data = np.float32((filtered_data + coefficients[-1] * signal.convolve(data, b, mode='same')))

    # if want to decrease a full volume with equal coefficients
    '''
    if coefficients.count(coefficients[0]) == len(coefficients):
        return np.int16((filtered_data / np.max(np.abs(filtered_data)) * 32767)* mean(coefficients))
    else:
        return np.int16(filtered_data / np.max(np.abs(filtered_data)) * 32767)
    '''
    
    # default mode
    return np.int16(filtered_data / np.max(np.abs(filtered_data)) * 32767)
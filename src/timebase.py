import numpy as np

def generate_time_axis(fs, duration):
    return np.linspace(0, duration, int(fs*duration), endpoint=False)

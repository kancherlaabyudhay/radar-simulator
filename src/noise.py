import numpy as np

def add_noise(signal, sigma):
    noise = np.random.normal(0, sigma, size=signal.shape)
    return signal + noise

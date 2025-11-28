import numpy as np
from scipy.signal import fftconvolve

def matched_filter(signal, template):
    # flip template for cross-correlation behavior using convolution
    tpl = template[::-1]
    conv = fftconvolve(signal, tpl, mode="same")
    # normalize to unit peak for easier thresholding
    if np.max(np.abs(conv)) != 0:
        conv = conv / np.max(np.abs(conv))
    return conv

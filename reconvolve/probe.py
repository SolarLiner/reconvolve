import json
import math
import os

import numpy as np
import scipy.signal as sig
from scipy.io import wavfile


class Probe:
    def __init__(self, sample_rate: int):
        if sample_rate < 0:
            raise ValueError("Sample rate can't be negative")
        self.sample_rate = sample_rate

    def generate(self, amplitude=0.7, length=4.0):
        w1 = 10
        w2 = self.sample_rate / 2.0
        t = np.linspace(0, length, np.ceil(self.sample_rate * length))
        K = 2 * math.pi * (w1 * length) / np.log(w2 / w1)
        L = length / np.log(w2 / w1)
        amp = amplitude * np.subtract(1.0, np.exp(-100*t))[-1::-1]
        return np.sin(K * (np.exp(t / L) - 1.0)) * amp

    def process(self, generated: np.ndarray, recorded: np.ndarray):
        w1 = 10
        w2 = self.sample_rate / 2.0

        sweep_smplen = int(generated.size)
        k_end = 10 ** ((-6 * np.log2(w2 / w1)) / 20)
        k = np.log(k_end) / sweep_smplen

        attenuation = np.exp(np.arange(sweep_smplen) * k)
        divisor = generated[-1::-1] * attenuation

        if len(np.shape(recorded)) == 1:
            impulse_out = sig.wiener(sig.fftconvolve(recorded, divisor))[sweep_smplen:]
            sample_max = np.max(np.abs(impulse_out))
            return np.float32(impulse_out)/sample_max
        elif len(np.shape(recorded)) == 2:
            reshaped_record = np.array(list(zip(*recorded)))
            impulse_out = list()
            for x in reshaped_record:
                impulse_out.append(sig.wiener(sig.fftconvolve(x, divisor))[sweep_smplen:])
            sample_max = np.max(np.abs(impulse_out))
            return np.float32(np.array(list(zip(*impulse_out))) / sample_max)
        else:
            raise ValueError(f"Recorded signal has a weird shape {np.shape(recorded)}")

    def write(self, filename: str, arr: np.ndarray):
        scaled = np.float32(arr)
        wavfile.write(filename, self.sample_rate, scaled)

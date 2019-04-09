import scipy.signal as sig
import scipy.fftpack as fft
from scipy.io import wavfile
import numpy as np

from bin import setup
from bin.create import CreateCommand
from bin.process import ProcessCommand


def run():
    args, logger, command = setup([CreateCommand(), ProcessCommand()])
    return command.run(args)


if __name__ == "__main__":
    exit(run())

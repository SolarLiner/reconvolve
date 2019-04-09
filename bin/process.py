from argparse import ArgumentParser, Namespace, FileType
import logging

import numpy as np
import scipy.signal as sig
from scipy.io import wavfile

from . import BaseCommand

logger = logging.getLogger(__name__)


class ProcessCommand(BaseCommand):
    name = "process"
    description = "Process the recording into a convolver impulse response. Note that both files must have the same sample rate."

    def setup(self, parser: ArgumentParser):
        parser.add_argument("sweep",
                            type=FileType("rb"),
                            help="Generated sweep file")
        parser.add_argument("record",
                            type=FileType("rb"),
                            help="Recorded response")
        parser.add_argument("output",
                            type=FileType("wb"),
                            help="Output impulse response")

    def run(self, args: Namespace):
        sweep_rate, sweep_in = wavfile.read(args.sweep)
        record_rate, record_in = wavfile.read(args.record)

        if sweep_rate != record_rate:
            raise ValueError("Sample rates do not match, IR cannot be generated")

        w1 = 20
        w2 = sweep_rate / 2.0

        sweep_length = int(sweep_in.size)
        k_end = 10**((-6 * np.log2(w2 / w1)) / 20)
        k = np.log(k_end) / sweep_length

        attenuation = np.exp(np.arange(sweep_length) * k)
        divisor: np.ndarray = sweep_in[-1::-1] * attenuation

        if len(np.shape(record_in)) == 1:
            impulse_out = sig.wiener(sig.fftconvolve(record_in, divisor))
            sample_max = np.max(np.abs(impulse_out))
            wavfile.write(args.output, sweep_rate, np.float32(impulse_out / sample_max))
            return 0
        elif len(np.shape(record_in)) == 2:
            reshaped_record = np.array(list(zip(*record_in)))
            impulse_out = list()
            for x in reshaped_record:
                impulse_out.append(sig.wiener(sig.fftconvolve(x, divisor)))
            sample_max = np.max(np.abs(impulse_out))
            wavfile.write(
                args.output, sweep_rate,
                np.float32(np.array(list(zip(*impulse_out))) / sample_max))
            return 0
        else:
            logger.critical(
                "The record sound file has a weird shape. Are you sure it's the right one?"
            )
            return 1

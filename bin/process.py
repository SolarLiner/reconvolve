from argparse import ArgumentParser, Namespace, FileType
import logging

import numpy as np
import scipy.signal as sig
from scipy.io import wavfile

from reconvolve.probe import Probe
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

        try:
            p = Probe(sweep_rate)
            result = p.process(np.float32(sweep_in), np.float32(record_in))
            p.write(args.output, result)
            return 0
        except ValueError as e:
            logger.critical(f"E: {str(e)}")
            return 1
        except:
            logger.critical("Unknown error.")
            return 10

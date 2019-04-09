from argparse import ArgumentParser, Namespace
import logging

from . import BaseCommand
from lib.probe import Probe

logger = logging.getLogger(__name__)


class CreateCommand(BaseCommand):
    name = "create"
    description = "Create the sweep signal to be used for the recording of the response"
    def setup(self, parser: ArgumentParser):
        parser.add_argument("file", help="Output wav file. Will also output metadata json next to it.")
        parser.add_argument("-l", "--length", type=float, nargs='?', default=2.0, help="Length of the input signal")
        parser.add_argument("-a", "--amplitude", type=float, nargs='?', default=0.7, help="Amplitude of the input signal")
        parser.add_argument("--samplerate", type=int, default=int(48e3), help="Sample rate (default 48000)")

    def run(self, args: Namespace):
        logger.debug(repr(args.__dict__))
        w1 = 20
        w2 = args.samplerate / 2.0
        p = Probe(w1, w2)
        p.sample_rate = args.samplerate
        array = p.generate(args.amplitude, args.length)
        p.write(args.file, array)
        return 0

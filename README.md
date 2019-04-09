# reconvolve
Create convolution impulse response from frequency sweep inputs

Reconvolve is a small CLI written in python which aims at helping create high-quality impulse responses by recording the medium of interest.  
The easiest way to do that is to record a click sound as passed through the medium and record the output - but those are limited in quality (more technically, temporal resolution). A better solution would be to have a longer input sound that would still capture the desired spectrum; this is where sine sweep impulses enter. But while they give better results, you can't directly use the recording as an impulse response, and need to convolve it back to a usable one.

## Use

```bash
python main.py create sweep.wav
```
Creates a sine sweep from 20 Hz to 20 kHz sampled at 48 kHz.

```bash
python main.py process sweep.wav record.wav IR_out.wav
```
Processes a recording `record.wav` of the impulse `sweep.wav` into `IR_out.wav`.

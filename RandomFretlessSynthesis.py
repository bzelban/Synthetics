######################################################################
# Theremin.AI Sound Synthesis
# In 2 Octave Range, Random Sound in Fretless Mode
# Bedirhan Z. ELBAN
######################################################################

"""
    To Make it usable, those steps are necessary:
    ~ pip install wheel
    ~ pip install pipwin
    ~ pipwin install pyaudio
    ~ Then install other common libraries with pip (scipy, numpy, etc)
"""


import numpy as np
import time

# Sample Rate may cripples CPU we have to calibrate later
# DSP (Digital Sound Processing) chips can handle sample rates easily
# but common CPU's works fairly on basic Signals
sample_rate = 44100


import random


# random Amplitude part of Random Sound Synthesis
def randomAmp():
    randA = random.uniform(0.0, 1.0)
    return randA


# random time generation
def randTime():
    randT = random.uniform(0.5, 2.0)
    randT = round(randT, 1)
    return randT


# This time, pitch isn't accorded well, output is fretless
def randomPitch():
    randP = random.uniform(220.00, 830.62)
    randP = round(randP, 2)
    return randP


import pyaudio
p = pyaudio.PyAudio()

# for paFloat32 sample values must be in range [-1.0, 1.0]
stream = p.open(format=pyaudio.paFloat32,
                channels=1,
                rate=sample_rate,
                output=True)

# This plays the sounds
while(True):
    f = randomPitch()
    duration = randTime()
    volume = randomAmp()
    fs = sample_rate

    sample = (np.sin(2 * np.pi * np.arange(fs * duration) * f / fs)).astype(np.float32)
    if (volume == 0.0):
        time.sleep(duration)
    else:
        stream.write(volume*sample)
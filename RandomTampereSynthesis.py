######################################################################
# Theremin.AI Sound Synthesis
# In 2 Octave Range, Random Sound in Tampere Mode
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
# but common CPU's works fairly on double type, not floats
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


# random Pitch part of Random Sound Synthesis
# Tradinional Theremins pitch antenna distance = ~40-50 cm
# For experimenting, I used as 48 cm to get 2 octaves 48 cm / 24 notes (2 Octaves)
# Distance Calibration is LETHAL!!
def randomPitch():

    # If somebody asks the math behind tampere frequencies, I will explain later
    _refFreqA3 = 220 # This is A3, as a reference point
    _constantFreq = 1.05946309434 # frequency handler

    randomPos = random.randint(0, 25)

    randP = _refFreqA3 * _constantFreq ** randomPos
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
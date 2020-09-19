########################################################
#Tone (pitch) generator
# Bedirhan Z. ELBAN #
# *- Also, No Python Libraries were harmed in the making of this script
#######################################################


from math import cos
import scipy as scp
import wave
import matplotlib.pyplot as plt

from scipy import signal
from numpy import linspace, sin, pi, int16, cos
from pylab import plot, show, title, xlabel, ylabel, subplot
from scipy.fftpack import rfft



def sine_note(freq, len, amp=10000, samp_rate=44100):
    t = linspace(0,len,len*samp_rate)
    data = sin(2*pi*freq*t)*amp
    return data.astype(int16) # two byte integers

def cosine_note(freq, len, amp=10000, samp_rate=44100):
    t = linspace(0,len,len*samp_rate)
    data = cos(2*pi*freq*t)*amp
    return data.astype(int16) # two byte integers

def saw_note(frq,len,samp_rate,Amp):
    ts = linspace(0, len, len*samp_rate)
    tsaw = scp.signal.sawtooth(2 * pi*frq* ts,1)*Amp
    return tsaw.astype(int16)

def triangle_note(frq,len,samp_rate,Amp):
    tt = linspace(0, len, len*samp_rate)
    trng = scp.signal.sawtooth(2 * pi*frq* tt,0.5)*Amp
    return trng.astype(int16)

def square_note(frq,len,samp_rate,Amp):
    tq = linspace(0, len, len*samp_rate)
    sqr = scp.signal.square(2* pi*frq* tq)*Amp
    return sqr.astype(int16)

def impulse_note(frq,len,samp_rate,duty_cycle,Amp):
    ti = linspace(0, len, len*samp_rate)
    imp = scp.signal.square(2 * pi*frq* ti,0.2)*Amp
    return imp.astype(int16)


def save_wav(signal,fname):
    total_samples=len(signal) # get the number of samples
    wav_file=wave.open(fname,"wb")
    wav_file.setnchannels(1)
    wav_file.setsampwidth(2)
    wav_file.setframerate(44100)
    wav_file.setnframes(total_samples)
    wav_file.writeframes(signal) # writing the sound to a file
    wav_file.close()



########################################################
# From C0 to infinite, you can run this freq() easily

# Formula I used is f = Referance Frequency (C0) * (Constant ^ (NoteIndex + NoteOctave))

_refFreqC0 = 16.35 # This is C0 frequency
_constantFreq = 1.05946309434

# This is only for the indexing issues, I didn't used the sharps and flats from here
_noteTableArray = ["C", "Cs", "D", "Ds", "E", "F", "Fs", "G", "Gs", "A", "As", "B"]


def freq(desired_note, ref_freq):
    _tempNoteArray = list(desired_note)
    _tempNoteArrayLen = len(_tempNoteArray)

    if _tempNoteArrayLen == 2:

        _tempNoteLast = _tempNoteArrayLen - 1
        _noteOctave = int(_tempNoteArray[_tempNoteLast]) * 12

        _noteKey = _tempNoteArray[0]
        _noteKey = _noteKey.upper()

        _noteIndex = _noteTableArray.index(_noteKey)

    elif _tempNoteArrayLen == 3:

        _tempNoteLast = _tempNoteArrayLen - 1
        _noteOctave = int(_tempNoteArray[_tempNoteLast]) * 12

        _noteKey = _tempNoteArray[0]
        _noteKey = _noteKey.upper()

        if _tempNoteArray[1] == "s":
            # print("sharp")
            _noteIndex = _noteTableArray.index(_noteKey)
            _noteIndex = _noteIndex + 1

        elif _tempNoteArray[1] == "b":
            # print("flat")
            _noteIndex = _noteTableArray.index(_noteKey)
            _noteIndex = _noteIndex - 1

    else:
        print("Wrong input")
        exit()

    # print(_noteOctave)
    # print(_noteKey)
    # print(_noteIndex)

    _noteStepDiff = _noteIndex + _noteOctave

    _theNote = ref_freq * _constantFreq ** _noteStepDiff

    return _theNote
################# END_OF_FUNCTION ##################################

# print(freq("g3", _refFreqC0)) # upper/lover note, with/without sharp/flat CHECK


# I wanted a util, global frequency calculator, Also I'll use freq() to build triads for Vigdis, my FM_Synthesis

# Part 2, a)
new_freq = freq("C4", _refFreqC0)

# Part 2, b)
_tone1 = impulse_note(new_freq, 1,44100,0.2,5000)
_tone2 = saw_note(new_freq, 1, 44100, 6000)
_tone3 = triangle_note(new_freq, 1, 44100, 4000)
_tone4 = square_note(new_freq, 1, 44100, 3000)
_tone5 = sine_note(new_freq, 1, 8000, 44100)

#_toneA = _tone1 + _tone2 + _tone3 + _tone4 + _tone5 # Not my organ sound xD
# save_wav(_toneA, 'part2b.wav')

_tone12 = _tone1 + _tone2

#save_wav(_tone12, 'kick.wav')

"""
# Lead sound created by adding square + sine below here
dyna_Note = "E5"
time_sig = 3

lead_freq = freq(dyna_Note, _refFreqC0)
frac1 = square_note(lead_freq, time_sig, 44100, 3000)
frac2 = sine_note(lead_freq, time_sig, 8000, 44100)
tone_lead =  frac1 + frac2
saveName = dyna_Note + str(time_sig)
save_wav(tone_lead, saveName)
#######################################################
"""


"""
# Kick sound created by adding impulse + saw
time_sig = 1

lead_freq = freq(dyna_Note, _refFreqC0)

fkick1 = impulse_note(new_freq, time_sig,44100,0.2,5000)
fkick2 = saw_note(new_freq, time_sig, 44100, 6000)
tone_lead =  frac1 + frac2
saveName = dyna_Note + str(time_sig)
save_wav(tone_lead, saveName + ".wav")
"""


##################### C0 to C5 Part ####################################
"""

# Lazy Student nested for loop part
# C0 to C5 part

for i in range(len(_noteTableArray)):
    for j in range(0,6):
        j_temp = j
        tempJ = str(j_temp)
        loopAll = _noteTableArray[i] + tempJ
        loopNote = freq(loopAll, _refFreqC0)
        # print("Frequency:")
        # print(loopNote)
        # print("Name:")
        # print( loopAll)
        frac1loop = square_note(loopNote, 1, 44100, 3000)
        frac2loop = sine_note(loopNote, 1, 8000, 44100)
        loopWave = frac1loop

        save_wav(loopWave, loopAll + ".wav")
################################################### 
"""

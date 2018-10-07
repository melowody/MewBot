#  _________________________________________________________________________________________________________________________
# |                                                                                                                         |
# |                                                                                                                         |
# | This code is taken from JCx on stackoverflow. Many thanks to him for this. https://stackoverflow.com/a/33913403/4503723 |
# |                                                                                                                         |
# |_________________________________________________________________________________________________________________________|




import math
import wave
import struct
from pydub import AudioSegment
import sys

AudioSegment.converter = "./Resources/Interactive/ffmpeg.exe"

# Audio will contain a long list of samples (i.e. floating point numbers describing the
# waveform).  If you were working with a very long sound you'd want to stream this to
# disk instead of buffering it all in memory list this.  But most sounds will fit in
# memory.
def append_silence(audio, duration_milliseconds=500):
    """
    Adding silence is easy - we add zeros to the end of our array
    """
    num_samples = duration_milliseconds * (44100.0 / 1000.0)

    for x in range(int(num_samples)):
        audio.append(0.0)

    return audio


def append_sinewave(
        audio,
        freq=440.0,
        duration_milliseconds=500,
        volume=1.0):
    """
    The sine wave generated here is the standard beep.  If you want something
    more aggresive you could try a square or saw tooth waveform.   Though there
    are some rather complicated issues with making high quality square and
    sawtooth waves... which we won't address here :)
    """

    num_samples = duration_milliseconds * (44100.0 / 1000.0)

    for x in range(int(num_samples)):
        audio.append(volume * math.sin(2 * math.pi * freq * ( x / 44100.0 )))

    return audio


def save_wav(file_name, audio):
    # Open up a wav file
    wav_file=wave.open(file_name,"w")

    # wav params
    nchannels = 1

    sampwidth = 2

    # 44100 is the industry standard sample rate - CD quality.  If you need to
    # save on file size you can adjust it downwards. The stanard for low quality
    # is 8000 or 8kHz.
    nframes = len(audio)
    comptype = "NONE"
    compname = "not compressed"
    wav_file.setparams((nchannels, sampwidth, 44100.0, nframes, comptype, compname))

    # WAV files here are using short, 16 bit, signed integers for the
    # sample size.  So we multiply the floating point data we have by 32767, the
    # maximum value for a short integer.  NOTE: It is theortically possible to
    # use the floating point -1.0 to 1.0 data directly in a WAV file but not
    # obvious how to do that using the wave module in python.
    for sample in audio:
        wav_file.writeframes(struct.pack('h', int( sample * 32767.0 )))

    wav_file.close()

    return audio

def do(arg1, arg2, arg3):

    audio = []

    bpm = int(arg1)
    x = arg2
    name = arg3
    dictop = {"c": 16.3516, "csh": 17.3239, "db": 17.3239, "d": 18.3540, "dsh": 19.4454, "eb": 19.4454, "e": 20.6017, "f": 21.8268, "fsh": 23.1247, "gb": 23.1247, "g": 24.4997, "gsh": 25.9565, "ab": 25.9565, "a": 27.5, "ash": 29.1352, "bb": 29.1352, "b": 30.8677}

    x = x.split('|')
    y = []
    for i in x:
        y.append([])
    for i in range(len(y)):
            z = 0
            for j in range(len(x[i])):
                    if(x[i][j].isdigit()):
                            z = j
                            y[i].append(z)
    for i in range(len(y)):
        m2 = -1
        for j in range(len(y[i])):
            k = y[i][j]
            y[i][j] = x[i][m2 + 1:k + 1]
            m2 = k

    z = y
    m = 0
    listop = []
    for i in z:
            if(len(i) > m):
                    m = len(i)
    for i in range(m):
            listop.append([])
    for i in range(len(z)):
        while(len(z[i]) != m):
            z[i].append('')
    for i in z:
            for j in range(len(i)):
                listop[j].append(i[j])
    for i in range(m):
        x = listop[i]
        for j in range(len(x)):
            x[j] = x[j].lower()
            if(x[j] != ""):
                x[j] = dictop[x[j][:-1].replace('#', 'sh')] * 2**(int(x[j][-1]))
            else:
                x[j] = None
        pn = listop[i]
        audio = []
        t = (60/bpm)*1000
        for j in pn:
            if(j != None):
                append_sinewave(audio, freq=int(j), duration_milliseconds=t, volume=float(1)/m)
            else:
                append_silence(audio, duration_milliseconds=t)
        save_wav(name + str(i) + ".wav", audio)
    return m

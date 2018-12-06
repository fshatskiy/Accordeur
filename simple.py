try:
    import pyaudio
    import numpy as np
    import pylab
    import matplotlib.pyplot as plt
    from scipy.io import wavfile
    import time
    import sys
    import seaborn as sns
    from scipy import fftpack
except:
    print("Something didn't import")

FORMAT = pyaudio.paInt16
CHANNELS = 2
RATE = 44100
CHUNK = 1024
RECORD_SECONDS = 5

audio = pyaudio.PyAudio()
stream = audio.open(format=FORMAT, channels=CHANNELS,
                        rate=RATE, input=True,
                        frames_per_buffer=CHUNK)

i=0

# Prepare the Plotting Environment with random starting values
x = np.arange(10000)
y = np.random.randn(10000)

# Plot 0 is for raw audio data
# plt.title("Raw Audio Signal")
# Show the plot, but without blocking updates
# plt.pause(0.01)

def record():
    # start Recording
    print("recording...")
    frames = []

    for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
        data = stream.read(CHUNK)
        frames.append(data)
    print("finished recording")


def plot_data(in_data):
    # get and convert the data to float
    audio_data = np.fromstring(in_data, np.int16)
    print(audio_data)
    plt.plot(np.arange(len(audio_data)), audio_data)
    plt.pause(0.01)

    X = fftpack.fft(np.arange(len(audio_data)))
    freqs = fftpack.fftfreq(len(x)) * RATE

    plt.stem(freqs, np.abs(X))
    plt.xlabel('Frequency in Hertz [Hz]')
    plt.ylabel('Frequency Domain (Spectrum) Magnitude')
    plt.xlim(-RATE / 2, RATE / 2)
    plt.show()


record()
for i in range(0, 10):
    plot_data(stream.read(CHUNK))
    # test(stream.read(CHUNK), i)

# stop Recording
stream.stop_stream()
stream.close()
audio.terminate()

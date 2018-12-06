import numpy as np
import matplotlib.pylab as plt
from scipy import fftpack

f = 440  # Frequency, in cycles per second, or Hertz
f_s = 900  # Sampling rate, or number of measurements per second

t = np.linspace(0, 2, 2 * f_s, endpoint=False)
x = np.sin(f * 2 * np.pi * t)


plt.plot(t, x)
plt.xlabel('Time [s]')
plt.ylabel('Signal amplitude')
plt.show()

X = fftpack.fft(x)
freqs = fftpack.fftfreq(len(x)) * f_s

plt.stem(freqs, np.abs(X))
plt.xlabel('Frequency in Hertz [Hz]')
plt.ylabel('Frequency Domain (Spectrum) Magnitude')
plt.xlim(-f_s / 2, f_s / 2)
plt.show()

for i in range(len(np.abs(X))):
    if np.abs(X)[i] > 1:
        print("la frequence est: "+str(i/2))
        break

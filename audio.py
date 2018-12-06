import numpy as np
import scipy.io.wavfile as wf
import matplotlib.pylab as plt


def main():
    # use power of 2 for FFT length
    FFTN = 2**14

    # generate the signal if it doesn't exist
    FS = 48000.
    N = FS * 3
    y = np.sin(2. * np.pi * 20 * np.arange(N) / FS)

    # read a chunk of the signal and apply hanning window
    y1 = y[:FFTN] * np.hanning(FFTN)

    # plot the signal to verify it's correct
    plt.plot(y[: 20000])
    plt.title("signal")
    plt.xlabel("time")
    plt.ylabel("amplitude")
    plt.show()
    plt.plot(y1)
    plt.show()

    # take first half of the FFT because the second half is a mirror image
    Y = np.fft.fft(y1)[:FFTN//2]

    # convert to SPL in dB and calculate frequency scale
    SPL = 10 * np.log10(abs(Y)**2)
    FBINS = np.linspace(0., 24000., len(SPL))

    # plot the intensity
    plt.semilogx(FBINS, SPL)
    plt.show()

    # take first value in list, * in case it's a list of length 1
    maxf, *_ = FBINS[SPL == max(SPL)]
    print("Peak detected at:", maxf, "Hz")


if __name__ == "__main__":
    main()
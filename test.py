import pyaudio
import numpy as np
import matplotlib.pyplot as plt
import math
import os


class Menu:
    def __init__(self):
        self.choix = 1

    def menu(self):
        print("quelle corde voulez vous accorder? (1,2,3,4,5,6) exit")
        self.choix = input(">")
        if self.choix == "exit":
            exit()
        self.enter()

    def enter(self):
        if int(self.choix) > 6 or int(self.choix) < 1:
            self.menu()
        else:
            correspondance = ["E4", "B3", "G3", "D3", "A2", "E2"]
            accordeur = Accordeur(correspondance[int(self.choix)-1])
            accordeur.jsp()


class Accordeur:

    def __init__(self,corde):
        self.corde = corde
        self.A4 = 440.0
        self.A4_INDEX = 57
        self.notes = {
            "E2": {
                "E2b": 78,
                "E2": 82.41,
                "E2#": 87
                },
            "A2": {
                "A2b": 104,
                "A2": 110,
                "A2#": 117
                },
            "D3": {
                "D3b": 139,
                "D3": 147,
                "D3#": 156
                },
            "G3": {
                "G3b": 185,
                "G3": 196,
                "G3#": 208
                },
            "B3": {
                "B3b": 233,
                "B3": 247,
                "B3#": 262
                },
            "E4": {
                "E4b": 311,
                "E4": 330,
                "E4#": 349
                },
        }

        self.CHUNK = 5120  # number of data points to read at a time
        self.RATE = 12000  # time resolution of the recording device (Hz)

    def note(self, val):
        if val < self.notes[self.corde][self.corde+"b"]:
            print("trop bas")
            # print(str(self.notes[self.corde][self.corde+"b"]) + " b " + str(val) + " corde " + self.corde)
            return 1
        if val > self.notes[self.corde][self.corde+"#"]:
            print("trop haut")
            # print(str(self.notes[self.corde][self.corde + "#"]) + " # " + str(val))
            return -1
        if val < ((self.notes[self.corde][self.corde+"#"]-self.notes[self.corde][self.corde])/2)+ self.notes[self.corde][self.corde] and val > self.notes[self.corde][self.corde] - ((self.notes[self.corde][self.corde]-self.notes[self.corde][self.corde+"b"])/2):
            return 0

    def record(self):
        self.p = pyaudio.PyAudio()  # start the PyAudio class
        self.stream = self.p.open(format=pyaudio.paInt16, channels=1, rate=self.RATE, input=True,
                            frames_per_buffer=self.CHUNK)  # uses default input device

    def jsp(self):
        print("\t\t\t" + self.corde)
        self.record()
        np.set_printoptions(suppress=True)  # don't use scientific notation
        # create a numpy array holding a single read of audio data
        while True:  # to it a few times just to see
            data = np.fromstring(self.stream.read(self.CHUNK), dtype=np.int16)
            data = data * np.hanning(len(data))  # smooth the FFT by windowing data
            fft = abs(np.fft.fft(data).real)
            fft = fft[:int(len(fft)/2)]  # keep only first half
            freq = np.fft.fftfreq(self.CHUNK, 1.0/self.RATE)
            freq = freq[:int(len(freq)/2)]  # keep only first half
            freqPeak = freq[np.where(fft == np.max(fft))[0][0]]+1
            if freqPeak > self.notes[self.corde][self.corde+"#"]+100 or freqPeak < self.notes[self.corde][self.corde+"b"] - 100:
                pass
            else:
                print("peak frequency: %d Hz" % freqPeak)
                if self.note(freqPeak) == 0:
                    print("cette corde est bien accordée")
                    break
            # uncomment this if you want to see what the freq vs FFT looks like
            # plt.plot(freq, fft)
            # plt.axis([0, 400, None, None])
            # plt.show()
            # plt.close()

        # close the stream gracefully
        self.stream.stop_stream()
        self.stream.close()
        self.p.terminate()
        menu = Menu()
        menu.menu()


if __name__ == "__main__":
    menu = Menu()
    menu.menu()

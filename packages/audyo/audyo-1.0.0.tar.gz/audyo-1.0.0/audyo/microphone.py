from sys import byteorder
from array import array
from struct import pack
import pyaudio
import wave


class Microphone(object):

    def __init__(self, threshold=500, frame_length=1024, format=pyaudio.paInt16, rate=16000, out_file='rec.wav'):
        self.threshold = threshold
        self.frame_length = frame_length
        self.format = format
        self.rate = rate
        self.out_file = out_file

    def __is_silent(self, snd_data):
        "Returns 'True' if below the 'silent' threshold"
        return max(snd_data) < self.threshold

    def __normalize(self, snd_data):
        "Average the volume out"
        MAXIMUM = 16384
        times = float(MAXIMUM)/max(abs(i) for i in snd_data)

        r = array('h')
        for i in snd_data:
            r.append(int(i*times))
        return r

    def __trim(self, snd_data):
        "Trim the blank spots at the start and end"
        def _trim(snd_data):
            snd_started = False
            r = array('h')

            for i in snd_data:
                if not snd_started and abs(i)>self.threshold:
                    snd_started = True
                    r.append(i)

                elif snd_started:
                    r.append(i)
            return r

        # Trim to the left
        snd_data = _trim(snd_data)

        # Trim to the right
        snd_data.reverse()
        snd_data = _trim(snd_data)
        snd_data.reverse()
        return snd_data

    def __add_silence(self, snd_data, seconds):
        "Add silence to the start and end of 'snd_data' of length 'seconds' (float)"
        r = array('h', [0 for i in range(int(seconds * self.rate))])
        r.extend(snd_data)
        r.extend([0 for i in range(int(seconds * self.rate))])
        return r

    def __record(self):
        """
        Record a word or words from the microphone and
        return the data as an array of signed shorts.

        Normalizes the audio, trims silence from the
        start and end, and pads with 0.5 seconds of
        blank sound to make sure VLC et al can play
        it without getting chopped off.
        """
        p = pyaudio.PyAudio()
        stream = p.open(format=self.format, channels=1, rate=self.rate,
                        input=True, output=True,
                        frames_per_buffer=self.frame_length)

        num_silent = 0
        snd_started = False

        r = array('h')
        while num_silent < 30:
            if num_silent > 0:
                print(num_silent)
            # little endian, signed short
            snd_data = array('h', stream.read(self.frame_length))
            if byteorder == 'big':
                snd_data.byteswap()
            r.extend(snd_data)

            silent = self.__is_silent(snd_data)

            if silent and snd_started:
                num_silent += 1
            elif not silent and snd_started:
                num_silent = 0
            elif not silent and not snd_started:
                snd_started = True

        width = p.get_sample_size(self.format)
        stream.stop_stream()
        stream.close()
        p.terminate()

        r = self.__normalize(r)
        r = self.__trim(r)
        r = self.__add_silence(r, 0.5)
        return width, r

    def record_to_file(self):
        "Records from the microphone and outputs the resulting data to 'path'"
        width, data = self.__record()
        data = pack('<' + ('h'*len(data)), *data)

        wf = wave.open(self.out_file, 'wb')
        wf.setnchannels(1)
        wf.setsampwidth(width)
        wf.setframerate(self.rate)
        wf.writeframes(data)
        wf.close()


def main(out_file="audyo.wav"):
    microphone = Microphone()
    microphone.out_file = out_file
    microphone.record_to_file()


if __name__ == '__main__':
    main()

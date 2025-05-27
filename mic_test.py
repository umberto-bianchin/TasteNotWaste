import pyaudio
import wave

CHUNK = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100

p = pyaudio.PyAudio()

stream = p.open(format=FORMAT, channels=CHANNELS, rate=RATE, input=True, frames_per_buffer=CHUNK)

frames = []
seconds = 5
for i in range(0, int(RATE / CHUNK * seconds)):
    data = stream.read(CHUNK)
    frames.append(data)

stream.stop_stream()
stream.close()
p.terminate()

w = wave.open("test.wav", "wb")
w.setnchannels(CHANNELS)
w.setsampwidth(p.get_sample_size(FORMAT))
w.setframerate(RATE)
w.writeframes(b''.join(frames))
w.close()
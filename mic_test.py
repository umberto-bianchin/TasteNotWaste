import sounddevice as sd
import numpy as np
import matplotlib.pyplot as plt
from scipy.io.wavfile import write
import os

def list_input_devices():
    print("🎤 Available input devices:")
    devices = sd.query_devices()
    for i, dev in enumerate(devices):
        if dev['max_input_channels'] > 0:
            print(f"  {i}: {dev['name']}")

def record_audio(device_index, duration=5, samplerate=16000):
    print(f"\n🎙️ Recording from device {device_index} for {duration} seconds...")
    sd.default.device = (device_index, None)
    recording = sd.rec(int(duration * samplerate), samplerate=samplerate, channels=1, dtype='float32')
    sd.wait()
    return recording.flatten()

def save_audio(audio, samplerate=16000, filename="test.wav"):
    write(filename, samplerate, (audio * 32767).astype(np.int16))
    print(f"✅ Audio saved to {filename}")

def plot_waveform(audio, samplerate):
    times = np.arange(len(audio)) / float(samplerate)
    plt.figure(figsize=(10, 4))
    plt.plot(times, audio)
    plt.title("Recorded waveform")
    plt.xlabel("Time [s]")
    plt.ylabel("Amplitude")
    plt.grid(True)
    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    list_input_devices()
    device_index = int(input("\nSelect device index to record from: "))
    duration = int(input("Enter duration in seconds: ") or "5")

    audio = record_audio(device_index, duration)
    save_audio(audio)

    # Optionally play audio (macOS only)
    if os.name == "posix":
        os.system("afplay test.wav")

    plot_waveform(audio, samplerate=16000)

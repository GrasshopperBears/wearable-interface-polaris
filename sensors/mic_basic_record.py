import pyaudio
import wave

RATE = 16000
CHUNK = int(RATE * 0.3)
FORMAT = pyaudio.paInt16
CHANNELS = 1
RECORD_SECONDS = 120
INPUT_DEVICE_INDEX = 1

p = pyaudio.PyAudio()

stream = p.open(format=FORMAT,
                channels=CHANNELS,
                rate=RATE,
                input=True,
                input_device_index=INPUT_DEVICE_INDEX,
                frames_per_buffer=CHUNK)

print("Start to record the audio.")

frames = []

print("Enter source name")
filename = input()

for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
    data = stream.read(CHUNK)
    frames.append(data)

print("Recording is finished.")

stream.stop_stream()
stream.close()
p.terminate()

WAVE_OUTPUT_FILENAME = f"{filename}.wav"

wf = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
wf.setnchannels(CHANNELS)
wf.setsampwidth(p.get_sample_size(FORMAT))
wf.setframerate(RATE)
wf.writeframes(b''.join(frames))
wf.close()

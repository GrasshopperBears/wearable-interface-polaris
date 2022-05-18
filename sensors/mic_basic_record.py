import pyaudio
import wave

# {'index': 1, 'structVersion': 2, 'name': 'USB Audio: - (hw:1,0)', 'hostApi': 0, 'maxInputChannels': 2, 'maxOutputChannels': 2, 'defaultLowInputLatency': 0.007979166666666667, 'defaultLowOutputLatency': 0.007979166666666667, 'defaultHighInputLatency': 0.032, 'defaultHighOutputLatency': 0.032, 'defaultSampleRate': 48000.0}
RATE = 48000
CHUNK = 200
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
print("Start recording")

for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
    data = stream.read(CHUNK, exception_on_overflow = False)
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

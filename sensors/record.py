import pyaudio
import wave

FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 24000
CHUNK = 1024
RECORD_SECONDS = 150
INPUT_DEVICE_INDEX = 1

audio = pyaudio.PyAudio()

# start Recording
stream = audio.open(format=FORMAT,
                    rate=RATE,
                    input=True,
                    channels=CHANNELS,
                    input_device_index=INPUT_DEVICE_INDEX,
                    frames_per_buffer=CHUNK)


object_name = input("Enter object name: ")
frames = []

for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
  data = stream.read(CHUNK)
  frames.append(data)
print("Record finished. Now saving...")

# stop Recording
stream.stop_stream()
stream.close()
audio.terminate()

waveFile = wave.open('{}.wav'.format(object_name), 'wb')
waveFile.setnchannels(CHANNELS)
waveFile.setsampwidth(audio.get_sample_size(FORMAT))
waveFile.setframerate(RATE)
waveFile.writeframes(b''.join(frames))
waveFile.close()
print("Done.")

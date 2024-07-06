import pyaudio
import keyboard
import numpy as np
from transformers import pipeline

pipe = pipeline('automatic-speech-recognition', model='openai/whisper-base')
audio = pyaudio.PyAudio()

CHUNK = 1000
FORMAT = pyaudio.paFloat32
SAMPLING_RATE = 16_000
AUDIO_SCALE = 1.0


def record_and_write():
    frames = []
    stream = audio.open(format=FORMAT, channels=1, rate=SAMPLING_RATE, input=True)

    while keyboard.is_pressed('ctrl+alt'):
        frames.append(np.frombuffer(stream.read(CHUNK), dtype=np.float32))

    stream.close()
    audio_data = np.concatenate(frames) * AUDIO_SCALE

    res = pipe(audio_data, generate_kwargs={"task": "transcribe"}, chunk_length_s=30, batch_size=8)
    keyboard.write(res['text'].strip())


keyboard.add_hotkey('ctrl+alt', record_and_write)
print('Model is ready to work!')

# Terminate
keyboard.wait('alt+s', suppress=True)
audio.terminate()
print('Model terminated')

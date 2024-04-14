import time

import pyaudio
import wave
import os
import whisper
from pydub import AudioSegment
from threading import Thread
import sounddevice

model = whisper.load_model("base")

def send(to_send):
    print(to_send)
    os.system(f"curl \"http://127.0.0.1:5040/new_recording/{to_send}\"")
def gettext():
    str1 = ""
    while 1:
        while os.path.exists(f"audio_sequences/sequence_{gettext.counter}.wav") == 0:
            pass
        sound = AudioSegment.from_wav(f"audio_sequences/sequence_{gettext.counter}.wav")
        sound.export(f"audio_sequences/sequence_{gettext.counter}.mp3", format="mp3")
        results = model.transcribe(f"audio_sequences/sequence_{gettext.counter}.mp3", language="en", fp16=False)

        print(results["text"])
        str1 = str1 + results["text"]
        to_send = results["text"].replace(" ", "_").replace("!", "[exclamationmark]").replace(".", "[fullstop]").replace("?", "[questionmark]")

        send(to_send)

        """of = open(f"drain.txt", "a")
        of.write(str1)
        of.close()
        if os.path.exists(f"audio_sequences/sequence_{gettext.counter}.mp3"):
            os.remove(f"audio_sequences/sequence_{gettext.counter}.mp3")
        if os.path.exists(f"audio_sequences/sequence_{gettext.counter}.wav"):
            os.remove(f"audio_sequences/sequence_{gettext.counter}.wav")
        gettext.counter += 1
        """

gettext.counter = 0


thr1 = Thread(target=gettext)
thr1.start()


def record_audio(filename, duration):
    CHUNK = 1024//8
    FORMAT = pyaudio.paInt16
    CHANNELS = 1
    RATE = 44100

    p = pyaudio.PyAudio()

    stream = p.open(format=FORMAT,
                    channels=CHANNELS,
                    rate=RATE,
                    input=True,
                    frames_per_buffer=CHUNK)

    frames = []

    #print("Recording...")
    for i in range(0, int(RATE / CHUNK * duration)):
        data = stream.read(CHUNK)
        frames.append(data)

    #print("Finished recording.")

    stream.stop_stream()
    stream.close()
    p.terminate()

    wf = wave.open(filename, 'wb')
    wf.setnchannels(CHANNELS)
    wf.setsampwidth(p.get_sample_size(FORMAT))
    wf.setframerate(RATE)
    wf.writeframes(b''.join(frames))
    wf.close()


def concatenate_audio(file1, file2, output_file):
    # Load audio files
    with wave.open(file1, 'rb') as f1, wave.open(file2, 'rb') as f2:
        frames1 = f1.readframes(f1.getnframes())
        frames2 = f2.readframes(f2.getnframes())

    # Concatenate frames
    combined_frames = frames1 + frames2

    # Write the combined frames to a new file
    with wave.open(output_file, 'wb') as outf:
        outf.setnchannels(f1.getnchannels())
        outf.setsampwidth(f1.getsampwidth())
        outf.setframerate(f1.getframerate())
        outf.writeframes(combined_frames)


def main():
    sequence_duration = 10

    folder_path = "audio_sequences"  # enter path here
    for filename in os.listdir(folder_path):
        file_path = os.path.join(folder_path, filename)
        try:
            if os.path.isfile(file_path):
                os.remove(file_path)
            elif os.path.isdir(file_path):
                os.rmdir(file_path)
        except Exception as e:
            #print(f"Error deleting {file_path}: {e}")
            pass
    #print("Deletion done")

    output_dir = "audio_sequences"
    os.makedirs(output_dir, exist_ok=True)
    i = 0
    while True:
        # Record audio
        filename = os.path.join(output_dir, f"sequence_{i}.wav")
        record_audio(filename, sequence_duration)
        #print(f"Sequence {i} recorded.")

        # Concatenate the first two audio sequences

        i += 1


if __name__ == "__main__":
    main()

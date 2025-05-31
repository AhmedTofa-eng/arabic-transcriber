import os
import gradio as gr
from vosk import Model, KaldiRecognizer
import wave
import subprocess

MODEL_PATH = "vosk-model"

def convert_to_wav(audio_path):
    wav_path = audio_path.replace(".ogg", ".wav")
    subprocess.call(["ffmpeg", "-i", audio_path, "-ar", "16000", "-ac", "1", wav_path])
    return wav_path

def transcribe(audio_file):
    if not os.path.exists(MODEL_PATH):
        os.system(f"wget -c https://alphacephei.com/vosk/models/vosk-model-ar-mgb2-0.4.zip")
        os.system("unzip -o vosk-model-ar-mgb2-0.4.zip && mv vosk-model-ar-mgb2-0.4 vosk-model")

    wav_path = convert_to_wav(audio_file)
    wf = wave.open(wav_path, "rb")

    model = Model(MODEL_PATH)
    rec = KaldiRecognizer(model, wf.getframerate())
    rec.SetWords(True)

    result = ""
    while True:
        data = wf.readframes(4000)
        if len(data) == 0:
            break
        if rec.AcceptWaveform(data):
            res = rec.Result()
            result += res

    result += rec.FinalResult()
    return result

gr.Interface(fn=transcribe,
             inputs=gr.Audio(type="filepath", label="Upload Arabic Audio (.ogg)"),
             outputs="text",
             title="Arabic Speech-to-Text (Vosk)",
             description="Upload an .ogg file to transcribe spoken Arabic to text").launch()

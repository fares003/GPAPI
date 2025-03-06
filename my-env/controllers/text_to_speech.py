from TTS.api import TTS
import torch
import os

def convert_text_to_speech(sentences):
    """Converts a list of sentences into speech and saves it as output.wav"""
    TEXT = " ".join(sentences)  # Join sentences into a single string
    device = "cuda" if torch.cuda.is_available() else "cpu"

    # Load TTS model
    tts = TTS(model_name="tts_models/en/ljspeech/vits").to(device)

    # Generate speech and save to file
    output_path = "output.wav"
    tts.tts_to_file(TEXT, file_path=output_path)

    return output_path
import datetime
import gtts
import os
import pydub
import pyttsx3
import soundfile as sf
import subprocess
import textwrap
import time
import torch
import torchaudio

from typing import Literal
from transformers import SpeechT5ForTextToSpeech, SpeechT5Processor, SpeechT5HifiGan

def text_to_speech_1(text: str) -> None:
    start = datetime.datetime.now()
    engine = pyttsx3.init()
    engine.save_to_file(text, "output.wav")
    engine.runAndWait()
    finish = datetime.datetime.now()
    print(f"Время: {str(finish - start)}")

def text_to_speech_2(text: str) -> None:
    start = datetime.datetime.now()
    model_name = "arevin42/speecht5_finetuned_russian-lang-dataset"
    processor = SpeechT5Processor.from_pretrained(model_name)
    model = SpeechT5ForTextToSpeech.from_pretrained(model_name)
    vocoder = SpeechT5HifiGan.from_pretrained("microsoft/speecht5_hifigan")
    speaker_embeddings = torch.randn((1, 512))
    inputs = processor(text=text, return_tensors="pt")
    with torch.no_grad():
        speech = model.generate_speech(
            input_ids=inputs["input_ids"],
            speaker_embeddings=speaker_embeddings,
            vocoder=vocoder
        )
    sf.write("output.wav", speech.numpy(), samplerate=16000)
    finish = datetime.datetime.now()
    print(f"Время: {str(finish - start)}")

def text_to_speech_3(text: str) -> None:
    start = datetime.datetime.now()
    model_name = "snakers4/silero-models"
    device = torch.device("cpu")
    model, example_texts = torch.hub.load(
        repo_or_dir=model_name,
        model="silero_tts",
        language="ru",
        speaker="baya_v2"
    )
    sample_rate = 7500
    chunks = textwrap.wrap(
        text=text,
        width=100,
        break_long_words=False,
        break_on_hyphens=False
    )
    full_audio = []
    for chunk in chunks:
        audio_chunk = model.apply_tts(chunk, sample_rate)
        full_audio.extend(audio_chunk[0])
    audio_tensor = torch.tensor(full_audio).unsqueeze(0)
    torchaudio.save("silero_output.wav", audio_tensor, sample_rate)
    finish = datetime.datetime.now()
    print(f"Время: {str(finish - start)}")

def text_to_speech_4(text: str) -> None:
    start = datetime.datetime.now()
    tts = gtts.gTTS(text=text, lang="ru")
    tts.save("output.mp3")
    audio = pydub.AudioSegment.from_file("output.mp3")
    louder_audio = audio + 10
    louder_audio.export("output_louder.mp3", format="mp3")
    os.remove("output.mp3")
    finish = datetime.datetime.now()
    print(f"Время: {str(finish - start)}")

def text_to_speech_5(
        text: str,
        voice: str = "Elena",
        output_file: str = "output.wav"
) -> None:
    start = datetime.datetime.now()
    ffmpeg_proc = subprocess.Popen([
        "ffmpeg", "-y", "-f", "pulse", "-i", "default", output_file
    ])
    time.sleep(1)
    subprocess.run(["echo", text], stdout=subprocess.PIPE)
    rhvoice_proc = subprocess.Popen(
        ["RHVoice-test", "-p", voice],
        stdin=subprocess.PIPE
    )
    rhvoice_proc.communicate(input=text.encode("utf-8"))
    time.sleep(1)
    ffmpeg_proc.terminate()
    finish = datetime.datetime.now()
    print(f"Время: {str(finish - start)}")

def text_to_speech_6(
        text: str,
        voice: Literal[
            "Artemiy",
            "Evgeniy-Rus",
            "Mikhail",
            "Pavel",
            "Seva",
            "Timofey",
            "Vitaliy",
            "Vitaliy-ng",
            "Yuriy",
        ],
        audio_file_path: str
) -> None:
    subprocess.run(
        [
            "RHVoice-test",
            "-p", voice,
            "-o", audio_file_path,
        ],
        input=text.encode("utf-8")
    )

if __name__ == "__main__":
    text = """«Мой дядя самых честных правил,
Когда не в шутку занемог,
Он уважать себя заставил
И лучше выдумать не мог.
Его пример другим наука;
Но, боже мой, какая скука
С больным сидеть и день и ночь,
Не отходя ни шагу прочь!
Какое низкое коварство
Полуживого забавлять,
Ему подушки поправлять,
Печально подносить лекарство,
Вздыхать и думать про себя:
Когда же черт возьмет тебя!»

Так думал молодой повеса,
Летя в пыли на почтовых,
Всевышней волею Зевеса
Наследник всех своих родных.
Друзья Людмилы и Руслана!
С героем моего романа
Без предисловий, сей же час
Позвольте познакомить вас:
Онегин, добрый мой приятель,
Родился на брегах Невы,
Где, может быть, родились вы
Или блистали, мой читатель;
Там некогда гулял и я:
Но вреден север для меня."""
    # text_to_speech_1(text)
    # text_to_speech_2(text)
    # text_to_speech_4(text, voice="Elena", output_file="speech.wav")
    voices = [
        # "Anna",
        "Artemiy",
        # "Elena",
        "Evgeniy-Rus",
        "Mikhail",
        "Pavel",
        "Seva",
        "Timofey",
        "Vitaliy",
        "Vitaliy-ng",
        "Yuriy",
    ]
    # for voice in voices:
    #     text_to_speech_6(text, voice, f"{voice}.wav")
    # a = torch.Tensor()
    # b = torch.Tensor([1, 2, 3])
    # c = torch.cat((a, b))
    # print(c)
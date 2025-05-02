import pyttsx3
import torch
from transformers import SpeechT5ForTextToSpeech, SpeechT5Processor, SpeechT5HifiGan
import torchaudio
import soundfile as sf
import datetime
import textwrap


def text_to_speech_1():
    start = datetime.datetime.now()
    engine = pyttsx3.init()
    text = "Привет! Добро пожаловать в мир Python."
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
    # engine.say(text)
    # engine.save_to_file(text, 'output.wav')
    voices = engine.getProperty('voices')
    print(voices[0].id, end='\n\n\n')
    print(voices[1].id)
    # for voice in voices:
    #     engine.setProperty('voice', voice.id)
    #     engine.say('Мой дядя самых честных правил.')
    engine.runAndWait()
    finish = datetime.datetime.now()
    print(f"Время:{str(finish - start)}")


def text_to_speech_2():
    processor = SpeechT5Processor.from_pretrained("arevin42/speecht5_finetuned_russian-lang-dataset")
    model = SpeechT5ForTextToSpeech.from_pretrained("arevin42/speecht5_finetuned_russian-lang-dataset")
    vocoder = SpeechT5HifiGan.from_pretrained("microsoft/speecht5_hifigan")
    speaker_embeddings = torch.randn((1, 512))
    text = "Привет, мир! Это пример синтеза речи на русском языке."
    inputs = processor(text=text, return_tensors="pt")
    with torch.no_grad():
        speech = model.generate_speech(inputs["input_ids"], speaker_embeddings, vocoder=vocoder)
    sf.write("output.wav", speech.numpy(), samplerate=16000)
    print("Аудио сохранено в output.wav")


def text_to_speech_3():
    start = datetime.datetime.now()
    model_name = "snakers4/silero-models"
    device = torch.device('cpu')
    model, example_texts = torch.hub.load(
        repo_or_dir=model_name,
        model='silero_tts',
        language='ru',
        speaker='baya_v2'
    )
    # available_speakers = model.speakers
    sample_rate = 7500
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
Когда же черт возьмет тебя!»"""

    audio = model.apply_tts(text, sample_rate)
    print(1111111, type(audio[0]))
    audio_tensor = torch.tensor(audio[0]).unsqueeze(0)
    torchaudio.save('silero_output.wav', audio_tensor, sample_rate)
    print("Аудио сохранено как silero_output.wav")
    finish = datetime.datetime.now()
    print(f"Модель: {model_name}")
    print(f"Время:{str(finish - start)}")


def text_to_speech_3():
    start = datetime.datetime.now()

    # Загрузка модели
    model_name = "snakers4/silero-models"
    device = torch.device('cpu')
    model, example_texts = torch.hub.load(
        repo_or_dir=model_name,
        model='silero_tts',
        language='ru',
        speaker='baya_v2'
    )

    sample_rate = 7500  # Лучше оставить стандартный sample_rate, например 48000

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

    chunks = textwrap.wrap(text, width=100, break_long_words=False, break_on_hyphens=False)
    full_audio = []
    for chunk in chunks:
        audio_chunk = model.apply_tts(chunk, sample_rate)
        full_audio.extend(audio_chunk[0])
    audio_tensor = torch.tensor(full_audio).unsqueeze(0)
    torchaudio.save('silero_output.wav', audio_tensor, sample_rate)
    finish = datetime.datetime.now()
    print(f"Модель: {model_name}")
    print(f"Время: {str(finish - start)}")




text_to_speech_1()
# a = torch.Tensor()
# b = torch.Tensor([1, 2, 3])
# c = torch.cat((a, b))
# print(c)
import os
from typing import Literal
from transformers import MarianMTModel, MarianTokenizer

from app.core.config import settings

def translate_text(
        target_language: Literal["en", "ru"],
        text: str,
) -> str:
    if target_language == "en":
        # model_name = "Helsinki-NLP/opus-mt-ru-en"
        model_name = "Helsinki-ru-en"
    elif target_language == "ru":
        # model_name = "Helsinki-NLP/opus-mt-en-ru"
        model_name = "Helsinki-en-ru"
    else:
        raise ValueError("Unsupported language")
    model_path = os.path.join(settings.lm_folder, model_name)
    tokenizer = MarianTokenizer.from_pretrained(model_path)
    model = MarianMTModel.from_pretrained(model_path)
    tokens = tokenizer(text, return_tensors="pt", padding=True)
    translated = model.generate(**tokens)
    translated_text = tokenizer.decode(translated[0], skip_special_tokens=True)
    return translated_text

# def translate_from_en_to_ru(prompt: str) -> str:
#     model_name = "Helsinki-NLP/opus-mt-en-ru"
#     tokenizer = MarianTokenizer.from_pretrained(model_name)
#     model = MarianMTModel.from_pretrained(model_name)
#     tokens = tokenizer(prompt, return_tensors="pt", padding=True)
#     translated = model.generate(**tokens)
#     translated_text = tokenizer.decode(translated[0], skip_special_tokens=True)
#     return translated_text

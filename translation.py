from typing import Literal
from transformers import MarianMTModel, MarianTokenizer

def translate_text(target_language: Literal["en", "ru"], text: str) -> str:
    if target_language == "en":
        model_name = "Helsinki-NLP/opus-mt-ru-en"
    elif target_language == "ru":
        model_name = "Helsinki-NLP/opus-mt-en-ru"
    else:
        raise ValueError("Unsupported language")
    tokenizer = MarianTokenizer.from_pretrained(model_name)
    model = MarianMTModel.from_pretrained(model_name)
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

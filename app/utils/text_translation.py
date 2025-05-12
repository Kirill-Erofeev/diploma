import os
from typing import Literal
from transformers import MarianMTModel, MarianTokenizer
from transformers import M2M100ForConditionalGeneration, M2M100Tokenizer

# from app.core.config import settings

def translate_text(
        target_language: Literal["en", "ru"],
        text: str,
) -> str:
    if target_language == "en":
        model_name = "Helsinki-NLP/opus-mt-ru-en"
        model_name = "Helsinki-ru-en"
    elif target_language == "ru":
        model_name = "Helsinki-NLP/opus-mt-en-ru"
        model_name = "Helsinki-en-ru"
    else:
        raise ValueError("Unsupported language")
    tokenizer = MarianTokenizer.from_pretrained(model_name)
    model = MarianMTModel.from_pretrained(model_name)
    tokens = tokenizer(text, return_tensors="pt", padding=True)
    translated = model.generate(**tokens)
    translated_text = tokenizer.decode(translated[0], skip_special_tokens=True)
    return translated_text

def translate_text_2(
        target_language: Literal["en", "ru"],
        text: str,
) -> str:
    path = r"C:\Users\user\Desktop\Институт\Диплом\fastapi\app\lm_models\facebookm2-m100_418M"
    model = M2M100ForConditionalGeneration.from_pretrained(pretrained_model_name_or_path=path)
    tokenizer = M2M100Tokenizer.from_pretrained(pretrained_model_name_or_path=path)
    # model = M2M100ForConditionalGeneration.from_pretrained("facebook/m2m100_418M")
    # tokenizer = M2M100Tokenizer.from_pretrained("facebook/m2m100_418M")
    if target_language == "en":
        tokenizer.src_lang = "en"
    elif target_language == "ru":
        tokenizer.src_lang = "ru"
    else:
        raise ValueError("Unsupported language")
    # tokenizer.src_lang = "ru"
    encoded = tokenizer("Пример текста для перевода.", return_tensors="pt")
    generated = model.generate(**encoded, forced_bos_token_id=tokenizer.get_lang_id("en"))
    print(tokenizer.batch_decode(generated, skip_special_tokens=True))

if __name__ == "__main__":
    print(translate_text(target_language="en", text="Привет"))
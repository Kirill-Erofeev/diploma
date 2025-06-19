import razdel

from starlette.concurrency import run_in_threadpool
from typing import Literal
from transformers import M2M100ForConditionalGeneration, M2M100Tokenizer

from backend.core import model_registry

async def translate_text(
        target_language: Literal["en", "ru"],
        text: str,
) -> str:
    if target_language == "en":
        tokenizer = model_registry.ru_en_tokenizer
        model = model_registry.ru_en_model
    elif target_language == "ru":
        tokenizer = model_registry.en_ru_tokenizer
        model = model_registry.en_ru_model
    else:
        raise ValueError("Unsupported language")
    sentences = [s.text for s in razdel.sentenize(text)]
    translated_sentences = []
    for sentence in sentences:
        tokens = tokenizer(sentence, return_tensors="pt", padding=True, truncation=True)
        translated = await run_in_threadpool(model.generate, **tokens)
        translated_text = tokenizer.decode(translated[0], skip_special_tokens=True)
        translated_sentences.append(translated_text)
    return " ".join(translated_sentences)

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
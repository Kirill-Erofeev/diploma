from faster_whisper import WhisperModel
from transformers import AutoModelForCausalLM, AutoTokenizer, MarianTokenizer, MarianMTModel
from typing import Optional

whisper_model: Optional[WhisperModel] = None
ru_en_tokenizer: Optional[MarianTokenizer] = None
ru_en_model: Optional[MarianMTModel] = None
en_ru_tokenizer: Optional[MarianTokenizer] = None
en_ru_model: Optional[MarianMTModel] = None
small_doge_tokenizer: Optional[AutoTokenizer] = None
small_doge_model: Optional[AutoModelForCausalLM] = None

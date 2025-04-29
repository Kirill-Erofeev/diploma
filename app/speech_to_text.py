import torch
import whisper
import datetime
import warnings
from transformers import AutoModelForSpeechSeq2Seq, AutoProcessor, pipeline
from datasets import load_dataset
from faster_whisper import WhisperModel
from transformers import AutoModelForCausalLM, AutoTokenizer
from dotenv import load_dotenv
import os


def audio_to_text(file_path: str, LM_FOLDER: str) -> str:
    # model_name = "deepdml/faster-whisper-large-v3-turbo-ct2"
    model_name = "Whisper"
    model_path = os.path.join(LM_FOLDER, model_name)
    model = WhisperModel(model_path, compute_type="int8", device="cpu")
    segments, info = model.transcribe(file_path)
    transcribed_text = ""
    for segment in segments:
        transcribed_text += segment.text + " "
    return transcribed_text

def audio_to_text_3(file_path: str = "audio.wav") -> str:
    model = whisper.load_model("medium")
    audio = whisper.load_audio(file_path)
    audio = whisper.pad_or_trim(audio)
    mel = whisper.log_mel_spectrogram(audio).to(model.device)
    options = whisper.DecodingOptions(fp16=False)
    result = whisper.decode(model, mel, options)
    transcribed_text = result.text
    return transcribed_text


def audio_to_text_2(file_path: str, model_id: str) -> None:
    start = datetime.datetime.now()
    device = "cuda:0" if torch.cuda.is_available() else "cpu"
    torch_dtype = torch.float16 if torch.cuda.is_available() else torch.float32
    model = AutoModelForSpeechSeq2Seq.from_pretrained(
        model_id, torch_dtype=torch_dtype, low_cpu_mem_usage=True, use_safetensors=True
    )
    model.to(device)
    processor = AutoProcessor.from_pretrained(model_id)
    pipe = pipeline(
        "automatic-speech-recognition",
        model=model,
        tokenizer=processor.tokenizer,
        feature_extractor=processor.feature_extractor,
        torch_dtype=torch_dtype,
        device=device,
    )
    # dataset = load_dataset("distil-whisper/librispeech_long", "clean", split="validation")
    # sample = dataset[0]["audio"]
    transcribed_text = pipe(file_path)["text"]
    finish = datetime.datetime.now()
    print(f"Модель: {model_id}")
    print(f"Текст: {transcribed_text}")
    print(f"Время:{str(finish - start)}")
    print(f"{'-' * 30}")
    
    
if __name__ == "__main__":
    warnings.filterwarnings("ignore")
    file_path = "audio1.wav"
    models_id = [
        # "openai/whisper-large-v3-turbo",
        # "erax-ai/EraX-WoW-Turbo-V1.1",
        # "keeve101/whisper-large-v3-turbo-cv-unified-splits-LoRA-finetuned-unified", #Not working
        # "mozilla-ai/whisper-large-v3-turbo-bn", #Not working
        # "dvislobokov/faster-whisper-large-v3-turbo-russian", #Not working
        # "onnx-community/lite-whisper-large-v3-turbo-fast-ONNX", #Not working
    ]
    # for model_id in models_id:
    #     audio_to_text_2(file_path, model_id)
        
    audio_to_text_3(file_path)





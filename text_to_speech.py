import whisper

file_path = "audio.wav"
duration = 10

def audio_to_text(file_path: str="audio.wav") -> str:
    model = whisper.load_model("medium")
    audio = whisper.load_audio(file_path)
    audio = whisper.pad_or_trim(audio)
    mel = whisper.log_mel_spectrogram(audio).to(model.device)
    _, probs = model.detect_language(mel)
    options = whisper.DecodingOptions(fp16=False)
    result = whisper.decode(model, mel, options)
    transcribed_text = result.text
    return transcribed_text

# transcribed_text = audio_to_text(file_path)
# print(transcribed_text)
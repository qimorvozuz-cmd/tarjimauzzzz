import asyncio
import speech_recognition as sr
from pydub import AudioSegment

async def transcribe(path: str, language: str | None = None) -> str:
    def run():
        wav = f"{path}.wav"
        AudioSegment.from_file(path).export(wav, format="wav")
        recognizer = sr.Recognizer()
        with sr.AudioFile(wav) as source:
            audio = recognizer.record(source)
        code = {"uz":"uz-UZ", "ru":"ru-RU", "en":"en-US", "tr":"tr-TR", "kk":"kk-KZ", "tg":"tg-TJ"}.get(language or "", "uz-UZ")
        return recognizer.recognize_google(audio, language=code)
    return await asyncio.to_thread(run)


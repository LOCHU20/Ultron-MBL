from __future__ import annotations

from dataclasses import dataclass


@dataclass
class VoiceResult:
    text: str
    error: str | None = None


class VoiceEngine:
    def __init__(self, tts_enabled: bool = True, stt_enabled: bool = True) -> None:
        self.tts_enabled = tts_enabled
        self.stt_enabled = stt_enabled
        self._tts = None

        if self.tts_enabled:
            try:
                import pyttsx3

                self._tts = pyttsx3.init()
                self._tts.setProperty("rate", 175)
            except Exception:
                self._tts = None

    def speak(self, text: str) -> None:
        if not self.tts_enabled or not text or not self._tts:
            return
        self._tts.say(text)
        self._tts.runAndWait()

    def listen_once(self, timeout: int = 5, phrase_time_limit: int = 12) -> VoiceResult:
        if not self.stt_enabled:
            return VoiceResult(text="", error="Speech-to-text disabled.")

        try:
            import speech_recognition as sr
        except Exception:
            return VoiceResult(text="", error="speech_recognition package not installed.")

        recognizer = sr.Recognizer()
        try:
            with sr.Microphone() as source:
                recognizer.adjust_for_ambient_noise(source, duration=0.6)
                audio = recognizer.listen(source, timeout=timeout, phrase_time_limit=phrase_time_limit)
            text = recognizer.recognize_google(audio)
            return VoiceResult(text=text)
        except Exception as exc:  # noqa: BLE001
            return VoiceResult(text="", error=str(exc))

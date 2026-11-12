from gnani.tts import GnaniTTSClient

from app.core.config import get_settings


def synthesize(text: str, voice: str | None = None, language: str = "en-IN") -> bytes:
    settings = get_settings()
    key = settings.gnani_api_key.get_secret_value() if settings.gnani_api_key else None
    if not key:
        raise RuntimeError("GNANI_API_KEY is not configured")
    client = GnaniTTSClient(api_key=key, base_url=settings.gnani_base_url)
    audio = client.synthesize(
        text=text,
        voice=voice or settings.gnani_tts_voice,
        model=settings.gnani_tts_model,
        language=language,
    )
    if isinstance(audio, (bytes, bytearray)):
        return bytes(audio)
    # some clients return an object with .audio or .content
    for attr in ("audio", "content", "data", "bytes"):
        val = getattr(audio, attr, None)
        if isinstance(val, (bytes, bytearray)):
            return bytes(val)
    raise RuntimeError("Unexpected TTS response type")

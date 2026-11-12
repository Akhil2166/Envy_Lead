from pathlib import Path

from gnani.stt import GnaniSTTClient
from gnani.stt._prisma import PRISMA_V3_MODEL

from app.core.config import get_settings


def transcribe_bytes(audio_bytes: bytes, filename: str, language: str = "indic-auto") -> dict:
    settings = get_settings()
    key = settings.gnani_api_key.get_secret_value() if settings.gnani_api_key else None
    if not key:
        raise RuntimeError("GNANI_API_KEY is not configured")
    client = GnaniSTTClient(api_key=key, base_url=settings.gnani_base_url)
    result = client.transcribe_bytes(
        audio_bytes=audio_bytes,
        filename=filename,
        language_code=language,
        model=settings.gnani_stt_model,
    )
    # normalize
    text = getattr(result, "text", None) or getattr(result, "transcript", None) or str(result)
    return {"text": text, "language": language, "request_id": getattr(result, "request_id", None)}

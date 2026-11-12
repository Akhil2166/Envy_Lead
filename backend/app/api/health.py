from fastapi import APIRouter

from app.core.config import get_settings

router = APIRouter(tags=["health"])


@router.get("/health")
def health() -> dict:
    s = get_settings()
    return {
        "status": "ok",
        "service": s.app_name,
        "version": s.app_version,
        "environment": s.environment,
        "gnani_configured": s.gnani_api_key is not None,
        "stt_model": s.gnani_stt_model,
        "tts_model": s.gnani_tts_model,
    }

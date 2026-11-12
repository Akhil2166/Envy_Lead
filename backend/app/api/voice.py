import io
from fastapi import APIRouter, File, Form, HTTPException, UploadFile
from fastapi.responses import Response

from app.services import stt as stt_service
from app.services import tts as tts_service
from app.services.extraction import extract_lead

router = APIRouter(tags=["voice"])


@router.post("/stt/transcribe")
async def transcribe(file: UploadFile = File(...), language: str = Form("indic-auto")):
    try:
        data = await file.read()
        result = stt_service.transcribe_bytes(data, file.filename or "audio.wav", language)
        text = result.get("text", "")
        extracted = extract_lead(text)
        return {"transcript": text, "language": language, "request_id": result.get("request_id"), "extracted": extracted}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/tts/synthesize")
async def synthesize(text: str = Form(...), voice: str = Form(None), language: str = Form("en-IN")):
    try:
        audio = tts_service.synthesize(text, voice, language)
        return Response(content=audio, media_type="audio/wav", headers={"Content-Disposition": 'attachment; filename="envylead-tts.wav"'})
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

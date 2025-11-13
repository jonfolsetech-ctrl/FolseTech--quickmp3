import os
import uuid
from pathlib import Path
from typing import Optional

from fastapi import FastAPI, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, JSONResponse
from pydub import AudioSegment

# --------------------
# Config
# --------------------
BASE_DIR = Path(__file__).parent
MEDIA_DIR = BASE_DIR / "generated"
MEDIA_DIR.mkdir(exist_ok=True)

app = FastAPI(
    title="QuickMP3 by FolseTech AI Solutions",
    description="Lyrics-to-song generator backend demo for FolseTech AI Solutions.",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # For dev; lock down in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --------------------
# Helper functions (stubs for real AI calls)
# --------------------


def generate_instrumental(lyrics: str, genre: str) -> Path:
    """
    Stub: In a real app, call Suno/Udio/etc here.
    For now, generate a 10-second silent track as placeholder.
    """
    out_path = MEDIA_DIR / f"instrumental_{uuid.uuid4().hex}.wav"
    silence = AudioSegment.silent(duration=10000)  # 10 seconds of silence
    silence.export(out_path, format="wav")
    return out_path


def synthesize_vocals(lyrics: str, voice_sample_path: Optional[Path], genre: str) -> Path:
    """
    Stub: In a real app, call ElevenLabs/RVC/etc here to synthesize vocals.
    For now, generate a 10-second silent vocal track as placeholder.
    """
    out_path = MEDIA_DIR / f"vocals_{uuid.uuid4().hex}.wav"
    silence = AudioSegment.silent(duration=10000)  # 10 seconds of silence
    silence.export(out_path, format="wav")
    return out_path


def mix_tracks(instrumental_path: Path, vocal_path: Path) -> Path:
    """
    Very basic mixing using pydub overlay.
    """
    instrumental = AudioSegment.from_file(instrumental_path)
    vocals = AudioSegment.from_file(vocal_path)

    # Simple overlay (vocals -3 dB)
    vocals = vocals - 3
    mixed = instrumental.overlay(vocals)

    out_path = MEDIA_DIR / f"song_{uuid.uuid4().hex}.mp3"
    mixed.export(out_path, format="mp3", bitrate="192k")
    return out_path


# --------------------
# API Routes
# --------------------


@app.post("/api/generate-song")
async def generate_song(
    lyrics: str = Form(...),
    genre: str = Form(...),
    voice_sample: Optional[UploadFile] = File(None),
):
    """
    Main endpoint: accepts lyrics, genre, and optional voice sample.
    Returns URL + metadata for the generated song.
    """
    try:
        voice_sample_path = None
        if voice_sample is not None:
            ext = os.path.splitext(voice_sample.filename or "")[1] or ".wav"
            voice_sample_path = MEDIA_DIR / f"voice_{uuid.uuid4().hex}{ext}"
            with open(voice_sample_path, "wb") as f:
                f.write(await voice_sample.read())

        instrumental_path = generate_instrumental(lyrics, genre)
        vocal_path = synthesize_vocals(lyrics, voice_sample_path, genre)
        song_path = mix_tracks(instrumental_path, vocal_path)

        file_name = song_path.name

        return {
            "success": True,
            "file_name": file_name,
            "song_url": f"/media/{file_name}",
            "metadata": {
                "genre": genre,
                "duration_seconds": 10,
                "id": uuid.uuid4().hex,
                "brand": "FolseTech AI Solutions",
            },
        }
    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={"success": False, "error": str(e)},
        )


@app.get("/media/{file_name}")
def get_media(file_name: str):
    """
    Serve generated audio files.
    """
    file_path = MEDIA_DIR / file_name
    if not file_path.exists():
        return JSONResponse(status_code=404, content={"detail": "File not found"})
    return FileResponse(file_path, media_type="audio/mpeg", filename=file_name)


@app.get("/health")
def health():
    return {"status": "ok", "brand": "FolseTech AI Solutions", "app": "QuickMP3"}

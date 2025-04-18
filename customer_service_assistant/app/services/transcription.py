# app/services/transcription.py

import os
import tempfile

from app.services.speaker_id import (
    align_transcript_with_speakers,
    detect_roles_by_line_keywords,
    simple_speaker_diarization,
    transcribe_audio,
)
from app.utils.logging_server import setup_logger

logger = setup_logger("Transcription")

async def transcribe_audio_and_identify_speakers(file_bytes: bytes, filename: str):
    try:
        with tempfile.NamedTemporaryFile(delete=False, suffix=os.path.splitext(filename)[-1]) as temp_file:
            temp_file.write(file_bytes)
            temp_file_path = temp_file.name

        transcript = transcribe_audio(temp_file_path)
        speakers = simple_speaker_diarization(temp_file_path)
        aligned = align_transcript_with_speakers(transcript, speakers)
        aligned = detect_roles_by_line_keywords(aligned)

        logger.info(f"Aligned Transcript with Roles: {aligned}")
        os.remove(temp_file_path)

        return {
            "transcript": aligned,
            "raw_transcript": transcript,
            "speaker_segments": speakers,
        }

    except Exception as e:
        logger.exception("🔥 Exception occurred in transcription pipeline")
        return {"error": "Transcription or speaker identification failed", "details": str(e)}

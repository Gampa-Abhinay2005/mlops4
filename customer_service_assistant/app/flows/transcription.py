from prefect import flow, task

from app.services.transcription import transcribe_audio_and_identify_speakers


@task
async def transcribe_text(file_bytes: bytes, filename: str):
    """Prefect task to transcribe the audio from raw bytes.
    """
    return await transcribe_audio_and_identify_speakers(file_bytes, filename)

@flow
async def transcribe_flow(file_bytes: bytes, filename: str):
    """Prefect flow to manage the transcription process.
    """
    return await transcribe_text(file_bytes, filename)

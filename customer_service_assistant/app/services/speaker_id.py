from faster_whisper import WhisperModel
import os

# Load Whisper Model (faster)
whisper_model = WhisperModel("base", device="cuda" if os.environ.get("USE_CUDA") == "1" else "cpu")

# Instead of pyannote, we can assume a basic two-speaker segmentation method
# You can replace this with a custom method if you have any specific segmentation logic

def transcribe_audio(file_path: str):
    """
    Transcribes audio using Whisper and returns the transcript with proper timestamps.
    """
    segments, _ = whisper_model.transcribe(file_path)
    transcript = []
    for segment in segments:
        transcript.append({
            "start": float(segment.start),
            "end": float(segment.end),
            "text": segment.text.strip()
        })
    return transcript


def simple_speaker_diarization(file_path: str):
    transcript = transcribe_audio(file_path)
    speakers = []
    
    speaker_labels = ["Speaker 1", "Speaker 2"]
    for i, segment in enumerate(transcript):
        speaker = speaker_labels[i % 2]  # Alternate speakers
        speakers.append({
            "start": segment["start"],
            "end": segment["end"],
            "speaker": speaker
        })
    
    return speakers


def align_transcript_with_speakers(transcript, speakers):
    aligned = []
    for line in transcript:
        line_start = line["start"]
        speaker_label = next(
            (sp["speaker"] for sp in speakers if sp["start"] <= line_start <= sp["end"]),
            "Unknown"
        )
        aligned.append({
            "speaker": speaker_label,
            "text": line["text"],
            "start": line["start"],
            "end": line["end"]
        })
    return aligned

def detect_roles_from_keywords(aligned_transcript):
    agent_keywords = [
        "please hold", "let me check", "i can help", "how may i assist",
        "thank you for reaching out", "we apologize", "i will escalate",
        "as per our policy", "i understand your concern", "can you provide",
        "i’ll be happy to", "is there anything else"
    ]
    agent_keywords = [kw.lower() for kw in agent_keywords]

    speaker_texts = {}
    for entry in aligned_transcript:
        speaker = entry["speaker"]
        speaker_texts.setdefault(speaker, "")
        speaker_texts[speaker] += " " + entry["text"].lower()

    speaker_scores = {
        speaker: sum(kw in speaker_texts[speaker] for kw in agent_keywords)
        for speaker in speaker_texts
    }

    sorted_speakers = sorted(speaker_scores.items(), key=lambda x: x[1], reverse=True)

    if len(sorted_speakers) < 2:
        return aligned_transcript  # Not enough data to decide

    agent_speaker = sorted_speakers[0][0]
    customer_speaker = sorted_speakers[1][0]

    updated = []
    for entry in aligned_transcript:
        role = "Agent" if entry["speaker"] == agent_speaker else "Customer"
        updated.append({
            "speaker": role,
            "text": entry["text"],
            "start": entry["start"],
            "end": entry["end"]
        })

    return updated
def detect_roles_by_line_keywords(aligned_transcript):
    """
    Detects roles (Agent or Customer) for each line based on presence of role-specific keywords.
    """
    agent_keywords = [
        "please hold", "let me check", "i can help", "how may i assist",
        "thank you for reaching out", "we apologize", "i will escalate",
        "as per our policy", "i understand your concern", "can you provide",
        "i’ll be happy to", "is there anything else"
    ]
    customer_keywords = [
        "i need", "i want", "i have a problem", "help me", "my order",
        "issue with", "i didn’t receive", "can you fix", "i’m not happy", "i want a refund"
    ]

    agent_keywords = [kw.lower() for kw in agent_keywords]
    customer_keywords = [kw.lower() for kw in customer_keywords]

    def score_text(text, keywords):
        return sum(kw in text for kw in keywords)

    updated_transcript = []
    for entry in aligned_transcript:
        text = entry["text"].lower()
        agent_score = score_text(text, agent_keywords)
        customer_score = score_text(text, customer_keywords)

        if agent_score > customer_score:
            role = "Agent"
        elif customer_score > agent_score:
            role = "Customer"
        else:
            role = "Customer"  # default fallback if no strong match

        updated_transcript.append({
            "speaker": role,
            "text": entry["text"],
            "start": entry["start"],
            "end": entry["end"]
        })

    return updated_transcript


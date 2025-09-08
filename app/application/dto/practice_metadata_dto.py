from dataclasses import dataclass

@dataclass
class PracticeMetadataDTO:
    id: int
    video_in_server: str
    video_in_local: str
    report: str
    video_done: bool
    audio_done: bool
from dataclasses import dataclass

@dataclass
class PracticeDTO:
    date: str
    time: str
    scale: str
    scale_type: str
    duration: int
    bpm: int
    figure: int
    octaves: int
    uid: str
    practice_id: int
    video_local_route: str
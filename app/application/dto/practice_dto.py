from dataclasses import dataclass

@dataclass
class PracticeDTO:
    date: str
    time: str
    duration: int
    uid: int
    practice_id: int
    video_route: str
    scale: str
    scale_type: str
    reps: str
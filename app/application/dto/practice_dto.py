from dataclasses import dataclass

@dataclass
class PracticeDTO:
    date: str
    time: str
    duration: int
    uid: int
    practice_id: int
    video_route: str
    id_scale: int
    scale: str
    reps: str
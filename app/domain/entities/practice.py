from dataclasses import dataclass
from typing import Optional

@dataclass
class Practice:
    date: str
    time: str
    scale: str
    scale_type: str
    num_postural_errors: int
    num_musical_errors: int
    duration: int
    bpm: int
    figure: float
    octaves: int
    total_notes_played: int
    id_student: str
    id_scale: Optional[int] = None
    id: Optional[int] = None
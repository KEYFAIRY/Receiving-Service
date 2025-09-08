from dataclasses import dataclass
from typing import Optional

@dataclass
class Practice:
    date: str
    time: str
    num_postural_errors: int
    num_musical_errors: int
    duration: int
    id_student: str
    id_scale: int
    id: Optional[int] = None
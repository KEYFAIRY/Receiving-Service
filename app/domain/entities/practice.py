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
    scale: str
    scale_type: str
    id_scale: Optional[int] = None
    id: Optional[int] = None
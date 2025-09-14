from dataclasses import dataclass
from typing import Optional

@dataclass
class Scale:
    name: str
    scale_type: str
    id: Optional[int] = None
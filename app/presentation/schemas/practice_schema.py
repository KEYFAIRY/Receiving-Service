from pydantic import BaseModel, Field

class PracticeRequest(BaseModel):
    """Request with information about a practice"""

    date: str = Field(..., description="Date of the practice in YYYY-MM-DD format", example="2025-09-07")
    time: str = Field(..., description="Time of the practice in HH:MM:SS format", example="15:30:00")
    duration: int = Field(..., description="Duration of the practice in seconds", example=3600)
    uid: str = Field(..., description="User ID who performed the practice", example="UID12345")
    video_local_route: str = Field(..., description="Path or URL to the practice video in local storage", example="/videos/practice_202.mp4")
    scale: str = Field(..., description="Name of the musical scale practiced", example="C Major")
    scale_type: str = Field(..., description="Type of the musical scale", example="Major")
    reps: int = Field(..., description="Number of repetitions performed", example=3)
    bpm: int = Field(..., description="Beats per minute during the practice", example=120)

    class Config:
        schema_extra = {
            "example": {
                "date": "2025-09-07",
                "time": "15:30:00",
                "duration": 3600,
                "uid": "UID12345",
                "video_local_route": "/videos/practice_202.mp4",
                "scale": "C Major",
                "scale_type": "Major",
                "reps": 3,
                "bpm": 120
            }
        }

class PracticeResponse(BaseModel):
    """Response with information about a registered practice"""
    practice_id: int = Field(..., description="ID of the registered practice", example=101)
    date: str = Field(..., description="Date of the practice in YYYY-MM-DD format", example="2025-09-07")
    time: str = Field(..., description="Time of the practice in HH:MM:SS format", example="15:30:00")
    duration: int = Field(..., description="Duration of the practice in seconds", example=3600)
    scale: str = Field(..., description="Name of the musical scale practiced", example="C Major")
    scale_type: str = Field(..., description="Type of the musical scale", example="Major")
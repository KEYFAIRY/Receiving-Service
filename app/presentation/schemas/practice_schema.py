from pydantic import BaseModel, Field


class PracticeRequest(BaseModel):
    """Request with information about a practice"""

    date: str = Field(..., description="Date of the practice in YYYY-MM-DD format", example="2025-09-07")
    time: str = Field(..., description="Time of the practice in HH:MM:SS format", example="15:30:00")
    duration: int = Field(..., description="Duration of the practice in seconds", example=3600)
    uid: str = Field(..., description="User ID who performed the practice", example="UID12345")
    practice_id: int = Field(..., description="Unique ID of the practice", example=0)
    video_route: str = Field(..., description="Path or URL to the practice video", example="/videos/practice_202.mp4")
    id_scale: int = Field(..., description="ID of the musical scale practiced", example=1)
    scale: str = Field(..., description="Name of the musical scale practiced", example="C Major")
    reps: int = Field(..., description="Number of repetitions performed", example=3)

    class Config:
        schema_extra = {
            "example": {
                "date": "2025-09-07",
                "time": "15:30:00",
                "duration": 3600,
                "uid": "UID12345",
                "practice_id": 0,
                "video_route": "/videos/practice_202.mp4",
                "id_scale": 1,
                "scale": "C Major",
                "reps": 3
            }
        }

class PracticeResponse(BaseModel):
    """Response with information about a registered practice"""
    
    message: str = Field(..., description="Response message", example="Practice registered successfully")
    
    class Config:
        schema_extra = {
            "example": {
                "message": "Practice registered successfully"
            }
        }
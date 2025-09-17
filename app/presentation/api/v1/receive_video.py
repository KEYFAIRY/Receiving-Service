import logging
import json
from fastapi import APIRouter, Depends, status, UploadFile, File, Form
from pydantic import ValidationError

from app.application.dto.practice_dto import PracticeDTO
from app.application.use_cases.register_practice_use_case import RegisterPracticeUseCase
from app.presentation.api.v1.dependencies import register_practice_use_case_dependency
from app.presentation.schemas.practice_schema import PracticeRequest, PracticeResponse
from app.presentation.schemas.common_schema import StandardResponse

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/practice", tags=["Practices"])

@router.post(
    "/register",
    response_model=StandardResponse[PracticeResponse],
    status_code=status.HTTP_201_CREATED,
    summary="Register a practice",
    description="Register a practice with its metadata (PracticeRequest) and video"
)
async def register_practice(
    video: UploadFile = File(..., description="Video file of the practice"),
    practice_data: str = Form(..., description="JSON string with practice metadata"),
    use_case: RegisterPracticeUseCase = Depends(register_practice_use_case_dependency)
):
    """
    Endpoint that receives a practice video and its metadata, then registers the practice.
    """
    logger.info("Registering practice...")

    try:
        practice_dict = json.loads(practice_data)
        practice_request = PracticeRequest(**practice_dict)
    except (json.JSONDecodeError, ValidationError) as e:
        logger.error(f"Invalid practice_data: {e}")
        raise ValueError(f"Invalid practice_data: {e}")

    practice_dto = PracticeDTO(
        date=practice_request.date,
        time=practice_request.time,
        duration=practice_request.duration,
        uid=practice_request.uid,
        practice_id=0,  # Placeholder, actual ID to be set by the system
        video_local_route=practice_request.video_local_route,
        scale=practice_request.scale,
        scale_type=practice_request.scale_type,
        reps=practice_request.reps,
        bpm=practice_request.bpm
    )

    practice_response = await use_case.execute(practice_dto, await video.read())

    response = PracticeResponse(video_in_server=practice_response)

    logger.info(f"Practice registered successfully: UID {practice_request.uid}, Scale {practice_request.scale}, Scale Type {practice_request.scale_type}")

    return StandardResponse.success(
        data=response,
        message="Practice registered successfully"
    )

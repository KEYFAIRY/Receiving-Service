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
    practice_data: str = Form(..., description="JSON string with PracticeRequest data"),
    use_case: RegisterPracticeUseCase = Depends(register_practice_use_case_dependency)
):
    """
    Endpoint that receives a practice video and its metadata, then registers the practice.
    """
    logger.info("Registering practice...")

    # Parsear el JSON recibido como string -> PracticeRequest
    try:
        practice_dict = json.loads(practice_data)
        practice_request = PracticeRequest(**practice_dict)
        practice_dto = PracticeDTO(
            date=practice_request.date,
            time=practice_request.time,
            duration=practice_request.duration,
            uid=practice_request.uid,
            practice_id=practice_request.practice_id,
            video_route=practice_request.video_route,
            id_scale=practice_request.id_scale,
            scale=practice_request.scale,
            reps=practice_request.reps
        )
    except (ValidationError, json.JSONDecodeError) as e:
        logger.error(f"Validation error: {e}")
        return StandardResponse.internal_error(message="Invalid practice data")
    
    # Ejecutar caso de uso
    practice_response = await use_case.execute(practice_dto, await video.read())

    logger.info(f"Practice {practice_request.practice_id} registered successfully")
    
    return StandardResponse.success(
        data={"message": practice_response} ,
        message="Practice registered successfully"
    )

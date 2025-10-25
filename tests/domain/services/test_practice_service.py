import pytest

from unittest.mock import AsyncMock, MagicMock

from app.domain.entities.practice import Practice
from app.domain.entities.scale import Scale
from app.domain.services.practice_service import PracticeService
from app.domain.repositories.i_scale_repo import IScaleRepo
from app.domain.repositories.i_practice_repo import IPracticeRepo
from app.domain.repositories.i_videos_repo import IVideoRepo
from app.domain.repositories.i_metadata_repo import IMetadataRepo

@pytest.fixture
def mock_scale_repo():
    return AsyncMock(spec=IScaleRepo)

@pytest.fixture
def mock_practice_repo():
    return AsyncMock(spec=IPracticeRepo)

@pytest.fixture
def mock_metadata_repo():
    return AsyncMock(spec=IMetadataRepo)

@pytest.fixture
def mock_videos_repo():
    return AsyncMock(spec=IVideoRepo)

@pytest.fixture
def practice_service(mock_practice_repo, mock_scale_repo, mock_metadata_repo, mock_videos_repo):
    return PracticeService(
        practice_repo=mock_practice_repo,
        scale_repo=mock_scale_repo,
        metadata_repo=mock_metadata_repo,
        videos_repo=mock_videos_repo
    )

@pytest.fixture
def practice_event():
    return Practice(
        date = "2024-06-01",
        time = "10:00:00",
        scale = "C",
        scale_type = "major",
        num_postural_errors = 2,
        num_musical_errors = 3,
        duration = 300,
        bpm = 120,
        figure = 1.0,
        octaves = 2,
        total_notes_played = 29,
        id_student = "lulo123",
        id_scale = 1,
        id = 123
        )

@pytest.fixture
def scale_exist():
    return Scale(
        id = 1,
        name = "C",
        scale_type = "major"
    )

class TestPracticeService:
    
    @pytest.mark.asyncio
    async def test_practice_exists(self, practice_service, practice_event, mock_scale_repo, mock_practice_repo, scale_exist):
        #Arrange
        mock_scale_repo.get_by_name_and_type.return_value = scale_exist
        mock_practice_repo.get_by_datetime_uid_scale.return_value = practice_event

        #Act
        result = await practice_service.practice_exists(practice_event)

        #Assert
        mock_scale_repo.get_by_name_and_type.assert_awaited_once_with(practice_event.scale, practice_event.scale_type)

        assert result.id == practice_event.id
        assert result.id_scale == practice_event.id_scale

    @pytest.mark.asyncio
    async def test_practice_does_not_exist(self, practice_service, practice_event, mock_scale_repo):
        #Arrange
        mock_scale_repo.get_by_name_and_type.return_value = None

        #Act
        result = await practice_service.practice_exists(practice_event)

        #Assert
        mock_scale_repo.get_by_name_and_type.assert_awaited_once_with(practice_event.scale, practice_event.scale_type)
        assert result is None

    @pytest.mark.asyncio
    async def test_store_practice_data_with_scale(self, practice_service, practice_event, mock_scale_repo, mock_practice_repo, mock_videos_repo, mock_metadata_repo, scale_exist):
        #Arrange
        mock_scale_repo.get_by_name_and_type.return_value = scale_exist
        mock_scale_repo.create.return_value = scale_exist
        mock_practice_repo.create.return_value = practice_event
        mock_videos_repo.save.return_value = "/path/to/video.mp4"
        mock_metadata_repo.add_practice_to_user.return_value = practice_event

        video_content = b"fake_video_data"
        video_local = "/local/path/to/video.mp4"

        #Act
        result = await practice_service.store_practice_data(practice_event, video_content, video_local)

        #Assert
        mock_scale_repo.get_by_name_and_type.assert_awaited_once_with(practice_event.scale, practice_event.scale_type)

        assert result.id == practice_event.id
        assert result.video_in_server == "/path/to/video.mp4"
        assert result.video_in_local == video_local

    @pytest.mark.asyncio
    async def test_store_practice_data_without_scale(self, practice_service, practice_event, mock_scale_repo, mock_practice_repo, mock_videos_repo, mock_metadata_repo, scale_exist):
        #Arrange
        mock_scale_repo.get_by_name_and_type.return_value = None
        mock_scale_repo.create.return_value = scale_exist
        mock_practice_repo.create.return_value = practice_event
        mock_videos_repo.save.return_value = "/path/to/video.mp4"
        mock_metadata_repo.add_practice_to_user.return_value = practice_event

        video_content = b"fake_video_data"
        video_local = "/local/path/to/video.mp4"

        #Act
        result = await practice_service.store_practice_data(practice_event, video_content, video_local)

        #Assert
        mock_scale_repo.get_by_name_and_type.assert_awaited_once_with(practice_event.scale, practice_event.scale_type)

        assert result.id == practice_event.id
        assert result.video_in_server == "/path/to/video.mp4"
        assert result.video_in_local == video_local
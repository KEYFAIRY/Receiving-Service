from beanie import Document

class PracticeDocument(Document):
    id_practice: int
    video_in_server: str
    video_in_local: str
    report: str
    video_done: bool
    audio_done: bool

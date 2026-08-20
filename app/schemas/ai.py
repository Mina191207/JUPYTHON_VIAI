from typing import Optional

from app.models.schema import VideoAspect
from pydantic import BaseModel

class EstimateRequest(BaseModel):
    video_subject: str
    language: str = ""
    paragraph_number: int = 1

class GenerateScriptResponse(BaseModel):
    draft_id: int
    script: str
    prompt_tokens: int
    completion_tokens: int
    total_tokens: int
    regenerate_count: int
    regenerate_limit: int

class GenerateScriptRequest(BaseModel):
    video_subject: str
    language: str = ""
    paragraph_number: int = 1

class RegenerateScriptRequest(BaseModel):
    draft_id: int

class GenerateTermsRequest(BaseModel):
    video_subject: str
    video_script: str
    amount: int = 5
    match_script_order: bool = False


class GenerateTermsResponse(BaseModel):
    terms: list[str]
    prompt_tokens: int
    completion_tokens: int
    total_tokens: int


class GenerateSocialMetadataRequest(BaseModel):
    video_subject: str
    video_script: str


class SocialMetadata(BaseModel):
    title: str
    caption: str
    hashtags: list[str]


class GenerateSocialMetadataResponse(BaseModel):
    metadata: SocialMetadata
    prompt_tokens: int
    completion_tokens: int
    total_tokens: int


class GenerateAudioRequest(BaseModel):
    script: str
    voice_name: str
    voice_rate: float = 1.0

class GenerateAudioResponse(BaseModel):
    audio_path: str

class GenerateVideoFileResponse(BaseModel):
    video_path: str

class GenerateVideoRequest(BaseModel):
    draft_id: int
    voice_name: str = "vi-VN-HoaiMyNeural"
    voice_rate: float = 1.0
    voice_volume: float = 1.0
    video_aspect: VideoAspect = VideoAspect.portrait
    subtitle_enabled: bool = True
    bgm_type: str = "random"
    bgm_file: str = ""
    bgm_volume: float = 0.2

class GenerateVideoResponse(BaseModel):
    script: GenerateScriptResponse
    terms: GenerateTermsResponse
    metadata: GenerateSocialMetadataResponse
    audio: GenerateAudioResponse
    materials: list[str]
    video: GenerateVideoFileResponse
    video_path: str


class GenerateVideoTask(BaseModel):
    """Trạng thái của một tác vụ tạo video đang chạy nền.

    state: -1 = failed, 1 = complete, 4 = processing
    """
    task_id: str
    state: int = 0
    progress: int = 0
    result: Optional[GenerateVideoResponse] = None
    error: Optional[str] = None


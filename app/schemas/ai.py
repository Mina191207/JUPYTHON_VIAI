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

class GenerateVideoResponse(BaseModel):
    script: GenerateScriptResponse
    terms: GenerateTermsResponse
    metadata: GenerateSocialMetadataResponse
    audio: GenerateAudioResponse
    materials: list[str]
    video: GenerateVideoFileResponse
    video_path: str


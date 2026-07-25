from pydantic import BaseModel


class EstimateRequest(BaseModel):
    video_subject: str
    language: str = ""
    paragraph_number: int = 1


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
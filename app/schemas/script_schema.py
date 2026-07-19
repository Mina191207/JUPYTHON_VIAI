from pydantic import BaseModel


class GenerateScriptRequest(BaseModel):
    video_subject: str
    language: str = "en"
    paragraph_number: int = 1
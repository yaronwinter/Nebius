import structlog
from pydantic import BaseModel, HttpUrl
from typing import List


class SummarizeSuccess(BaseModel):
    summary: str
    technologies: List[str]
    structure: str


class SummarizeError(BaseModel):
    status: str = "error"
    message: str


class SummarizeRequest(BaseModel):
    github_url: HttpUrl


logger = structlog.get_logger()

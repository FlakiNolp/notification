from pydantic import BaseModel, Field
from typing import List
from datetime import datetime


class QueryModel(BaseModel):
    code: int = Field(..., ge=100, le=526)
    message: str = Field(..., min_length=1, max_length=100)
    additional: str = Field(..., min_length=1, max_length=100)


class LogModel(BaseModel):
    time: datetime
    level: str
    message: str
    source: str


class ResponseLogsModel(BaseModel):
    logs: List[LogModel]
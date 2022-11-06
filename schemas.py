from pydantic import BaseModel, Field


class QueryModel(BaseModel):
    code: int = Field(..., ge=100, le=526)
    message: str = Field(..., min_length=1, max_length=100)
    additional: str = Field(..., min_length=1, max_length=100)


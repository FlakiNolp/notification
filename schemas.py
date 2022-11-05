from pydantic import BaseModel, Field


class Query(BaseModel):
    code: int = Field(..., gt=99, lt=527, description='Code number must be from 100 to 526')
    message: str = Field(..., min_length=1, max_length=101, description='There is no message in the request')
    additional: str = Field(..., min_length=1, max_length=101, description='There is no additional in the request')


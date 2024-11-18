from pydantic import BaseModel

class SuccessResponse(BaseModel):
    detail: str
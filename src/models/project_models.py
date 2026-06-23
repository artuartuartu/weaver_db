from pydantic import BaseModel

class ProjectCreate(BaseModel):
    name: str
    user_email: str

class ProjectResponse(BaseModel):
    id: str
    name: str
    user_email: str | None = None
    updated_at: str

    model_config = {"from_attributes": True}
    
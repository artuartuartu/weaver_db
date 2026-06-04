from pydantic import BaseModel

class AuthRequest(BaseModel):
    email: str
    name: str
    provider: str
    provider_id: str

class AuthResponse(BaseModel):
    email: str
    is_vip: bool
    message: str

from pydantic import BaseModel 

class PreferenceResponse(BaseModel):
    email: bool
    push: bool

class UpdatePreferenceRequest(BaseModel):
    email: bool | None = None
    push: bool | None = None
from pydantic import BaseModel
from typing import Optional, List

class StartSessionRequest(BaseModel):
    user_id: int
    session_type: str = "discovery"

class StartSessionResponse(BaseModel):
    session_id: int
    message: str

class ImageRecognitionRequest(BaseModel):
    session_id: int
    image_id: int
    user_guess: str

class ImageRecognitionResponse(BaseModel):
    is_correct: bool
    parent_category: Optional[str] = None
    child_category: Optional[str] = None
    fun_fact: Optional[str] = None

class PreFedImage(BaseModel):
    id: int
    image_url: str

class PreFedImageList(BaseModel):
    images: List[PreFedImage]

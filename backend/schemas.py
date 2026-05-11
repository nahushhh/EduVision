from pydantic import BaseModel
from typing import Optional, List

class StartSessionRequest(BaseModel):
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

# --- Story Mode Schemas ---

class StoryClickRequest(BaseModel):
    story_id: int
    scene_id: int
    click_x_ratio: float  # Percentage of width (0.0 to 1.0)
    click_y_ratio: float  # Percentage of height (0.0 to 1.0)

class StoryClickResponse(BaseModel):
    is_correct: bool
    message: str
    detected_class: Optional[str] = None

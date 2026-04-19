import os
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from .. import models, schemas, database
from ..services.cv_model import CVModelService
from ..services.llm_fun_facts import LLMFunFactService

router = APIRouter()
cv_service = CVModelService()
llm_service = LLMFunFactService()

# Absolute path to local test images
TEST_IMAGES_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "test_images"))

# Pre-fed images for the discovery loop mapped logically
PRE_FED_IMAGES = [
    {"id": 0, "filename": "albetross.jpg"},
    {"id": 1, "filename": "camel.jpg"},
    {"id": 2, "filename": "car.jpg"},
    {"id": 3, "filename": "whale.jpg"}
]

@router.post("/start", response_model=schemas.StartSessionResponse)
def start_session(req: schemas.StartSessionRequest, db: Session = Depends(database.get_db)):
    db_session = models.Session(user_id=req.user_id, session_type=req.session_type)
    db.add(db_session)
    db.commit()
    db.refresh(db_session)
    return {"session_id": db_session.id, "message": "Session started successfully!"}

@router.get("/images", response_model=schemas.PreFedImageList)
def get_images():
    # We serve the images over HTTP from the /static endpoint configured in main.py!
    return {"images": [{"id": img["id"], "image_url": f"http://localhost:8000/static/{img['filename']}"} for img in PRE_FED_IMAGES]}

@router.post("/recognize", response_model=schemas.ImageRecognitionResponse)
def recognize_image(req: schemas.ImageRecognitionRequest, db: Session = Depends(database.get_db)):
    image = next((img for img in PRE_FED_IMAGES if img["id"] == req.image_id), None)
    if not image:
        raise HTTPException(status_code=404, detail="Image not found")
        
    # Crucial: Give the PyTorch models the actual full windows path, NOT the URL string!
    local_path = os.path.join(TEST_IMAGES_DIR, image["filename"])
        
    parent, child = cv_service.predict(local_path)
    
    guess_clean = req.user_guess.lower().strip()
    parent_clean = parent.lower().strip()
    
    # Evaluate correctness using the parent model as the ultimate judge
    is_correct = (guess_clean == parent_clean)
    
    # Pluralization check (Land Animal vs Land Animals)
    if not is_correct and guess_clean.rstrip('s') == parent_clean.rstrip('s'):
        is_correct = True
        
    if not is_correct:
         return {
             "is_correct": False
         }
         
    fact = llm_service.generate_fact(child)
    
    # Log it
    log_entry = models.ImageRecognitionLog(
        session_id=req.session_id,
        image_path=image["filename"],
        parent_category=parent,
        child_category=child
    )
    db.add(log_entry)
    db.commit()
    
    return {
        "is_correct": True,
        "parent_category": parent,
        "child_category": child,
        "fun_fact": fact
    }

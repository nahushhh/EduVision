import os
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.sql.expression import func as sql_func
from .. import models, schemas, database
from ..services.cv_model import CVModelService
from ..services.llm_fun_facts import LLMFunFactService

router = APIRouter()
cv_service = CVModelService()
llm_service = LLMFunFactService()

# Absolute path to local test images
TEST_IMAGES_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "test_images"))

# Fallback image list — used if the DB is empty or unavailable
PRE_FED_IMAGES = [
    {"id": 0, "filename": "alb 1.jpg"},
    {"id": 1, "filename": "crab3.jpg"},
    {"id": 2, "filename": "Peach0046.png"},
    {"id": 3, "filename": "pot2.jpg"},
    {"id": 4, "filename": "car1.jpg"},
]

IMAGES_PER_SESSION = 5


@router.post("/start", response_model=schemas.StartSessionResponse)
def start_session(req: schemas.StartSessionRequest, db: Session = Depends(database.get_db)):
    db_session = models.Session(session_type=req.session_type)
    db.add(db_session)
    db.commit()
    db.refresh(db_session)
    return {"session_id": db_session.id, "message": "Session started successfully!"}


@router.get("/images", response_model=schemas.PreFedImageList)
def get_images(db: Session = Depends(database.get_db)):
    # Pull IMAGES_PER_SESSION random images from the DB
    db_images = (
        db.query(models.Image)
        .order_by(sql_func.random())
        .limit(IMAGES_PER_SESSION)
        .all()
    )

    if db_images:
        return {
            "images": [
                {"id": img.id, "image_url": f"http://localhost:8000/static/{img.filename}"}
                for img in db_images
            ]
        }

    # Fallback: DB is empty — use PRE_FED_IMAGES
    print("[Discovery] DB has no images — falling back to PRE_FED_IMAGES.")
    return {
        "images": [
            {"id": img["id"], "image_url": f"http://localhost:8000/static/{img['filename']}"}
            for img in PRE_FED_IMAGES
        ]
    }


@router.post("/recognize", response_model=schemas.ImageRecognitionResponse)
def recognize_image(req: schemas.ImageRecognitionRequest, db: Session = Depends(database.get_db)):
    # First try the DB
    db_image = db.query(models.Image).filter(models.Image.id == req.image_id).first()

    if db_image:
        filename = db_image.filename
    else:
        # Fallback: look in PRE_FED_IMAGES
        fallback = next((img for img in PRE_FED_IMAGES if img["id"] == req.image_id), None)
        if not fallback:
            raise HTTPException(status_code=404, detail="Image not found")
        filename = fallback["filename"]

    # Give PyTorch the full Windows path — NOT the URL
    local_path = os.path.join(TEST_IMAGES_DIR, filename)

    parent, child = cv_service.predict(local_path)

    guess_clean  = req.user_guess.lower().strip()
    parent_clean = parent.lower().strip()

    # Evaluate correctness via parent model
    is_correct = guess_clean == parent_clean

    # Pluralization tolerance (e.g. "Land Animal" vs "Land Animals")
    if not is_correct and guess_clean.rstrip('s') == parent_clean.rstrip('s'):
        is_correct = True

    if not is_correct:
        return {"is_correct": False}

    fact = llm_service.generate_fact(child)

    # Log the recognition
    log_entry = models.ImageRecognitionLog(
        session_id=req.session_id,
        image_path=filename,
        parent_category=parent,
        child_category=child,
    )
    db.add(log_entry)
    db.commit()

    return {
        "is_correct": True,
        "parent_category": parent,
        "child_category": child,
        "fun_fact": fact,
    }

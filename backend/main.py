from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
import os
from . import models, database
from .routers import discovery

# Create DB tables
models.Base.metadata.create_all(bind=database.engine)

app = FastAPI(title="EduVision Backend")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # For dev frontends
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(discovery.router, prefix="/api/discovery", tags=["Discovery Phase 1"])

# Serve images over HTTP so the React UI can display them
STATIC_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "test_images"))
# Check to prevent crash if directory isn't created yet
if not os.path.exists(STATIC_DIR):
    os.makedirs(STATIC_DIR)
    
app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")

@app.get("/")
def read_root():
    return {"message": "Welcome to EduVision API - Buddy the Dog says Hi!"}

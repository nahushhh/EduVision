import os
import sys
import subprocess
from fastapi import APIRouter

router = APIRouter()

@router.post("/start")
def start_gesture_quiz():
    """
    Launches the OpenCV python script for the Gesture Quiz.
    Because it's an OpenCV GUI, it needs to run as an independent process on the host machine.
    """
    script_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "gesturequiz", "main.py"))
    
    # Run the script non-blocking
    subprocess.Popen([sys.executable, script_path])
    
    return {"message": "Gesture Quiz Launched!"}

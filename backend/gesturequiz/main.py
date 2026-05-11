import cv2
import sys
import os

# Add parent directory to sys path so relative imports work if run directly
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from gesturequiz.gesture.detector import GestureDetector
from gesturequiz.engagement.model import EngagementModel
from gesturequiz.quiz.engine import QuizEngine
from gesturequiz.ui.renderer import UIRenderer
from gesturequiz.ui.sound import play_success, play_fail

def main():
    print("Opening webcam...")
    cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
    if not cap.isOpened():
        print("Error: Could not open webcam.")
        return
    print("Webcam opened successfully.")

    # Initialize modules
    detector = GestureDetector(hover_threshold=2.0) # 2 seconds hover to select
    engagement_model = EngagementModel()
    quiz = QuizEngine()
    renderer = UIRenderer()
    
    cv2.namedWindow("EduVision - Gesture Quiz", cv2.WINDOW_NORMAL)
    cv2.resizeWindow("EduVision - Gesture Quiz", 1280, 720)
    cv2.setWindowProperty("EduVision - Gesture Quiz", cv2.WND_PROP_TOPMOST, 1)

    frame_count = 0

    while True:
        ret, frame = cap.read()
        if not ret:
            break
            
        frame = cv2.flip(frame, 1) # Mirror effect for natural interaction
        frame_count += 1

        # Run engagement model async every 10 frames to avoid lag
        if frame_count % 10 == 0:
            engagement_model.analyze_async(frame)

        # Process gestures
        frame, hover_zone, hover_progress, is_selected = detector.process_frame(frame)
        
        # Check game logic
        current_q = quiz.get_current_question()
        engagement_status = engagement_model.get_status()
        
        if is_selected and current_q:
            correct = quiz.submit_answer(hover_zone)
            if correct:
                play_success()
            else:
                play_fail()

        # Render UI
        frame = renderer.draw(
            frame=frame, 
            question=current_q, 
            score=quiz.score, 
            streak=quiz.streak, 
            engagement=engagement_status, 
            hover_zone=hover_zone, 
            hover_progress=hover_progress
        )

        cv2.imshow("EduVision - Gesture Quiz", frame)

        key = cv2.waitKey(1) & 0xFF
        if key == ord('q'):
            break
        elif key == ord('r'):
            # Restart
            quiz = QuizEngine()

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()

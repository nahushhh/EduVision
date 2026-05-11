import cv2
import threading

class EngagementModel:
    def __init__(self):
        # Lazy import to avoid loading TF until needed
        from deepface import DeepFace
        self.DeepFace = DeepFace
        
        self.current_engagement = "Neutral"
        self._lock = threading.Lock()
        self._is_analyzing = False

    def analyze_async(self, frame):
        """
        Runs deepface analysis in a background thread to prevent OpenCV UI blocking.
        """
        with self._lock:
            if self._is_analyzing:
                return
            self._is_analyzing = True
            
        # Copy frame to avoid thread mutations
        frame_copy = frame.copy()
        
        def worker():
            try:
                # enforce_detection=False prevents crash if face leaves frame
                result = self.DeepFace.analyze(frame_copy, actions=['emotion'], enforce_detection=False, silent=True)
                
                # If multiple faces, take first
                if isinstance(result, list):
                    result = result[0]
                    
                emotion = result.get('dominant_emotion', 'neutral')
                
                if emotion in ['happy', 'surprise']:
                    status = "Engaged"
                elif emotion in ['sad', 'fear', 'angry']:
                    status = "Struggling"
                elif emotion in ['disgust']:
                    status = "Distracted"
                else:
                    status = "Neutral"
                    
                with self._lock:
                    self.current_engagement = status
            except Exception as e:
                pass
            finally:
                with self._lock:
                    self._is_analyzing = False

        threading.Thread(target=worker, daemon=True).start()

    def get_status(self):
        with self._lock:
            return self.current_engagement

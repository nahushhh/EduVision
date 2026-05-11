import cv2
import mediapipe as mp
import time

class GestureDetector:
    def __init__(self, hover_threshold=2.0):
        self.mp_hands = mp.solutions.hands
        self.hands = self.mp_hands.Hands(
            max_num_hands=1,
            min_detection_confidence=0.7,
            min_tracking_confidence=0.7
        )
        self.mp_draw = mp.solutions.drawing_utils
        
        self.hover_threshold = hover_threshold
        self.current_zone = None
        self.zone_enter_time = None

    def _get_zone(self, x, y, w, h):
        """Map normalized coordinates to 4 quadrants A,B,C,D"""
        if x < 0.5 and y < 0.5:
            return "A"
        elif x >= 0.5 and y < 0.5:
            return "B"
        elif x < 0.5 and y >= 0.5:
            return "C"
        else:
            return "D"

    def process_frame(self, frame):
        """
        Processes the frame, draws landmarks, determines active zone.
        Returns: 
          - frame (drawn)
          - zone string ("A", "B", "C", "D") or None
          - progress (0.0 to 1.0) indicating hover progress
          - is_selected (bool) if hover threshold met
        """
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = self.hands.process(rgb_frame)
        
        h, w, c = frame.shape
        zone = None
        progress = 0.0
        is_selected = False

        if results.multi_hand_landmarks:
            hand_lms = results.multi_hand_landmarks[0]
            self.mp_draw.draw_landmarks(frame, hand_lms, self.mp_hands.HAND_CONNECTIONS)
            
            # Use Index Finger Tip (Landmark 8)
            index_finger = hand_lms.landmark[8]
            
            zone = self._get_zone(index_finger.x, index_finger.y, w, h)
            
            if zone == self.current_zone:
                if self.zone_enter_time:
                    elapsed = time.time() - self.zone_enter_time
                    progress = min(1.0, elapsed / self.hover_threshold)
                    if progress >= 1.0:
                        is_selected = True
                        self.zone_enter_time = None # Reset after selection
            else:
                self.current_zone = zone
                self.zone_enter_time = time.time()
                progress = 0.0
        else:
            self.current_zone = None
            self.zone_enter_time = None

        return frame, zone, progress, is_selected

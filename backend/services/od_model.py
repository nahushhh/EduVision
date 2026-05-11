import os
from PIL import Image

class ObjectDetectionService:
    def __init__(self):
        self.models_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "ir_models"))
        self.model_path = os.path.join(self.models_dir, "best_final_latest.pt")
        self.model = None
        
        try:
            from ultralytics import YOLO
            if os.path.exists(self.model_path):
                print(f"Loading YOLO model from {self.model_path}")
                self.model = YOLO(self.model_path)
            else:
                print(f"Warning: YOLO model not found at {self.model_path}. Using mock detection.")
        except ImportError:
            print("Warning: ultralytics not installed. Using mock detection.")
            
    def evaluate_click(self, image_path: str, click_x_ratio: float, click_y_ratio: float, expected_class: str) -> dict:
        """
        Evaluates if the clicked ratio coordinates fall within the bounding box of the expected class.
        """
        if not os.path.exists(image_path):
            return {"is_correct": False, "message": "Image not found.", "detected_class": None}
            
        try:
            img = Image.open(image_path)
            width, height = img.size
            
            click_x = click_x_ratio * width
            click_y = click_y_ratio * height
            
            # Use real YOLO model if available
            if self.model is not None:
                results = self.model(image_path, verbose=False)
                
                # Check all detected bounding boxes
                for result in results:
                    boxes = result.boxes
                    for box in boxes:
                        # Convert to standard python scalars
                        cls_id = int(box.cls[0].item())
                        class_name = result.names[cls_id]
                        
                        x1, y1, x2, y2 = box.xyxy[0].tolist()
                        
                        # Check if click falls inside this bounding box
                        if x1 <= click_x <= x2 and y1 <= click_y <= y2:
                            # Is it the class we are looking for?
                            if class_name.lower() == expected_class.lower():
                                return {"is_correct": True, "message": f"Yay! That's correct! It's a {class_name}!", "detected_class": class_name}
                            else:
                                # They clicked on something else
                                return {"is_correct": False, "message": f"Oops! You clicked on a {class_name}. Try again!", "detected_class": class_name}
                
                # If they clicked in empty space
                return {"is_correct": False, "message": "Oops! I don't see anything there. Try again!", "detected_class": None}
            
            # --- MOCK DETECTION FALLBACK ---
            # If the user hasn't added the .pt file yet, just pretend the right half of the screen is the firetruck
            else:
                print(f"Mocking evaluation for {expected_class} at X:{click_x_ratio:.2f}, Y:{click_y_ratio:.2f}")
                # Mock: If they click on the right side of the image (X > 0.5), we pretend it's a firetruck
                if click_x_ratio > 0.5:
                    if expected_class.lower() == "firetruck" or expected_class.lower() == "fire truck":
                        return {"is_correct": True, "message": "Yay that's correct!", "detected_class": "firetruck"}
                    else:
                        return {"is_correct": False, "message": f"Oops! You found a firetruck. Where is the {expected_class}?", "detected_class": "firetruck"}
                else:
                    return {"is_correct": False, "message": "Oops! Try clicking on the other side!", "detected_class": None}
                    
        except Exception as e:
            print(f"Error during object detection evaluation: {e}")
            return {"is_correct": False, "message": "Something went wrong with the detector.", "detected_class": None}

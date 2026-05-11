import os
from fastapi import APIRouter, HTTPException
from .. import schemas
from ..services.od_model import ObjectDetectionService

router = APIRouter()
od_service = ObjectDetectionService()

TEST_IMAGES_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "test_images"))

MOCK_STORIES = [
    {
        "id": 1,
        "title": "Kitten Rescue",
        "scenes": [
            {
                "scene_id": 1,
                "description": "Oh no! A little kitten is stuck in a tall tree. Who will you call for help?",
                "context_image": "scene1.1.jfif",      
                "interactive_image": "scene1.2.jpg", 
                "target_object": "Fire Truck"
            }
        ]
    },
    {
        "id": 2,
        "title": "The Great Escape",
        "scenes": [
            {
                "scene_id": 1,
                "description": "A sneaky thief is running away with the jewels! Who can chase them down?",
                "context_image": "scene2.1.jfif",      
                "interactive_image": "scene2.2.jpg", 
                "target_object": "Police Car"
            }
        ]
    },
    {
        "id": 3,
        "title": "Ouch! A Scraped Knee",
        "scenes": [
            {
                "scene_id": 1,
                "description": "Oh dear, someone fell down and scraped their knee. Who can give them a bandage?",
                "context_image": "scene3.1.jfif",      
                "interactive_image": "scene3.2.jpg", 
                "target_object": "Ambulance"
            }
        ]
    },
    {
        "id": 4,
        "title": "The Magic Traffic Light",
        "scenes": [
            {
                "scene_id": 1,
                "description": "The cars are driving too fast! Which signal tells them to STOP?",
                "context_image": "scene4.1.1.jpeg",      
                "interactive_image": "scene4.1.2.jpeg", 
                "target_object": "Red Light"
            },
            {
                "scene_id": 2,
                "description": "Good job! Now, which signal tells the cars to SLOW DOWN and get ready to stop?",
                "context_image": "scene4.2.1.jpeg",      
                "interactive_image": "scene4.1.2.jpeg", 
                "target_object": "Yellow Light"
            },
            {
                "scene_id": 3,
                "description": "Perfect! Finally, which signal tells the cars they can GO safely?",
                "context_image": "scene4.1.1.jpeg",      
                "interactive_image": "scene4.1.2.jpeg", 
                "target_object": "Green Light"
            }
        ]
    },
    {
        "id": 5,
        "title": "Traffic Jam Troubles",
        "scenes": [
            {
                "scene_id": 1,
                "description": "There is a huge traffic jam at the intersection! Who can direct the cars?",
                "context_image": "scene5.1.jpeg",      
                "interactive_image": "scene5.2.jpeg", 
                "target_object": "Police"
            }
        ]
    },
    {
        "id": 6,
        "title": "Fire at the Bakery!",
        "scenes": [
            {
                "scene_id": 1,
                "description": "Oh no! There's smoke coming from the bakery! Who is trained to put out the fire?",
                "context_image": "scene6.1.jpeg",      
                "interactive_image": "scene6.2.jpeg", 
                "target_object": "Fire Fighters"
            }
        ]
    }
]

@router.get("/scenarios")
def get_scenarios():
    scenarios = []
    for s in MOCK_STORIES:
        formatted_scenes = []
        for scene in s["scenes"]:
            formatted_scenes.append({
                "scene_id": scene["scene_id"],
                "description": scene["description"],
                "context_image_url": f"http://localhost:8000/static/{scene['context_image']}",
                "interactive_image_url": f"http://localhost:8000/static/{scene['interactive_image']}",
                "target_object": scene["target_object"]
            })
            
        scenarios.append({
            "id": s["id"],
            "title": s["title"],
            "scenes": formatted_scenes
        })
    return {"scenarios": scenarios}

@router.post("/evaluate", response_model=schemas.StoryClickResponse)
def evaluate_click(req: schemas.StoryClickRequest):
    story = next((s for s in MOCK_STORIES if s["id"] == req.story_id), None)
    if not story:
        raise HTTPException(status_code=404, detail="Story not found")
        
    scene = next((sc for sc in story["scenes"] if sc["scene_id"] == req.scene_id), None)
    if not scene:
        raise HTTPException(status_code=404, detail="Scene not found")
        
    local_path = os.path.join(TEST_IMAGES_DIR, scene["interactive_image"])
    
    result = od_service.evaluate_click(
        image_path=local_path,
        click_x_ratio=req.click_x_ratio,
        click_y_ratio=req.click_y_ratio,
        expected_class=scene["target_object"]
    )
    
    return result

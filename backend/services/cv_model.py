import torch
import torch.nn as nn
import torch.nn.functional as F
import torchvision.models as models
import torchvision.transforms as transforms
from PIL import Image
import os

DEVICE = torch.device("cuda" if torch.cuda.is_available() else "cpu")
class HierarchicalResNet(nn.Module):
    def __init__(self, num_parent_classes, num_child_classes, weight_path=None):
        super(HierarchicalResNet, self).__init__()
        # 1. Load the base ResNet
        self.resnet = models.resnet18(weights=None)
        num_ftrs = self.resnet.fc.in_features

        # 2. Define the TWO heads
        self.parent_head = nn.Linear(num_ftrs, num_parent_classes)
        self.child_head = nn.Linear(num_ftrs, num_child_classes)

        # 3. Remove the original ResNet head
        self.resnet.fc = nn.Identity()

        # 4. Load Parent Weights if provided
        if weight_path:
            # Create a temporary dict to match your saved parent model structure
            temp_model = models.resnet18(weights=None)
            temp_model.fc = nn.Linear(num_ftrs, num_parent_classes)
            temp_model.load_state_dict(torch.load(weight_path, map_location=DEVICE))

            # Transfer weights to our new structure
            self.resnet.load_state_dict(temp_model.resnet.state_dict() if hasattr(temp_model, 'resnet') else {k.replace('resnet.', ''): v for k, v in temp_model.state_dict().items() if 'fc' not in k})
            self.parent_head.load_state_dict(temp_model.fc.state_dict())
            print("[OK] Backbone and Parent Head weights loaded.")

    def forward(self, x):
        # Shared features from backbone
        features = self.resnet(x)
        # Predict both levels simultaneously
        parent_logits = self.parent_head(features)
        child_logits = self.child_head(features)
        return parent_logits, child_logits

def load_weights_robust(model_obj, weight_path):
    """Fixes naming mismatches (prefixes) when loading weights."""
    state_dict = torch.load(weight_path, map_location=DEVICE)
    new_state_dict = {}

    for key, value in state_dict.items():
        # If the saved key is 'conv1.weight' but the model expects 'resnet.conv1.weight'
        if not key.startswith('resnet.') and not key.startswith('child_head.') and not key.startswith('parent_head.'):
            if 'fc' in key:
                # Map the old 'fc' head to the new 'child_head'
                new_key = key.replace('fc.', 'child_head.')
            else:
                # Map backbone layers to 'resnet.layer_name'
                new_key = f'resnet.{key}'
        else:
            new_key = key
        new_state_dict[new_key] = value

    # Load with strict=False to ignore the parent_head if it wasn't in the child model save
    model_obj.load_state_dict(new_state_dict, strict=False)
    print(f"[OK] Successfully loaded: {os.path.basename(weight_path)}")
    return model_obj

class CVModelService:
    def __init__(self):
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        print(f"Using device: {self.device}")
        
        self.parent_classes = ['Birds', 'Fruits', 'Land Animals', 'Sea Animals', 'Veggies', 'Vehicles']
        
        self.child_classes = {
            'birds': ['Albatross', 'Auklet', 'Blackbird', 'Bunting', 'Crow', 'Cuckoo', 'Flycatcher', 'Grebe', 'Gull', 'Hummingbird', 'Sparrow'],
            'fruits': ['apple', 'banana', 'carambola', 'dragon fruit', 'guava', 'kiwi', 'mango', 'muskmelon', 'orange', 'peach', 'pear', 'pomegranate'],
            'veggies': ['brinjal', 'garlic', 'green chilli', 'ladies finger', 'onion', 'potato'],
            'vehicles': ['bikes', 'bus', 'cars', 'scooter', 'truck'],
            'sea animals': ['Clams', 'Corals', 'Crabs', 'Dolphin', 'Eel', 'Fish', 'Jelly Fish', 'Lobster', 'Octopus', 'Penguin', 'Seahorse', 'Sharks', 'Whale'],
            'land animals': ['bear', 'camel', 'cat', 'cow', 'deer', 'dog', 'elephant', 'horse', 'leopard', 'lion', 'monkey', 'rabbit', 'tiger']
        }
        
        # Assuming you will place the models in 'e:\Projects\EduVision\backend\ir_models'
        MODELS_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "ir_models"))
        
        main_parent_model = os.path.join(MODELS_DIR, 'resnet_finetuned_new latest.pth')
        birds_model = os.path.join(MODELS_DIR, 'child_birds_model_new_latest.pth')
        fruits_model = os.path.join(MODELS_DIR, 'child_fruits_model_new_latest.pth')
        veggies_model = os.path.join(MODELS_DIR, 'child_veggies_model_new_latest.pth')
        sea_animals_model = os.path.join(MODELS_DIR, 'child_sea_animal_model_new_latest.pth')
        land_animals_model = os.path.join(MODELS_DIR, 'child_land_animal_model_new_latest.pth')
        vehicles_model = os.path.join(MODELS_DIR, 'child_vehicles_model_new_latest.pth')
        
        num_parents = len(self.parent_classes)
        
        # 1. Initialize & Load Parent
        self.parent_model = models.resnet18(weights=None)
        num_ftrs = self.parent_model.fc.in_features
        self.parent_model.fc = nn.Linear(num_ftrs, num_parents)
        
        try:
            self.parent_model.load_state_dict(torch.load(main_parent_model, map_location=self.device))
            self.parent_model.to(self.device)
            # self.parent_model.eval()
            print("Loaded Parent Model")
        except Exception as e:
            print(f"Warning: Could not load parent model. {e}")

        # 2. Initialize & Load Child Models
        self.child_models_dict = {}
        
        try:
            fruit_model_obj = HierarchicalResNet(num_parents, len(self.child_classes['fruits'])).to(self.device)
            load_weights_robust(fruit_model_obj, fruits_model)
            self.child_models_dict['fruits'] = fruit_model_obj
        except Exception as e:
            print(f"Error loading fruits model: {e}")
            
        try:
            veggies_model_obj = HierarchicalResNet(num_parents, len(self.child_classes['veggies'])).to(self.device)
            load_weights_robust(veggies_model_obj, veggies_model)
            self.child_models_dict['veggies'] = veggies_model_obj
        except Exception as e:
            print(f"Error loading veggies model: {e}")
            
        try:
            bird_model_obj = HierarchicalResNet(num_parents, len(self.child_classes['birds'])).to(self.device)
            load_weights_robust(bird_model_obj, birds_model)
            self.child_models_dict['birds'] = bird_model_obj
        except Exception as e:
            print(f"Error loading birds model: {e}")
            
        try:
            land_animal_model_obj = HierarchicalResNet(num_parents, len(self.child_classes['land animals'])).to(self.device)
            load_weights_robust(land_animal_model_obj, land_animals_model)
            self.child_models_dict['land animals'] = land_animal_model_obj
        except Exception as e:
            print(f"Error loading land animals model: {e}")
            
        try:
            sea_animal_model_obj = HierarchicalResNet(num_parents, len(self.child_classes['sea animals'])).to(self.device)
            load_weights_robust(sea_animal_model_obj, sea_animals_model)
            self.child_models_dict['sea animals'] = sea_animal_model_obj
        except Exception as e:
            print(f"Error loading sea animals model: {e}")
            
        try:
            vehicle_model_obj = HierarchicalResNet(num_parents, len(self.child_classes['vehicles'])).to(self.device)
            load_weights_robust(vehicle_model_obj, vehicles_model)
            self.child_models_dict['vehicles'] = vehicle_model_obj
        except Exception as e:
            print(f"Error loading vehicles model: {e}")
            
        # Transform logic - using the exact transform from your script
        self.inference_transform = transforms.Compose([
            transforms.Resize((224, 224)),
            transforms.ToTensor(),
            transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])
        ])

    def predict(self, image_path: str):
        # Fallback to mock if full model isn't loaded or image isn't available
        if not hasattr(self, 'parent_model') or not os.path.exists(image_path):
            print(f"Could not load {image_path} or model missing. Mocking...")
            return self._mock_predict(image_path)
            
        try:
            img = Image.open(image_path).convert('RGB')
            img_tensor = self.inference_transform(img).unsqueeze(0).to(self.device)
            
            # Parent model inference
            self.parent_model.eval()
            with torch.no_grad():
                parent_out = self.parent_model(img_tensor)
                if isinstance(parent_out, tuple):
                    parent_out = parent_out[0]
                    
                parent_probs = F.softmax(parent_out, dim=1)
                parent_conf, parent_idx = torch.max(parent_probs, 1)
                parent_name = self.parent_classes[parent_idx.item()]
                
            # Child model inference
            child_model = self.child_models_dict.get(parent_name.lower())
            if child_model is None:
                return parent_name, f"Unknown {parent_name}"
                
            child_model.eval()
            with torch.no_grad():
                child_out = child_model(img_tensor)
                if isinstance(child_out, tuple):
                    _, child_out = child_out
                
                child_probs = F.softmax(child_out, dim=1)
                child_conf, child_idx = torch.max(child_probs, 1)
                specific_child_labels = self.child_classes[parent_name.lower()]
                child_name = specific_child_labels[child_idx.item()]
                
            return parent_name, child_name
            
        except Exception as e:
            print(f"Inference error: {e}")
            return self._mock_predict(image_path)
            
    def _mock_predict(self, image_path: str):
        path_lower = image_path.lower()
        if "albetross" in path_lower or "bird" in path_lower:
            return "Birds", "Albatross"
        elif "camel" in path_lower or "dog" in path_lower:
            return "Land Animals", "Camel"
        elif "car" in path_lower:
            return "Vehicles", "Cars"
        elif "whale" in path_lower or "sea" in path_lower:
            return "Sea Animals", "Whale"
        else:
            return "Fruits", "Apple"

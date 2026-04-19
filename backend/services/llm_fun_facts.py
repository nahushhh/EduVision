import os
from dotenv import load_dotenv

load_dotenv(os.path.join(os.path.dirname(__file__), '.env'))

# Backwards compatibility if your .env file uses LLM_API_KEY! 
if "LLM_API_KEY" in os.environ and "GEMINI_API_KEY" not in os.environ:
    os.environ["GEMINI_API_KEY"] = os.environ["LLM_API_KEY"]

try:
    from google import genai
except ImportError:
    genai = None

class LLMFunFactService:
    def __init__(self):
        # The client automatically picks up os.environ["GEMINI_API_KEY"]
        if genai and os.environ.get("GEMINI_API_KEY"):
            try:
                self.client = genai.Client()
            except Exception as e:
                print(f"Failed to initialize Gemini Client: {e}")
                self.client = None
        else:
            self.client = None
        
    def generate_fact(self, child_category: str):
        clean_category = child_category.replace("Unknown ", "").strip()
        
        # 1. Fallback if the SDK is missing or API key isn't loaded correctly
        if not self.client:
             print("Warning: Gemini SDK missing or GEMINI_API_KEY not found. Using fallback.")
             return self._fallback_generator(clean_category)
             
        # 2. Build the kid-friendly prompt
        prompt = f"Generate a very short, fun, and kid-friendly fact (ages 3-6) about a {clean_category} in exactly one sentence. Include a relevant emoji at the end."
        
        try:
            # 3. Use the bleeding-edge official SDK approach exactly as you provided
            response = self.client.models.generate_content(
                model="gemini-3-flash-preview", 
                contents=prompt
            )
            
            fact = response.text
            return fact.strip() if fact else self._fallback_generator(clean_category)
            
        except Exception as e:
            print(f"Error calling Gemini SDK for fact generation: {e}")
            return self._fallback_generator(clean_category)
            
    def _fallback_generator(self, child_category: str):
        # Safe fallback dictionary if your API is offline or key is missing
        facts = {
            "Dog": "Dogs have an amazing sense of smell, 40 times better than ours! 🐶",
            "Parrot": "Parrots can imitate human speech and even solve puzzles! 🦜",
            "Apple": "Apples float in water because they are 25% air! 🍎",
            "Car": "The first cars ever made didn't have steering wheels, they had levers! 🚗",
            "Albatross": "An albatross can glide over the ocean for hundreds of miles without even flapping its wings! 🌊",
            "Camel": "Camels store fat, not water, inside their humps to travel through the desert! 🐪",
            "Whale": "Blue whales are the largest animals to have ever lived on Earth! 🐋"
        }
        return facts.get(child_category, f"Did you know {child_category}s are super fascinating? 🌟")

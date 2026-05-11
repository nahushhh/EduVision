import os
from dotenv import load_dotenv

load_dotenv(os.path.join(os.path.dirname(__file__), '.env'))

try:
    from groq import Groq
except ImportError:
    Groq = None

class LLMFunFactService:
    def __init__(self):
        api_key = os.environ.get("GROQ_API_KEY")
        if Groq and api_key:
            try:
                self.client = Groq(api_key=api_key)
                print("[OK] Groq client initialized.")
            except Exception as e:
                print(f"Failed to initialize Groq client: {e}")
                self.client = None
        else:
            self.client = None
            if not Groq:
                print("Warning: groq package not installed. Using fallback facts.")
            else:
                print("Warning: GROQ_API_KEY not found. Using fallback facts.")

    def generate_fact(self, child_category: str):
        clean_category = child_category.replace("Unknown ", "").strip()

        if not self.client:
            return self._fallback_generator(clean_category)

        prompt = (
            f"Generate a very short, fun, and kid-friendly fact (ages 3-6) about a "
            f"{clean_category} in exactly one sentence. Include a relevant emoji at the end."
        )

        try:
            response = self.client.chat.completions.create(
                model="llama-3.1-8b-instant",
                messages=[{"role": "user", "content": prompt}],
                max_tokens=80,
                temperature=0.8,
            )
            fact = response.choices[0].message.content
            return fact.strip() if fact else self._fallback_generator(clean_category)

        except Exception as e:
            print(f"Error calling Groq API: {e}")
            return self._fallback_generator(clean_category)

    def _fallback_generator(self, child_category: str):
        facts = {
            "Dog": "Dogs have an amazing sense of smell, 40 times better than ours! 🐶",
            "Parrot": "Parrots can imitate human speech and even solve puzzles! 🦜",
            "Apple": "Apples float in water because they are 25% air! 🍎",
            "Car": "The first cars ever made didn't have steering wheels, they had levers! 🚗",
            "Albatross": "An albatross can glide over the ocean for hundreds of miles without flapping its wings! 🌊",
            "Camel": "Camels store fat, not water, inside their humps to travel through the desert! 🐪",
            "Whale": "Blue whales are the largest animals to have ever lived on Earth! 🐋",
        }
        return facts.get(child_category, f"Did you know {clean_category}s are super fascinating? 🌟")

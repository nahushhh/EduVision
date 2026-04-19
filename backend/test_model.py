import sys
import os

# Add parent directory to path so we can import backend packages properly
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from backend.services.cv_model import CVModelService

def main():
    print("Loading PyTorch Models into memory... This might take a few seconds.")
    # This initialization loads the parent and all child weights completely independently of the FastAPI server
    service = CVModelService()
    
    print("\n" + "="*50)
    print("🤖 EduVision Local Model Tester Ready!")
    print("="*50)
    
    while True:
        try:
            image_path = input("\nEnter the absolute path to an image (or type 'q' to quit):\n> ").strip()
        except KeyboardInterrupt:
            break
            
        if image_path.lower() in ('q', 'quit', 'exit'):
            print("Exiting tester...")
            break
            
        # Strip exact quotes if you drag-and-dropped the file into the Windows terminal
        image_path = image_path.strip('"').strip("'")
            
        if not os.path.exists(image_path):
            print(f"❌ Error: File not found exactly at: '{image_path}'")
            continue
            
        print("\n⏳ Running inference...")
        parent, child = service.predict(image_path)
        
        print("\n" + "-"*30)
        print("🔍 INFERENCE RESULTS")
        print("-"*30)
        print(f"PARENT LEVEL: {parent.upper()}")
        print(f"CHILD LEVEL:  {child.upper()}")
        print("-"*30 + "\n")

if __name__ == "__main__":
    main()

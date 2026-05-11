# EduVision 🎓👁️

EduVision is an interactive educational platform designed for children, featuring three primary learning modes powered by computer vision and AI integration. The application combines a **React-based frontend** with a **FastAPI Python backend**, utilizing advanced machine learning models for image recognition, object detection, and gesture-based interaction.

## 🚀 Features

### 1. Discovery Session (Image Recognition)
An interactive gameplay mode where children identify objects across 7 categories (Birds, Fruits, Land Animals, Sea Animals, Vehicles, Veggies). It features:
- **Hierarchical ResNet18 Architecture** for parent and child class predictions.
- **Instant AI-powered feedback** and educational fun facts upon correct identification.
- Streak and score tracking for user engagement.

### 2. Story Session (Object Detection)
An interactive narrative adventure where children help story characters by identifying and clicking on objects in scenes.
- Powered by **YOLOv8** for real-time single-shot multi-scale object detection.
- Includes 6 predefined scenarios (e.g., Kitten Rescue, The Great Escape).
- Children learn to recognize emergency vehicles, traffic signals, and community helpers.

### 3. Gesture Quiz (Hand Tracking)
A real-time interactive quiz where children use hand gestures to answer questions.
- Uses **MediaPipe Hands** to track 21 3D hand keypoints in real-time.
- Divides the screen into hover-able quadrants corresponding to quiz answers.
- Audio-visual feedback, score tracking, and temporal smoothing (Kalman filtering) for a fluid experience.

## 🛠️ Technology Stack

- **Frontend**: React 18+ (Vite), Tailwind CSS, Axios
- **Backend**: FastAPI, Uvicorn, SQLAlchemy (SQLite)
- **AI/ML**: 
  - PyTorch & TorchVision (Image Classification)
  - Ultralytics YOLOv8 (Object Detection)
  - MediaPipe (Hand Tracking)
  - OpenCV (Image processing & GUI)

## ⚙️ Prerequisites

- Python 3.8+
- Node.js 16+
- Webcam (for Gesture Quiz)
- *Optional but recommended*: NVIDIA GPU with CUDA for faster AI inference.

## 💻 Installation & Setup

### 1. Clone the repository
```bash
git clone <repository-url>
cd EduVision
```

### 2. Backend Setup
Navigate to the backend directory, install dependencies, and run the FastAPI server:
```bash
cd backend

# Create and activate virtual environment
python -m venv .venv
# Windows: .venv\Scripts\activate
# Mac/Linux: source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Start the server
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

### 3. Frontend Setup
Open a new terminal, navigate to the frontend directory, install dependencies, and start the development server:
```bash
cd frontend
npm install
npm run dev
```

## 🎮 Usage

1. Start both the backend and frontend servers as described above.
2. Open your browser and navigate to `http://localhost:5173` (default Vite port).
3. The backend runs on `http://localhost:8000`. API documentation is available at `http://localhost:8000/docs`.
4. Select one of the learning modes from the main menu and start exploring!

---
*Note: Make sure your webcam is enabled and you have sufficient lighting when using the Gesture Quiz feature.*

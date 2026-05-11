import React, { useState } from 'react';
import axios from 'axios';
import DiscoverySession from './pages/DiscoverySession';
import StorySession from './pages/StorySession';
import DogMascot from './components/DogMascot';
import NavBar from './components/NavBar';

function App() {
  const [mode, setMode] = useState('menu'); // 'menu', 'discovery', 'story'

  const launchGestureQuiz = async () => {
    try {
      await axios.post('http://localhost:8000/api/gesture/start');

    } catch (err) {
      console.error("Failed to launch gesture quiz", err);
      alert("Failed to launch Gesture Quiz. Make sure backend is running.");
    }
  };

  if (mode === 'discovery') {
    return (
      <div className="min-h-screen bg-blue-400 font-sans flex flex-col">
        <NavBar onReturnHome={() => setMode('menu')} />
        <div className="flex-1 w-full h-full">
          <DiscoverySession onReturnHome={() => setMode('menu')} />
        </div>
      </div>
    );
  }

  if (mode === 'story') {
    return (
      <div className="min-h-screen bg-orange-400 font-sans flex flex-col">
        <NavBar onReturnHome={() => setMode('menu')} />
        <div className="flex-1 w-full h-full">
          <StorySession onReturnHome={() => setMode('menu')} />
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-yellow-400 font-sans flex flex-col items-center overflow-x-hidden">
      <NavBar onReturnHome={() => setMode('menu')} />
      
      <div className="flex-1 w-full max-w-[90rem] px-8 py-12 flex flex-col items-center animate-popIn">
        
        <div className="flex justify-center mb-6 animate-float">
          <DogMascot message="Hi! What do you want to play today?" state="happy" />
        </div>

        <div className="grid grid-cols-1 md:grid-cols-3 gap-12 w-full mt-4">
          {/* Discovery Mode Card */}
          <button 
            onClick={() => setMode('discovery')}
            className="flex flex-col items-center overflow-hidden bg-blue-500 rounded-[4rem] shadow-[0_20px_0_rgb(217,119,6)] hover:-translate-y-6 hover:shadow-[0_30px_0_rgb(217,119,6)] active:translate-y-4 active:shadow-none transition-all border-[12px] border-white group animate-fadeInUp"
            style={{ animationDelay: '0.1s', opacity: 0 }}
          >
            <div className="w-full h-[400px] bg-blue-100 overflow-hidden relative">
              <img src="/discovery_mode.png" alt="Discovery Mode" className="w-full h-full object-cover group-hover:scale-110 transition-transform duration-700" />
            </div>
            <div className="w-full p-12 bg-blue-500 text-center">
              <h2 className="text-6xl font-black text-white drop-shadow-md mb-4">Discovery</h2>
              <p className="text-blue-100 font-bold text-3xl">Find items and learn facts!</p>
            </div>
          </button>

          {/* Story Mode Card */}
          <button 
            onClick={() => setMode('story')}
            className="flex flex-col items-center overflow-hidden bg-orange-500 rounded-[4rem] shadow-[0_20px_0_rgb(217,119,6)] hover:-translate-y-6 hover:shadow-[0_30px_0_rgb(217,119,6)] active:translate-y-4 active:shadow-none transition-all border-[12px] border-white group animate-fadeInUp"
            style={{ animationDelay: '0.2s', opacity: 0 }}
          >
            <div className="w-full h-[400px] bg-orange-100 overflow-hidden relative">
              <img src="/story_mode.png" alt="Story Mode" className="w-full h-full object-cover group-hover:scale-110 transition-transform duration-700" />
            </div>
            <div className="w-full p-12 bg-orange-500 text-center">
              <h2 className="text-6xl font-black text-white drop-shadow-md mb-4">Story Mode</h2>
              <p className="text-orange-100 font-bold text-3xl">Interactive Rescue Adventures!</p>
            </div>
          </button>

          {/* Gesture Mode Card */}
          <button 
            onClick={launchGestureQuiz}
            className="flex flex-col items-center overflow-hidden bg-green-500 rounded-[4rem] shadow-[0_20px_0_rgb(21,128,61)] hover:-translate-y-6 hover:shadow-[0_30px_0_rgb(21,128,61)] active:translate-y-4 active:shadow-none transition-all border-[12px] border-white group animate-fadeInUp"
            style={{ animationDelay: '0.3s', opacity: 0 }}
          >
            <div className="w-full h-[400px] bg-green-100 overflow-hidden relative">
              <img src="/gesture_mode.png" alt="Gesture Mode" className="w-full h-full object-cover group-hover:scale-110 transition-transform duration-700" />
            </div>
            <div className="w-full p-12 bg-green-500 text-center">
              <h2 className="text-6xl font-black text-white drop-shadow-md mb-4">Gesture Quiz</h2>
              <p className="text-green-100 font-bold text-3xl">Play using your webcam!</p>
            </div>
          </button>
        </div>
      </div>
    </div>
  );
}

export default App;

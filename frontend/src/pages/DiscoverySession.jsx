import React, { useState, useEffect } from 'react';
import axios from 'axios';
import DogMascot from '../components/DogMascot';
import { Play, RefreshCw, Star } from 'lucide-react';

const API_BASE = 'http://localhost:8000/api/discovery';

const DiscoverySession = ({ onReturnHome }) => {
    const [sessionId, setSessionId] = useState(null);
    const [images, setImages] = useState([]);
    const [currentIndex, setCurrentIndex] = useState(0);
    const [status, setStatus] = useState('welcome'); // welcome, playing, evaluating, fact, finished
    const [score, setScore] = useState(0);
    const [currentGuessState, setCurrentGuessState] = useState(null);

    const startSession = async () => {
        try {
            // Start session requires user_id
            const res = await axios.post(`${API_BASE}/start`, { user_id: 1, session_type: 'discovery' });
            setSessionId(res.data.session_id);
            
            // Fetch images separately
            const imgRes = await axios.get(`${API_BASE}/images`);
            setImages(imgRes.data.images);
            
            setCurrentIndex(0);
            setScore(0);
            setStatus('playing');
        } catch (err) {
            console.error("Failed to start session", err);
        }
    };

    const handleGuess = async (guess) => {
        if (status !== 'playing') return;
        
        setStatus('evaluating');
        const currentImage = images[currentIndex];
        
        try {
            const res = await axios.post(`${API_BASE}/recognize`, {
                session_id: sessionId,
                image_id: currentImage.id,
                user_guess: guess
            });
            
            if (res.data.is_correct) {
                // Determine if it's the first try
                const firstTry = !currentGuessState || !currentGuessState.failedAttempts;
                if (firstTry) {
                    setScore(prev => prev + 1);
                }
                
                setCurrentGuessState({ 
                    isCorrect: true, 
                    fact: res.data.fun_fact,
                    firstTry: firstTry
                });
                setStatus('fact');
            } else {
                // Incorrect guess
                setCurrentGuessState(prev => ({
                    ...prev,
                    isCorrect: false,
                    failedAttempts: (prev?.failedAttempts || 0) + 1
                }));
                setStatus('playing');
            }
        } catch (err) {
            console.error("Failed to submit guess", err);
            setStatus('playing');
        }
    };

    const nextImage = () => {
        if (currentIndex < images.length - 1) {
            setCurrentIndex(prev => prev + 1);
            setCurrentGuessState(null);
            setStatus('playing');
        } else {
            setStatus('finished');
        }
    };

    if (status === 'welcome') {
        return (
            <div className="flex flex-col items-center justify-center w-full h-full p-12 animate-popIn">
                <div className="w-full text-center">
                    <h1 className="text-[6rem] font-black text-white mb-6 drop-shadow-lg">Let's Play a Game!</h1>
                    <div className="flex justify-center my-8">
                        <DogMascot message="Click start to find cool objects!" state="happy" />
                    </div>
                    
                    <button onClick={startSession} className="mx-auto mt-12 flex items-center gap-4 bg-yellow-400 text-blue-900 text-4xl font-black py-8 px-16 rounded-[3rem] hover:scale-110 transition-transform shadow-[0_12px_0_rgb(202,138,4)] border-4 border-yellow-200">
                        <Play size={48} className="text-blue-900" /> Start Game!
                    </button>
                </div>
            </div>
        );
    }

    if (status === 'finished') {
         // Calculate stars (max 3, based on percentage)
         const percentage = score / images.length;
         let stars = 0;
         if (percentage >= 0.9) stars = 3;
         else if (percentage >= 0.5) stars = 2;
         else if (percentage > 0) stars = 1;
         
         const starsDisplay = [1, 2, 3].map(i => (
             <Star 
                 key={i} 
                 size={80} 
                 className={`${i <= stars ? 'text-yellow-400 fill-yellow-400 drop-shadow-lg' : 'text-blue-300 fill-blue-300 opacity-50'} transition-all duration-700`} 
                 style={{ animationDelay: `${i * 200}ms` }}
             />
         ));

         return (
            <div className="flex flex-col items-center justify-center w-full h-full p-12 relative animate-popIn">
                <div className="w-full flex flex-col items-center max-w-4xl">
                    <h1 className="text-7xl font-black text-white mb-8 drop-shadow-lg flex justify-center">
                        <Star className="w-16 h-16 text-yellow-300 mr-4"/> Game Over! <Star className="w-16 h-16 text-yellow-300 ml-4"/>
                    </h1>

                    <div className="flex gap-6 mb-10">
                        {starsDisplay}
                    </div>

                    <div className="flex justify-center w-full">
                        <DogMascot message="You did amazing! I'm so proud of you!" state="excited" />
                    </div>
                    
                    <div className="flex justify-center gap-8 mt-12">
                        <button onClick={startSession} className="flex items-center gap-4 bg-yellow-400 text-blue-900 text-4xl font-black py-8 px-16 rounded-[3rem] hover:scale-110 transition-transform shadow-[0_12px_0_rgb(202,138,4)] border-4 border-yellow-200">
                            <RefreshCw size={48} className="text-blue-900" /> Play Again!
                        </button>
                    </div>
                </div>
            </div>
        );
    }

    // playing, evaluating, or fact status
    const currentImage = images[currentIndex];
    
    if (status === 'fact') {
        return (
            <div className="flex flex-col items-center justify-center w-full h-full p-8 relative animate-fadeInUp">
                <div className="w-full max-w-5xl">
                    <h2 className="text-6xl font-black text-white mb-10 text-center drop-shadow-lg">
                        {currentGuessState?.firstTry ? 'Perfect!' : 'You got it!'}
                    </h2>
                    
                    <div className="flex justify-center mb-10">
                        <DogMascot message={currentGuessState?.fact || "Awesome job!"} state="excited" />
                    </div>
                    
                    <button onClick={nextImage} className="mx-auto mt-8 flex items-center gap-4 bg-yellow-400 text-blue-900 text-4xl font-black py-8 px-16 rounded-[3rem] hover:scale-110 transition-transform shadow-[0_12px_0_rgb(202,138,4)] border-4 border-yellow-200">
                        Next <ArrowRight size={48} />
                    </button>
                </div>
            </div>
        );
    }

    return (
        <div className="flex flex-col items-center justify-center w-full h-full p-12 relative">
            <div className="w-full max-w-[100rem]">
                <div className="flex justify-between items-center mb-8">
                    <h2 className="text-[4rem] font-black text-white drop-shadow-md">What's in the picture?</h2>
                    <div className="bg-white text-blue-600 font-black text-4xl px-10 py-4 rounded-[2rem] border-8 border-yellow-300 shadow-xl">
                        Score: {score}
                    </div>
                </div>

                <div className="flex flex-col lg:flex-row gap-12 items-stretch w-full animate-popIn">
                    {/* LEFT: The Image */}
                    <div className="flex-[1.5] w-full max-h-[600px] bg-white rounded-[3rem] overflow-hidden border-8 border-yellow-300 shadow-2xl relative flex items-center justify-center">
                         <img src={currentImage?.image_url} alt="Guess the object" className="w-full h-full object-contain p-4" onError={(e) => e.target.style.display='none'} />
                         <span className="absolute text-gray-400 font-bold text-2xl z-[-1]">Place '{currentImage?.image_url?.split('/').pop()}' in test_images/</span>
                    </div>
                    
                    {/* RIGHT: The Options */}
                    <div className="flex-1 flex flex-col justify-center items-center bg-white/20 backdrop-blur-sm p-10 rounded-[3rem] border-4 border-white/40 shadow-xl">
                        {currentGuessState && currentGuessState.isCorrect === false ? (
                             <div className="mb-8 w-full flex justify-center">
                                 <DogMascot message="Not quite! Try another one!" state="thinking" />
                             </div>
                        ) : (
                             <div className="mb-8 w-full flex justify-center">
                                 <DogMascot message="Which category is this?" state="happy" />
                             </div>
                        )}
                        
                        <div className="grid grid-cols-2 gap-6 w-full">
                             {['birds', 'fruits', 'veggies', 'vehicles', 'sea animals', 'land animals'].map(category => (
                                 <button 
                                     key={category}
                                     onClick={() => handleGuess(category)}
                                     disabled={status === 'evaluating'}
                                     className="bg-white text-blue-600 text-3xl font-black py-8 px-6 rounded-[2rem] shadow-[0_10px_0_rgb(147,197,253)] hover:-translate-y-2 hover:shadow-[0_15px_0_rgb(147,197,253)] active:translate-y-2 active:shadow-none transition-all disabled:opacity-50 disabled:cursor-not-allowed border-4 border-blue-200 capitalize w-full"
                                 >
                                     {category}
                                 </button>
                             ))}
                         </div>
                    </div>
                </div>
            </div>
            
            {status === 'evaluating' && (
                <div className="absolute inset-0 bg-blue-900/40 backdrop-blur-md z-50 flex items-center justify-center">
                    <DogMascot message="Let me take a look..." state="thinking" />
                </div>
            )}
        </div>
    );
};

// Also import ArrowRight
import { ArrowRight } from 'lucide-react';

export default DiscoverySession;

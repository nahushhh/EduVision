import React, { useState } from 'react';
import axios from 'axios';
import DogMascot from '../components/DogMascot';
import { RefreshCw, ArrowRight, PlayCircle, Sparkles, Star } from 'lucide-react';

const API_BASE = 'http://localhost:8000/api/discovery';

const DiscoverySession = () => {
    const [sessionId, setSessionId] = useState(null);
    const [images, setImages] = useState([]);
    const [currentIndex, setCurrentIndex] = useState(0);
    const [status, setStatus] = useState('welcome');
    const [currentResult, setCurrentResult] = useState(null);
    const [score, setScore] = useState(0);
    const [isFirstTry, setIsFirstTry] = useState(true);

    const startSession = async () => {
        setStatus('loading');
        try {
            const startRes = await axios.post(`${API_BASE}/start`, { user_id: 1, session_type: "discovery" });
            setSessionId(startRes.data.session_id);
            const imgRes = await axios.get(`${API_BASE}/images`);
            setImages(imgRes.data.images);
            setCurrentIndex(0);
            setScore(0);
            setIsFirstTry(true);
            setStatus('active');
        } catch (err) {
            console.error(err);
            setStatus('welcome');
        }
    };

    const recognizeImage = async (categoryLabel) => {
        setStatus('checking');
        try {
            const currentImg = images[currentIndex];
            const res = await axios.post(`${API_BASE}/recognize`, {
                session_id: sessionId,
                image_id: currentImg.id,
                user_guess: categoryLabel
            });
            
            if (res.data.is_correct) {
                if (isFirstTry) setScore(s => s + 1);
                setCurrentResult(res.data);
                setStatus('matched');
            } else {
                setIsFirstTry(false);
                setStatus('incorrect');
                setTimeout(() => setStatus('active'), 2500);
            }
        } catch (err) {
            console.error(err);
            setStatus('active');
        }
    };
    
    const GUESS_CATEGORIES = [
        { label: 'Land Animal', emoji: '🦁', color: 'from-orange-400 to-red-500', shadow: '#b91c1c' },
        { label: 'Bird', emoji: '🦅', color: 'from-sky-400 to-blue-600', shadow: '#1d4ed8' },
        { label: 'Fruits', emoji: '🍎', color: 'from-pink-400 to-rose-500', shadow: '#be123c' },
        { label: 'Veggies', emoji: '🥦', color: 'from-emerald-400 to-green-600', shadow: '#15803d' },
        { label: 'Vehicle', emoji: '🚗', color: 'from-slate-400 to-gray-600', shadow: '#374151' },
        { label: 'Sea Animal', emoji: '🐋', color: 'from-cyan-400 to-indigo-500', shadow: '#312e81' }
    ];

    const nextImage = () => {
        if (currentIndex < images.length - 1) {
            setCurrentIndex(currentIndex + 1);
            setCurrentResult(null);
            setIsFirstTry(true);
            setStatus('active');
        } else {
            setStatus('finished');
        }
    };

    if (status === 'welcome') {
        return (
            <div className="flex flex-col items-center justify-center min-h-screen p-8 bg-gradient-to-br from-cyan-400 via-blue-400 to-purple-500 overflow-hidden relative">
                {/* Decorative background elements */}
                <Sparkles className="absolute top-20 left-20 text-yellow-300 w-24 h-24 opacity-70 animate-pulse" />
                <Star className="absolute bottom-32 right-20 text-pink-300 w-32 h-32 opacity-70 animate-bounce" />
                <div className="absolute top-40 right-40 w-48 h-48 bg-white opacity-20 rounded-full blur-3xl"></div>
                <div className="absolute bottom-20 left-40 w-64 h-64 bg-pink-400 opacity-30 rounded-full blur-3xl"></div>

                <div className="bg-white/90 backdrop-blur-md p-10 rounded-[3rem] shadow-2xl border-4 border-white text-center z-10 max-w-2xl transform transition-transform hover:scale-105">
                    <h1 className="text-6xl font-extrabold text-transparent bg-clip-text bg-gradient-to-r from-pink-500 to-orange-500 mb-8 drop-shadow-sm">
                        EduVision Explorer!
                    </h1>
                    <DogMascot message="Woof! Ready to learn about some cool things?" state="excited" />
                    <button onClick={startSession} className="mx-auto mt-10 flex items-center gap-3 bg-gradient-to-r from-yellow-400 to-orange-500 text-white text-4xl font-black py-6 px-12 rounded-full hover:scale-105 hover:rotate-3 transition-all shadow-[0_10px_0_rgb(194,65,12)] border-4 border-yellow-200">
                        <PlayCircle size={48} className="text-yellow-100" /> Let's Play!
                    </button>
                </div>
            </div>
        );
    }

    if (status === 'finished') {
         let earnedStars = 1;
         if (images.length > 0) {
             const ratio = score / images.length;
             if (ratio === 1) earnedStars = 3;
             else if (ratio >= 0.5) earnedStars = 2;
         }
         
         const starElements = Array(3).fill(0).map((_, i) => (
             <Star key={i} className={`w-24 h-24 ${i < earnedStars ? 'fill-yellow-400 text-yellow-500 animate-pulse drop-shadow-md' : 'text-gray-300 fill-gray-200'} mx-2`} />
         ));

         return (
            <div className="flex flex-col items-center justify-center min-h-screen p-8 bg-gradient-to-tr from-green-400 via-teal-400 to-blue-500">
                <div 
                    className="bg-white/95 backdrop-blur-lg p-12 rounded-[3.5rem] shadow-2xl border-[6px] border-yellow-400 text-center animate-bounce flex flex-col items-center max-w-2xl"
                    style={{ animationIterationCount: 2 }}
                >
                    <div className="flex justify-center mb-6">
                        {starElements}
                    </div>
                    <h1 className="text-6xl font-black text-green-500 mb-8">You're a Star!</h1>
                    
                    <div className="bg-gradient-to-br from-green-100 to-teal-100 p-8 rounded-3xl border-4 border-green-300 mb-8 w-full shadow-inner">
                        <p className="text-2xl font-bold text-teal-800 mb-2 uppercase tracking-wide">Final Report</p>
                        <p className="text-4xl font-extrabold text-green-600">You got {score} out of {images.length} right on the first try!</p>
                    </div>

                    <DogMascot message="You did amazing! I'm so proud of you!" state="excited" />
                    
                    <button onClick={startSession} className="mx-auto mt-10 flex items-center gap-3 bg-gradient-to-r from-blue-500 to-cyan-400 text-white text-3xl font-black py-6 px-12 rounded-full hover:scale-110 transition-transform shadow-[0_8px_0_rgb(30,58,138)] border-4 border-cyan-200">
                        <RefreshCw size={40} className="text-cyan-100" /> Play Again!
                    </button>
                </div>
            </div>
        );
    }

    const currentImg = images[currentIndex];

    return (
        <div className="flex flex-col items-center min-h-screen px-4 md:px-8 py-10 bg-gradient-to-br from-indigo-100 via-purple-100 to-pink-100">
            {/* Progress Bar Area */}
            <div className="w-full max-w-5xl flex justify-between items-center mb-10 bg-white p-6 rounded-full shadow-lg border-[5px] border-purple-200 relative overflow-hidden">
                 <div className="absolute top-0 left-0 w-full h-full bg-gradient-to-r from-transparent to-white opacity-50 pointer-events-none"></div>
                 <h2 className="text-3xl font-black text-purple-600 px-6 drop-shadow-sm whitespace-nowrap">Item {currentIndex + 1} of {images.length}</h2>
                 <div className="h-8 w-full max-w-md bg-purple-100 rounded-full overflow-hidden mr-4 shadow-inner border-2 border-purple-200">
                     <div className="h-full bg-gradient-to-r from-pink-400 to-orange-400 transition-all duration-700 ease-out rounded-full relative" style={{width: `${((currentIndex+1)/images.length)*100}%`}}>
                        <div className="absolute top-0 right-0 h-full w-full bg-[linear-gradient(45deg,rgba(255,255,255,.15)_25%,transparent_25%,transparent_50%,rgba(255,255,255,.15)_50%,rgba(255,255,255,.15)_75%,transparent_75%,transparent)] bg-[length:20px_20px] animate-[slide_1s_linear_infinite]"></div>
                     </div>
                 </div>
            </div>

            <div className="flex flex-col lg:flex-row gap-12 w-full max-w-6xl items-stretch">
                
                {/* Left Side: Image Area */}
                <div className="flex-1 flex flex-col items-center justify-center w-full">
                     <div className="bg-white p-2 rounded-[3.5rem] shadow-2xl border-8 border-yellow-400 flex w-full aspect-square relative transform transition-transform duration-500 hover:rotate-2 hover:scale-105 overflow-hidden">
                         <div className="absolute top-4 left-4 bg-pink-500 text-white rounded-full w-16 h-16 flex items-center justify-center font-black text-2xl shadow-lg transform -rotate-12 border-4 border-white z-20">
                            #{currentIndex + 1}
                         </div>
                         <img src={currentImg?.image_url} alt="Educational Item" className="w-full h-full object-cover rounded-[3rem] z-10" />
                     </div>
                     
                     {(status === 'active' || status === 'checking' || status === 'incorrect') && (
                         <div className="w-full mt-6">
                             <h3 className="text-2xl font-black text-purple-600 mb-4 text-center">What is in the picture?</h3>
                             <div className="grid grid-cols-2 gap-4">
                                 {GUESS_CATEGORIES.map(cat => (
                                     <button 
                                         key={cat.label}
                                         className={`flex flex-col items-center justify-center p-4 rounded-[2rem] text-white font-black text-xl md:text-2xl bg-gradient-to-br ${cat.color} border-[4px] border-white transition-all ${status === 'checking' ? 'opacity-50 cursor-not-allowed transform translate-y-1' : 'hover:-translate-y-1 active:translate-y-2'}`}
                                         style={{ boxShadow: status === 'checking' ? 'none' : `0 8px 0 ${cat.shadow}` }}
                                         onClick={() => status === 'active' && recognizeImage(cat.label)}
                                         disabled={status !== 'active'}
                                     >
                                         <span className="text-4xl mb-2">{cat.emoji}</span>
                                         {cat.label}
                                     </button>
                                 ))}
                             </div>
                         </div>
                     )}
                </div>

                {/* Right Side: Mascot and Results */}
                <div className="flex-1 w-full flex flex-col justify-center">
                     {status === 'loading' && (
                         <div className="animate-pulse">
                            <DogMascot message="Loading up the game... Here we go!" state="happy" />
                         </div>
                     )}
                     {status === 'checking' && (
                         <div className="animate-pulse">
                            <DogMascot message="Checking my encyclopedia... Hang tight!" state="thinking" />
                         </div>
                     )}
                     {status === 'incorrect' && (
                         <div className="animate-[wiggle_0.5s_ease-in-out]">
                            <DogMascot message="Woof! Not quite! Try a different category!" state="confused" />
                         </div>
                     )}
                     
                     {status === 'matched' && (
                         <div className="flex flex-col gap-6 w-full animate-[wiggle_1s_ease-in-out]">
                             <DogMascot message={`Woof! I know! It's a ${currentResult.child_category}!`} state="excited" />
                             
                             <div className="bg-gradient-to-br from-cyan-100 to-blue-200 p-8 rounded-[3rem] border-8 border-cyan-400 shadow-2xl relative">
                                 <Sparkles className="absolute -top-4 -right-4 text-cyan-500 w-12 h-12 bg-white rounded-full p-2 shadow-md border-2 border-cyan-200" />
                                 
                                 <div className="bg-white rounded-3xl p-6 shadow-inner border-4 border-cyan-100 mb-4">
                                     <h3 className="text-lg font-black text-orange-500 uppercase tracking-widest mb-1">Family Category</h3>
                                     <p className="text-3xl font-extrabold text-blue-600">{currentResult.parent_category}</p>
                                 </div>

                                 <div className="bg-white rounded-3xl p-6 shadow-inner border-4 border-pink-200 mb-6">
                                     <h3 className="text-lg font-black text-pink-500 uppercase tracking-widest mb-1">Specific Item</h3>
                                     <p className="text-4xl font-extrabold text-pink-600 capitalize">{currentResult.child_category.replace('Unknown ', '')}</p>
                                 </div>
                                 
                                 <div className="bg-white rounded-3xl p-6 shadow-inner border-4 border-cyan-100 relative">
                                     <div className="absolute -top-5 left-6 bg-orange-500 text-white px-4 py-1 rounded-full text-sm font-black uppercase shadow-md border-2 border-white">Fun Fact!</div>
                                     <p className="text-2xl font-bold text-gray-700 leading-snug pt-3 flex items-start">
                                         <span className="text-4xl mr-3 floating-emoji align-top">💡</span> 
                                         {currentResult.fun_fact}
                                     </p>
                                 </div>
                             </div>

                             <button onClick={nextImage} className="self-end flex items-center justify-center gap-3 bg-gradient-to-r from-green-400 to-emerald-600 text-white font-black text-3xl py-6 px-10 rounded-full shadow-[0_10px_0_rgb(22,101,52)] hover:-translate-y-2 hover:shadow-[0_16px_0_rgb(22,101,52)] active:translate-y-2 active:shadow-none transition-all border-[6px] border-green-200 mt-6 w-full md:w-auto">
                                 Next Item! <ArrowRight size={36} strokeWidth={3} className="text-green-100" />
                             </button>
                         </div>
                     )}
                     
                     {status === 'active' && (
                         <div className="opacity-90 transform hover:scale-105 transition-transform duration-300">
                            <DogMascot message="Which category is this? Make your best guess!" state="happy" />
                         </div>
                     )}
                </div>
            </div>
            
            <style jsx>{`
                @keyframes slide {
                    from { background-position: 0 0; }
                    to { background-position: -20px -20px; }
                }
                @keyframes wiggle {
                    0%, 100% { transform: rotate(-1deg); }
                    50% { transform: rotate(1.5deg); }
                }
                .floating-emoji {
                    animation: bouncyfloat 2s ease-in-out infinite;
                }
                @keyframes bouncyfloat {
                    0%, 100% { transform: translateY(0); }
                    50% { transform: translateY(-10px); }
                }
            `}</style>
        </div>
    );
};

export default DiscoverySession;

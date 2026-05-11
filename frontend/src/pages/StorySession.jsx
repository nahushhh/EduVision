import React, { useState, useEffect } from 'react';
import axios from 'axios';
import DogMascot from '../components/DogMascot';
import { ArrowRight, Star, Sparkles, Crosshair } from 'lucide-react';

const API_BASE = 'http://localhost:8000/api/story';

const StorySession = ({ onReturnHome }) => {
    const [scenarios, setScenarios] = useState([]);
    const [status, setStatus] = useState('loading'); // loading, selecting, scene1, scene2, finished
    const [currentScenario, setCurrentScenario] = useState(null);
    const [currentSceneIndex, setCurrentSceneIndex] = useState(0);
    const [feedback, setFeedback] = useState(null);

    useEffect(() => {
        const fetchScenarios = async () => {
            try {
                const res = await axios.get(`${API_BASE}/scenarios`);
                setScenarios(res.data.scenarios);
                setStatus('selecting');
            } catch (err) {
                console.error("Failed to load scenarios", err);
                setStatus('error');
            }
        };
        fetchScenarios();
    }, []);

    const startScenario = (scenario) => {
        setCurrentScenario(scenario);
        setCurrentSceneIndex(0);
        setFeedback(null);
        setStatus('scene1');
    };

    const currentScene = currentScenario?.scenes ? currentScenario.scenes[currentSceneIndex] : null;

    const handleImageClick = async (e) => {
        if (status !== 'scene2') return;
        
        const rect = e.target.getBoundingClientRect();
        const x = e.clientX - rect.left;
        const y = e.clientY - rect.top;
        
        const click_x_ratio = x / rect.width;
        const click_y_ratio = y / rect.height;
        
        setStatus('evaluating');
        
        try {
            const res = await axios.post(`${API_BASE}/evaluate`, {
                story_id: currentScenario.id,
                scene_id: currentScene.scene_id,
                click_x_ratio: click_x_ratio,
                click_y_ratio: click_y_ratio
            });
            
            if (res.data.is_correct) {
                setFeedback({ isCorrect: true, message: res.data.message });
                setTimeout(() => {
                    if (currentSceneIndex < currentScenario.scenes.length - 1) {
                        setCurrentSceneIndex(currentSceneIndex + 1);
                        setStatus('scene1');
                        setFeedback(null);
                    } else {
                        setStatus('finished');
                    }
                }, 3000);
            } else {
                setFeedback({ isCorrect: false, message: res.data.message });
                setStatus('scene2');
            }
        } catch (err) {
            console.error("Evaluation failed", err);
            setStatus('scene2');
        }
    };

    if (status === 'loading') {
        return (
            <div className="flex flex-col items-center justify-center w-full h-full p-12">
                <div className="animate-float">
                    <DogMascot message="Loading stories..." state="thinking" />
                </div>
            </div>
        );
    }

    if (status === 'selecting') {
        return (
            <div className="flex flex-col items-center w-full h-full p-12">
                <h1 className="text-[5rem] font-black text-white mb-16 drop-shadow-md animate-popIn">Choose a Story Adventure!</h1>
                <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-12 w-full max-w-[100rem]">
                    {scenarios.map((s, index) => (
                        <div 
                            key={s.id} 
                            onClick={() => startScenario(s)} 
                            className="bg-white p-10 rounded-[3rem] shadow-xl border-8 border-yellow-300 cursor-pointer transform transition hover:-translate-y-4 hover:shadow-2xl flex flex-col justify-between animate-fadeInUp group"
                            style={{ animationDelay: `${index * 0.1}s`, opacity: 0 }}
                        >
                            <div>
                                <h2 className="text-4xl font-black text-orange-500 mb-6 group-hover:text-orange-600 transition-colors">{s.title}</h2>
                                <p className="text-2xl text-gray-600 font-medium leading-relaxed">{s.scenes[0].description}</p>
                            </div>
                            <div className="mt-10 flex justify-between items-center bg-orange-50 p-4 rounded-2xl border-2 border-orange-100">
                                <span className="text-lg font-black text-orange-400 uppercase tracking-widest">{s.scenes.length} {s.scenes.length === 1 ? 'Scene' : 'Scenes'}</span>
                                <span className="text-3xl group-hover:animate-wiggle">📖 ✨</span>
                            </div>
                        </div>
                    ))}
                </div>
            </div>
        );
    }

    if (status === 'scene1') {
        return (
            <div className="flex flex-col items-center justify-center w-full h-full p-12 animate-popIn">
                <div className="w-full max-w-[100rem]">
                    <h2 className="text-[4rem] font-black text-white mb-12 drop-shadow-md text-center">{currentScenario.title} {currentScenario.scenes.length > 1 ? `(Part ${currentSceneIndex + 1})` : ''}</h2>
                    
                    <div className="flex flex-col lg:flex-row gap-12 items-stretch w-full">
                        {/* LEFT: Scene Image */}
                        <div className="flex-1 w-full rounded-[3rem] overflow-hidden border-8 border-yellow-300 shadow-2xl relative flex items-center justify-center bg-white max-h-[500px]">
                             <img src={currentScene.context_image_url} alt="Story Context" className="w-full h-full object-contain" onError={(e) => e.target.style.display='none'} />
                             <span className="absolute text-gray-400 font-bold z-[-1] text-2xl">Place '{currentScene.context_image_url.split('/').pop()}' in test_images/</span>
                        </div>
                        
                        {/* RIGHT: Story and Question */}
                        <div className="flex-1 flex flex-col justify-center items-center bg-white/20 backdrop-blur-sm p-12 rounded-[3rem] border-4 border-white/40 shadow-xl">
                            <div className="w-full max-w-2xl mb-12">
                                <DogMascot message={currentScene.description} state="excited" />
                            </div>
                            <button onClick={() => setStatus('scene2')} className="flex items-center gap-4 bg-yellow-400 text-orange-900 font-black text-4xl py-8 px-16 rounded-full shadow-[0_12px_0_rgb(217,119,6)] hover:-translate-y-2 hover:shadow-[0_16px_0_rgb(217,119,6)] active:translate-y-2 active:shadow-none transition-all border-4 border-yellow-200 w-full justify-center">
                                Let's Help! <ArrowRight size={48} />
                            </button>
                        </div>
                    </div>
                </div>
            </div>
        );
    }

    if (status === 'scene2' || status === 'evaluating') {
        return (
            <div className="flex flex-col items-center justify-center w-full h-full p-12 animate-popIn">
                <div className="w-full max-w-[100rem] relative">
                    <h2 className="text-[4rem] font-black text-white mb-12 drop-shadow-md text-center">Tap on the correct answer!</h2>
                    
                    <div className="flex flex-col lg:flex-row gap-12 items-stretch w-full">
                        {/* LEFT: Interactive Image */}
                        <div className="flex-[1.5] w-full relative bg-white rounded-[3rem] border-8 border-yellow-300 shadow-2xl cursor-crosshair overflow-hidden max-h-[600px] flex items-center justify-center">
                             <img 
                                src={currentScene.interactive_image_url} 
                                alt="Options" 
                                className={`w-full h-full object-contain z-10 ${status === 'evaluating' ? 'opacity-50' : 'hover:opacity-90 transition-opacity'}`}
                                onClick={handleImageClick}
                                onError={(e) => e.target.style.display='none'}
                             />
                             <span className="absolute text-gray-400 font-bold z-0 text-2xl">Place '{currentScene.interactive_image_url.split('/').pop()}' in test_images/</span>
                             
                             {status === 'evaluating' && (
                                 <div className="absolute inset-0 z-20 flex items-center justify-center bg-black/20">
                                     <div className="bg-white p-8 rounded-full animate-pulse shadow-2xl">
                                         <Crosshair size={64} className="text-blue-500 animate-spin-slow" />
                                     </div>
                                 </div>
                             )}
                        </div>
                        
                        {/* RIGHT: Feedback Bar */}
                        <div className="flex-1 flex flex-col justify-center items-center bg-white/20 backdrop-blur-sm p-12 rounded-[3rem] border-4 border-white/40 shadow-xl">
                            <div className="w-full max-w-2xl">
                                {feedback ? (
                                    <DogMascot 
                                        message={feedback.message} 
                                        state={feedback.isCorrect ? 'happy' : 'confused'} 
                                    />
                                ) : (
                                    <DogMascot message="Tap on the correct item to help!" state="happy" />
                                )}
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        );
    }

    if (status === 'finished') {
        return (
            <div className="flex flex-col items-center justify-center w-full h-full p-12 animate-popIn">
                <div className="w-full max-w-4xl flex flex-col items-center">
                    <h1 className="text-[6rem] font-black text-white mb-10 flex justify-center drop-shadow-xl text-center">
                        <Sparkles className="w-20 h-20 text-yellow-300 mr-6"/> Story Complete! <Sparkles className="w-20 h-20 text-yellow-300 ml-6"/>
                    </h1>
                    <div className="flex justify-center w-full mb-12">
                        <DogMascot message={`Great job finishing ${currentScenario.title}! You saved the day!`} state="excited" />
                    </div>
                    <button onClick={() => setStatus('selecting')} className="mx-auto flex items-center gap-4 bg-yellow-400 text-orange-900 text-4xl font-black py-8 px-16 rounded-[3rem] hover:scale-110 transition-transform shadow-[0_12px_0_rgb(217,119,6)] border-4 border-yellow-200">
                        Play Another Story
                    </button>
                </div>
            </div>
        );
    }
    
    return null;
};

export default StorySession;

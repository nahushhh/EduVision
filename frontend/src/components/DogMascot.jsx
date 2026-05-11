import React from 'react';

const DogMascot = ({ message, state }) => {
  return (
    <div className="flex flex-col items-center p-4 m-4">
      <div className="relative w-48 h-48 drop-shadow-2xl">
        <img 
            src="/dog_mascot.png" 
            alt="EduVision Mascot" 
            className={`w-full h-full object-contain transition-transform duration-500 ${state === 'excited' ? 'scale-110' : ''}`} 
        />
        {/* Thinking marks */}
        {state === 'thinking' && (
            <div className="absolute top-0 right-0 text-5xl font-black text-blue-500 animate-bounce drop-shadow-md">
                ?
            </div>
        )}
      </div>

      <div className="mt-4 text-center w-full max-w-md px-4">
        <p className="text-2xl font-bold text-blue-900 bg-white/90 backdrop-blur-sm px-8 py-4 rounded-[2rem] border-4 border-blue-300 shadow-xl leading-tight">
          "{message}"
        </p>
      </div>
    </div>
  );
};

export default DogMascot;

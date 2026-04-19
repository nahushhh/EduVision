import React from 'react';

const DogMascot = ({ message, state }) => {
  return (
    <div className="flex flex-col items-center bg-white p-6 rounded-[3rem] border-[6px] border-orange-400 shadow-[0_8px_30px_rgb(0,0,0,0.12)] m-4 w-full">
      <div className="relative w-32 h-32 bg-gradient-to-b from-orange-300 to-orange-400 rounded-full flex items-center justify-center shadow-inner border-4 border-orange-200">
        {/* Ears */}
        <div className={`absolute -top-2 -left-3 w-10 h-16 bg-gradient-to-b from-orange-400 to-orange-500 rounded-full origin-bottom rotate-[-25deg] transition-all duration-500 ${state === 'excited' ? 'rotate-[-35deg] scale-110' : ''}`}></div>
        <div className={`absolute -top-2 -right-3 w-10 h-16 bg-gradient-to-b from-orange-400 to-orange-500 rounded-full origin-bottom rotate-[25deg] transition-all duration-500 ${state === 'excited' ? 'rotate-[35deg] scale-110' : ''}`}></div>
        
        {/* Eyes */}
        <div className="absolute top-10 left-8 w-4 h-4 bg-gray-900 rounded-full flex justify-end p-[2px]">
            {/* Catchlight */}
            <div className="w-1.5 h-1.5 bg-white rounded-full"></div>
        </div>
        <div className="absolute top-10 right-8 w-4 h-4 bg-gray-900 rounded-full flex justify-end p-[2px]">
            {/* Catchlight */}
            <div className="w-1.5 h-1.5 bg-white rounded-full"></div>
        </div>
        
        {/* Nose Area */}
        <div className="absolute bottom-6 w-14 h-10 bg-orange-200 rounded-3xl flex justify-center pt-1 border-2 border-orange-300">
            {/* Nose */}
            <div className="w-6 h-4 bg-gray-900 rounded-[50%]"></div>
        </div>

        {/* Mouth/Tongue */}
        {(state === 'excited' || state === 'happy' || true) && (
          <div className="absolute bottom-1 w-8 h-8 bg-pink-500 rounded-b-full shadow-inner border-2 border-pink-600 flex justify-center">
            {/* Tongue line */}
            <div className="w-0.5 h-4 bg-pink-700 mt-1 opacity-50"></div>
          </div>
        )}
        
        {/* Thinking marks */}
        {state === 'thinking' && (
            <div className="absolute -top-6 -right-6 text-2xl font-bold text-gray-400 animate-bounce">
                ?
            </div>
        )}
      </div>

      <div className="mt-8 text-center w-full px-4">
        <p className="text-2xl font-bold text-blue-900 bg-blue-50 px-6 py-4 rounded-[2rem] border-2 border-blue-200 shadow-sm leading-tight italic">
          "{message}"
        </p>
      </div>
    </div>
  );
};

export default DogMascot;

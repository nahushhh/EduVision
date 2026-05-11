import React from 'react';

const NavBar = ({ onReturnHome }) => {
  return (
    <nav className="w-full bg-white shadow-md px-8 py-4 flex justify-between items-center z-50 sticky top-0 border-b-4 border-yellow-400 animate-fadeInUp">
      <div 
        className="flex items-center gap-4 cursor-pointer group"
        onClick={onReturnHome}
      >
        <img src="/dog_mascot.png" alt="EduVision Logo" className="w-12 h-12 object-contain group-hover:animate-wiggle" />
        <h1 className="text-3xl font-black text-blue-600 tracking-wide drop-shadow-sm group-hover:scale-105 transition-transform">
          Edu<span className="text-pink-500">Vision</span>
        </h1>
      </div>
      

    </nav>
  );
};

export default NavBar;

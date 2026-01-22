import React from 'react';

const Navbar = () => {
  return (
    <header className="h-16 px-4 md:px-8 flex items-center bg-slate-900 border-b border-slate-800 fixed top-0 right-0 left-0 md:left-64 z-30 shadow-md">
      <div className="md:hidden flex items-center">
        <div className="text-lg font-bold text-white tracking-tight">
          Portal
        </div>
      </div>
      <div className="ml-auto flex items-center gap-4">
        <span className="text-xs md:text-sm font-semibold text-gray-200 px-3 py-1 bg-slate-800/50 border border-slate-700/50 rounded-full">
          Welcome, XYZ
        </span>
      </div>
    </header>
  );
};

export default Navbar;

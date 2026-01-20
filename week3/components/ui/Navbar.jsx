import React from 'react';

const Navbar = () => {
  return (
    <nav className="h-16 bg-slate-900 flex items-center justify-between px-4 z-30 shadow">
      <div className="flex items-center md:hidden">
        <button className="text-gray-400 hover:text-white p-1">
          <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 6h16M4 12h16M4 18h16" /></svg>
        </button>
      </div>
    </nav>
  );
};

export default Navbar;

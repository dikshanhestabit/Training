import React from 'react';
import Link from 'next/link';

const Sidebar = () => {
    return (
        <aside className="w-64 bg-slate-700 h-screen fixed top-0 left-0 flex flex-col z-40 font-sans shadow-lg">
            <div className="h-16 flex items-center justify-center border-b border-slate-800 bg-slate-900">
                <Link href="/" className="font-bold text-xl text-white tracking-wide no-underline hover:text-gray-200">
                    STUDENT PORTAL
                </Link>
            </div>

            <div className="flex-1 py-6 space-y-1">
                <Link
                    href="/"
                    className="block px-6 py-3 text-gray-300 hover:text-white hover:bg-slate-800 transition-colors no-underline"
                >
                    <span className="font-medium">Home Page</span>
                </Link>

                <Link
                    href="/dashboard"
                    className="block px-6 py-3 text-gray-300 hover:text-white hover:bg-slate-800 transition-colors no-underline"
                >
                    <span className="font-medium">Dashboard</span>
                </Link>

                <Link
                    href="/dashboard/profile"
                    className="block px-6 py-3 text-gray-300 hover:text-white hover:bg-slate-800 transition-colors no-underline"
                >
                    <span className="font-medium">My Profile</span>
                </Link>

                <Link
                    href="/about"
                    className="block px-6 py-3 text-gray-300 hover:text-white hover:bg-slate-800 transition-colors no-underline"
                >
                    <span className="font-medium">About Us</span>
                </Link>
            </div>
        </aside>
    );
};

export default Sidebar;

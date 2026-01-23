"use client";

import Link from "next/link";
import Image from "next/image";
import { Button, Card } from "@/components/ui";
import { motion } from "framer-motion";

/**
 * LANDING PAGE COMPONENT
 */
export default function LandingPage() {
  return (
    <div className="min-h-screen bg-white font-sans text-gray-900">

      {/* SECTION 1: NAVIGATION BAR */}
      <nav className="flex items-center justify-between px-6 py-4 border-b border-gray-200">
        {/* The Portal Name */}
        <div className="text-xl font-bold text-gray-800 cursor-default">
          Student Portal
        </div>

        {/* Links to other pages */}
        <div className="hidden md:flex gap-6 items-center text-sm">
          <Link href="/about" className="text-gray-600 hover:text-black">About</Link>
          <Link href="/dashboard" className="text-gray-600 hover:text-black">Dashboard</Link>
          <Link href="/login">
            <Button variant="primary" className="px-5 py-1.5 text-xs">Login</Button>
          </Link>
        </div>
      </nav>

      {/* SECTION 2: HERO SECTION */}
      <section className="px-6 py-12 md:py-20 bg-gray-50 border-b border-gray-200 overflow-hidden">
        <div className="max-w-6xl mx-auto flex flex-col md:flex-row items-center gap-10">

          {/* Left Side: Text and Buttons (Animated) */}
          <motion.div
            initial={{ opacity: 0, y: 20 }}     // Starts invisible and slightly lower
            animate={{ opacity: 1, y: 0 }}      // Fades in and moves up to its spot
            transition={{ duration: 0.6 }}      // Takes 0.6 seconds
            className="flex-1 space-y-4 text-center md:text-left"
          >
            <h1 className="text-3xl md:text-5xl font-bold text-gray-900">
              Manage Your Academic Life with Ease
            </h1>
            <p className="text-base md:text-lg text-gray-700">
              A simple and effective portal for tracking your assignments, grades, and attendance.
              Stay organized and focused on your studies.
            </p>

            {/* Action Buttons */}
            <div className="flex flex-col sm:flex-row gap-3 justify-center md:justify-start pt-2">
              <Link href="/dashboard">
                <Button variant="secondary" className="w-full sm:w-auto">Go to Dashboard</Button>
              </Link>
              <Link href="/about">
                <Button variant="secondary" className="w-full sm:w-auto">Learn More</Button>
              </Link>
            </div>
          </motion.div>

          {/* Hero Image (Animated) */}
          <motion.div
            initial={{ opacity: 0, scale: 0.95 }}
            animate={{ opacity: 1, scale: 1 }}
            transition={{ duration: 0.8, delay: 0.2 }}
            className="flex-1 w-full max-w-lg"
          >
            <div className="border border-gray-300 rounded shadow-sm overflow-hidden bg-white">
              <Image
                src="https://thumbs.dreamstime.com/b/student-surrounded-symbols-knowledge-ideas-perfect-educational-inspirational-visuals-smart-illustration-375967148.jpg"
                alt="Student Illustration"
                width={1000}
                height={600}
                priority
              />
            </div>
          </motion.div>
        </div>
      </section>

      {/* SECTION 3: CORE FEATURES
          
      */}
      <section className="px-6 py-16 bg-white">
        <div className="max-w-6xl mx-auto">
          <h2 className="text-2xl font-bold text-center mb-10">Core Features</h2>

          <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
            {[
              { title: "Assignment Tracker", desc: "Keep a list of all your upcoming homework and project deadlines." },
              { title: "Attendance Monitor", desc: "View your attendance percentage for each subject easily." },
              { title: "Grade Reports", desc: "Check your scores and track your GPA throughout the semester." }
            ].map((feature, i) => (
              /* Each card grows a little when you put your mouse over it */
              <motion.div
                key={i}
                whileHover={{ scale: 1.02 }}
                transition={{ type: "spring", stiffness: 400, damping: 10 }}
              >
                <Card title={feature.title} className="h-full">
                  <p className="text-gray-600 text-sm">{feature.desc}</p>
                </Card>
              </motion.div>
            ))}
          </div>
        </div>
      </section>

      {/* SECTION 4: TESTIMONIALS
          
      */}
      <section className="px-6 py-16 bg-gray-50 border-y border-gray-200">
        <div className="max-w-6xl mx-auto">
          <h2 className="text-2xl font-bold text-center mb-10">What Students Say</h2>

          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6">
            {[
              { name: "abc", text: "It helps me stay on top of my assignments. Simple and useful." },
              { name: "def", text: "The attendance tracker is my favorite part. No more guessing!" },
              { name: "ghi", text: "Very clear and easy to navigate. Does exactly what it says." }
            ].map((t, idx) => (
              <div key={idx} className="bg-white p-6 border border-gray-200 rounded text-sm">
                <p className="mb-4">"{t.text}"</p>
                <p className="font-bold text-gray-800">- {t.name}</p>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* SECTION 5: FOOTER
          
      */}
      <footer className="px-6 py-10 bg-gray-100 text-gray-600 border-t border-gray-200">
        <div className="max-w-6xl mx-auto text-center">
          <div className="text-xs">
            © {new Date().getFullYear()} All Rights Reserved.
          </div>
        </div>
      </footer>
    </div>
  );
}

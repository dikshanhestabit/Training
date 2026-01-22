import Link from "next/link";
import { Button, Card } from "@/components/ui";

/**
 * ABOUT PAGE COMPONENT
 * This page gives more information about why the portal was built.
 */
export default function AboutPage() {
    return (
        <div className="min-h-screen bg-gray-50 font-sans text-gray-900 flex flex-col">

            {/* NAVIGATION BAR
                A simple top bar with the portal name and a back button.
            */}
            <nav className="flex items-center justify-between px-6 py-4 bg-white border-b border-gray-200 sticky top-0 z-50">
                <div className="text-xl font-bold text-gray-800 cursor-default">
                    Student Portal
                </div>
                <Link href="/">
                    <Button variant="secondary" className="text-sm">Back Home</Button>
                </Link>
            </nav>

            {/* MAIN CONTENT AREA
                Where the story of the portal is told.
            */}
            <main className="max-w-3xl mx-auto px-6 py-12 flex-grow">
                <div className="space-y-6">
                    <h1 className="text-3xl font-bold">About This Portal</h1>

                    <p className="text-gray-700 leading-relaxed">
                        This Student Portal is a project built to help students manage their day-to-day academic life.
                        It focuses on three main areas: assignments, attendance, and grades.
                    </p>

                    <h2 className="text-xl font-bold pt-4">Why we built it</h2>
                    <p className="text-gray-700">
                        Managing multiple subjects can be hard. This portal gives you a single place to see what's due,
                        how often you've attended classes, and how you're performing.
                    </p>

                    {/* Features Card: Listing specific benefits */}
                    <Card title="Portal Features">
                        <ul className="list-disc ml-5 space-y-2 text-sm text-gray-700">
                            <li>Keep track of all assignments in one place.</li>
                            <li>Monitor your attendance percentage easily.</li>
                            <li>View and manage your academic profile.</li>
                            <li>Simple and clean interface for students.</li>
                        </ul>
                    </Card>
                </div>
            </main>

            {/* FOOTER
                The copyright line at the very bottom.
            */}
            <footer className="mt-auto py-8 bg-white border-t border-gray-200 text-center text-xs text-gray-500">
                © {new Date().getFullYear()} All Rights Reserved.
            </footer>
        </div>
    );
}

import Link from "next/link";
import { Button } from "@/components/ui";

export default function LandingPage() {
  return (
    <div className="min-h-screen flex flex-col items-center justify-center p-10 bg-gray-50 text-black text-center">
      <div className="max-w-xl space-y-4">
        <h1 className="text-4xl font-bold">Student Portal</h1>
        <p className="text-gray-600">
          This is a portal for students to manage their assignments, attendance, and profile.
        </p>
        <div className="flex justify-center gap-4 pt-4">
          <Link href="/dashboard">
            <Button>Go to Dashboard</Button>
          </Link>
          <Link href="/about">
            <Button variant="outline">About Us</Button>
          </Link>
        </div>
      </div>
    </div>
  );
}

import Link from "next/link";
import { Button, Card } from "@/components/ui";

export default function AboutPage() {
    return (
        <div className="min-h-screen flex flex-col items-center justify-center p-10 bg-gray-50 text-black text-center">
            <div className="max-w-xl w-full">
                <h1 className="text-2xl font-bold mb-4">About the Portal</h1>
                <p className="mb-6 text-gray-700">
                    The Student Portal is a simple tool created for students to keep track of their academic activities like assignments and attendance.
                </p>

                <div className="space-y-4">
                    <Card title="Portal Features" className="text-left">
                        <ul className="list-disc ml-5 text-sm space-y-1 text-gray-600">
                            <li>Tracking your daily assignments</li>
                            <li>Viewing your monthly attendance</li>
                            <li>Checking your academic grades</li>
                        </ul>
                    </Card>

                    <div className="pt-6 flex justify-center">
                        <Link href="/">
                            <Button variant="outline">Back to Home</Button>
                        </Link>
                    </div>
                </div>
            </div>
        </div>
    );
}

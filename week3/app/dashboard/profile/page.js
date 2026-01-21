import { Card, Badge, Button } from "@/components/ui";

export default function ProfilePage() {
    return (
        <div className="p-4 space-y-6 bg-white text-black min-h-screen">
            <div className="border-b pb-4">
                <h2 className="text-xl font-bold">User Profile</h2>
                <p className="text-sm text-gray-500">Manage your basic student information here.</p>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                <Card title="Basic Info">
                    <div className="space-y-4">
                        <div className="text-sm">
                            <p><strong>Name:</strong> XYZ</p>
                            <p><strong>Email:</strong> xyz@gmail.com</p>
                            <p><strong>Roll No:</strong> XYZ-2024-001</p>
                            <p><strong>Semester:</strong> 8th Semester</p>
                        </div>
                        <div className="pt-2">
                            <Badge variant="success">Active</Badge>
                        </div>
                    </div>
                </Card>

                <Card title="Contact Info">
                    <div className="space-y-4">
                        <div className="text-sm">
                            <p><strong>Phone:</strong> +91 **********</p>
                            <p><strong>Address:</strong> Not provided</p>
                        </div>
                        <div className="flex justify-end">
                            <Button variant="outline" className="text-xs">Edit</Button>
                        </div>
                    </div>
                </Card>
            </div>
        </div>
    );
}

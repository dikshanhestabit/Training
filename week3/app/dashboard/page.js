import { Card, Button, Input, Badge } from "@/components/ui";

export default function DashboardPage() {
    return (
        <div className="space-y-6">
            <h2 className="text-2xl font-bold text-gray-800 tracking-tight">Dashboard Overview</h2>

            {/* Colorful Stat Cards from Day 2 */}
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
                <Card title="Assignments" variant="primary">
                    <p className="text-3xl font-bold">12</p>
                    <p className="text-sm opacity-80">Active Tasks</p>
                </Card>

                <Card title="Attendance" variant="warning">
                    <p className="text-3xl font-bold">94%</p>
                    <p className="text-sm opacity-80">This Month</p>
                </Card>

                <Card title="Grade Point" variant="success">
                    <p className="text-3xl font-bold">3.8</p>
                    <p className="text-sm opacity-80">Average GPA</p>
                </Card>

                <Card title="Alerts" variant="danger">
                    <p className="text-3xl font-bold">2</p>
                    <p className="text-sm opacity-80">Urgent Notices</p>
                </Card>
            </div>

            {/* Restored Task 2 Sections below the cards */}
            <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
                <Card title="Search & Actions">
                    <div className="space-y-4">
                        <p className="text-sm text-gray-600">Use this section to search for library resources.</p>
                        <div className="flex flex-col gap-2">
                            <Input placeholder="Enter resource name..." />
                            <div className="flex items-center gap-2">
                                <Button>Search</Button>
                                <Badge variant="info">Library System Online</Badge>
                            </div>
                        </div>
                    </div>
                </Card>

                <Card title="Recent Activity">
                    <div className="space-y-4">
                        <p className="text-sm text-gray-600 text-left">Current status of your enrollment.</p>
                        <div className="p-3 bg-gray-50 border rounded text-sm text-gray-500 italic">
                            No recent activity to display.
                        </div>
                    </div>
                </Card>
            </div>
        </div>
    );
}

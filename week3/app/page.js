import { Button, Card, Badge, Input } from "@/components/ui";

export default function Home() {
  return (
    <div className="space-y-6">
      {/* 4 Simple Colored Stat Cards as seen in the reference layout */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        <Card title="Assignments" variant="primary">
          <p className="text-sm">12 Active Tasks</p>
        </Card>

        <Card title="Attendance" variant="warning">
          <p className="text-sm">94% This Month</p>
        </Card>

        <Card title="Grade Point" variant="success">
          <p className="text-sm">3.8 Average</p>
        </Card>

        <Card title="Alerts" variant="danger">
          <p className="text-sm">2 Urgent Notices</p>
        </Card>
      </div>

      {/* Main Content Area using grid for charts/data placeholders */}
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
            <p className="text-sm text-gray-600">Current status of your enrollment.</p>
            <div className="p-3 bg-gray-50 border rounded text-sm text-gray-500 italic">
              No recent activity to display.
            </div>
          </div>
        </Card>
      </div>

      {/* Note: Modal.jsx is part of the library but not rendered statically here 
          as it requires logic to trigger. It is fully implemented in /components/ui/ */}
    </div>
  );
}

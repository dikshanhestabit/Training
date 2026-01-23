"use client";

import React from "react";
import Card from "@/components/ui/Card";
import Badge from "@/components/ui/Badge";
import Button from "@/components/ui/Button";

const MOCK_USERS = [
    { id: 1, name: "abc", email: "abc@gmail.com", status: "Active", role: "Student" },
    { id: 2, name: "wxy", email: "wxy@gmail.com", status: "Active", role: "Student" },
    { id: 3, name: "xyz", email: "xyz@gmail.com", status: "Pending", role: "Student" },
    { id: 4, name: "pqr", email: "pqr@gmail.com", status: "Inactive", role: "Student" },
    { id: 5, name: "lmn", email: "lmn@gmail.com", status: "Active", role: "Student" },
];

export default function UsersPage() {
    return (
        <div className="space-y-6">
            <div className="flex justify-between items-center">
                <h1 className="text-2xl font-bold text-slate-800">Users Listing</h1>
                <Button variant="primary">Add New User</Button>
            </div>

            <Card className="overflow-hidden p-0 border-slate-200">
                <div className="overflow-x-auto">
                    <table className="w-full text-left border-collapse">
                        <thead className="bg-slate-50 border-b border-slate-200">
                            <tr>
                                <th className="px-6 py-4 font-semibold text-slate-700 text-sm">NAME</th>
                                <th className="px-6 py-4 font-semibold text-slate-700 text-sm">EMAIL</th>
                                <th className="px-6 py-4 font-semibold text-slate-700 text-sm">ROLE</th>
                                <th className="px-6 py-4 font-semibold text-slate-700 text-sm">STATUS</th>
                                <th className="px-6 py-4 font-semibold text-slate-700 text-sm">ACTIONS</th>
                            </tr>
                        </thead>
                        <tbody className="divide-y divide-slate-100">
                            {MOCK_USERS.map((user) => (
                                <tr key={user.id} className="hover:bg-slate-50 transition-colors">
                                    <td className="px-6 py-4 text-sm font-medium text-slate-900">{user.name}</td>
                                    <td className="px-6 py-4 text-sm text-slate-600">{user.email}</td>
                                    <td className="px-6 py-4 text-sm text-slate-600">{user.role}</td>
                                    <td className="px-6 py-4 text-sm text-slate-600">
                                        <Badge variant={user.status === "Active" ? "primary" : "secondary"}>
                                            {user.status}
                                        </Badge>
                                    </td>
                                    <td className="px-6 py-4 text-sm">
                                        <div className="flex space-x-2">
                                            <button className="text-blue-600 hover:text-blue-800 font-medium">Edit</button>
                                            <button className="text-red-600 hover:text-red-800 font-medium">Delete</button>
                                        </div>
                                    </td>
                                </tr>
                            ))}
                        </tbody>
                    </table>
                </div>
            </Card>
        </div>
    );
}

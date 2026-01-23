"use client";

import React from "react";
import Card from "@/components/ui/Card";
import Button from "@/components/ui/Button";
import Input from "@/components/ui/Input";

export default function ProfilePage() {
    return (
        <div className="max-w-4xl mx-auto space-y-8">
            <div className="flex items-center justify-between border-b pb-4">
                <h1 className="text-2xl font-bold text-slate-800">My Profile</h1>
                <Button variant="primary">Save Changes</Button>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
                {/* Left Column - Avatar & Info */}
                <div className="md:col-span-1 space-y-6">
                    <Card className="text-center p-6 border-slate-200">
                        <div className="mb-4">
                            <img
                                src="https://img.freepik.com/premium-vector/user-profile-icon-circle_1256048-12499.jpg?semt=ais_hybrid&w=740&q=80"
                                alt="User Profile"
                                className="w-24 h-24 rounded-full mx-auto object-cover"
                            />
                        </div>
                        <h3 className="text-lg font-semibold text-slate-900">xyz</h3>
                        <p className="text-sm text-slate-500">Student | Semester 8</p>
                        <div className="mt-4 pt-4 border-t text-left space-y-2">
                            <p className="text-xs font-medium text-slate-400 uppercase tracking-wider">Contact Info</p>
                            <p className="text-sm text-slate-700">xyz@gmail.com</p>
                            <p className="text-sm text-slate-700">+91 9876543210</p>
                        </div>
                    </Card>
                </div>

                {/* Right Column - Form */}
                <div className="md:col-span-2 space-y-6">
                    <Card title="Account Settings" className="border-slate-200">
                        <form className="space-y-4">
                            <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
                                <div>
                                    <label className="block text-sm font-medium text-slate-700 mb-1">First Name</label>
                                    <Input defaultValue="xyz" fullWidth />
                                </div>
                                <div>
                                    <label className="block text-sm font-medium text-slate-700 mb-1">Last Name</label>
                                    <Input defaultValue="" fullWidth />
                                </div>
                            </div>
                            <div>
                                <label className="block text-sm font-medium text-slate-700 mb-1">Email Address</label>
                                <Input defaultValue="xyz@gmail.com" type="email" fullWidth />
                            </div>
                            <div>
                                <label className="block text-sm font-medium text-slate-700 mb-1">Phone Number</label>
                                <Input defaultValue="+91 9876543210" fullWidth />
                            </div>
                            <div>
                                <label className="block text-sm font-medium text-slate-700 mb-1">Address</label>
                                <textarea
                                    className="w-full h-24 p-2 border border-slate-300 rounded-md focus:ring-1 focus:ring-blue-500 focus:outline-none text-sm text-slate-900"
                                    placeholder="Enter your address..."
                                ></textarea>
                            </div>
                        </form>
                    </Card>
                </div>
            </div>
        </div>
    );
}

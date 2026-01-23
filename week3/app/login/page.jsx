"use client";

import React from "react";
import Button from "@/components/ui/Button";
import Input from "@/components/ui/Input";
import Card from "@/components/ui/Card";

export default function LoginPage() {
    return (
        <div className="flex min-h-screen items-center justify-center bg-gray-50 px-4">
            <Card className="w-full max-w-md p-8 shadow-sm">
                <div className="mb-8 text-center">
                    <h1 className="text-2xl font-bold text-gray-900">Login</h1>
                    <p className="mt-2 text-sm text-gray-600">Enter your credentials to access your account</p>
                </div>
                <form className="space-y-6" onSubmit={(e) => e.preventDefault()}>
                    <div>
                        <label className="block text-sm font-medium text-gray-700 mb-1">Email Address</label>
                        <Input type="email" placeholder="email@example.com" fullWidth />
                    </div>
                    <div>
                        <label className="block text-sm font-medium text-gray-700 mb-1">Password</label>
                        <Input type="password" placeholder="••••••••" fullWidth />
                    </div>
                    <div className="flex items-center justify-between">
                        <div className="flex items-center">
                            <input
                                id="remember-me"
                                name="remember-me"
                                type="checkbox"
                                className="h-4 w-4 rounded border-gray-300 text-blue-600 focus:ring-blue-500"
                            />
                            <label htmlFor="remember-me" className="ml-2 block text-sm text-gray-900">
                                Remember me
                            </label>
                        </div>
                        <div className="text-sm">
                            <a href="#" className="font-medium text-blue-600 hover:text-blue-500">
                                Forgot password?
                            </a>
                        </div>
                    </div>
                    <Button variant="primary" fullWidth className="py-2.5">
                        Login
                    </Button>
                </form>
            </Card>
        </div>
    );
}

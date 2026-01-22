import Sidebar from "@/components/ui/Sidebar";
import Navbar from "@/components/ui/Navbar";

export default function DashboardLayout({ children }) {
    return (
        <div className="flex bg-gray-50 min-h-screen">
            <div className="hidden md:block">
                <Sidebar />
            </div>

            <div className="flex-1 md:ml-64 flex flex-col min-h-screen">
                <Navbar />

                <main className="p-4 md:p-6 mt-16 flex-1">
                    {children}
                </main>
            </div>
        </div>
    );
}

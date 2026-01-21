import Sidebar from "@/components/ui/Sidebar";
import Navbar from "@/components/ui/Navbar";

export default function DashboardLayout({ children }) {
    return (
        <div className="flex">
            <Sidebar />

            <div className="flex-1 ml-64 flex flex-col min-h-screen">
                <Navbar />

                <main className="p-6 mt-16 flex-1">
                    {children}
                </main>
            </div>
        </div>
    );
}

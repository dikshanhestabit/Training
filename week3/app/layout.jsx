
import { Geist, Geist_Mono } from "next/font/google";
import "./globals.css";
import Sidebar from "@/components/ui/Sidebar";
import Navbar from "@/components/ui/Navbar";

const geistSans = Geist({
  variable: "--font-geist-sans",
  subsets: ["latin"],
});

const geistMono = Geist_Mono({
  variable: "--font-geist-mono",
  subsets: ["latin"],
});

export const metadata = {
  title: "Day 1 Dashboard",
  description: "Week 3 Day 1 Task",
};

export default function RootLayout({ children }) {
  return (
    <html lang="en">
      <body
        className={`${geistSans.variable} ${geistMono.variable} antialiased bg-gray-50`}
      >
        <div className="flex">
          <Sidebar />

          <div className="flex-1 ml-64 flex flex-col min-h-screen">
            <Navbar />

            <main className="p-6 mt-16 flex-1">
              {children}
            </main>
          </div>
        </div>
      </body>
    </html>
  );
}

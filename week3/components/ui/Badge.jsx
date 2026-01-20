export default function Badge({ children, variant = "default", className = "" }) {
    const variants = {
        default: "bg-gray-200 text-gray-800",
        success: "bg-green-100 text-green-800",
        warning: "bg-yellow-100 text-yellow-800",
        danger: "bg-red-100 text-red-800",
        info: "bg-blue-100 text-blue-800",
    };
    return (
        <span className={`px-2 py-1 rounded-full text-[10px] font-bold uppercase tracking-wider ${variants[variant] || variants.default} ${className}`}>
            {children}
        </span>
    );
}

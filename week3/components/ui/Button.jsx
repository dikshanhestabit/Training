export default function Button({ children, onClick, variant = "primary", className = "", ...rest }) {
    const base = "px-4 py-2 rounded font-medium transition-colors text-sm";
    const variants = {
        primary: "bg-blue-50 text-blue-700 hover:bg-blue-100 border border-blue-200",
        secondary: "bg-gray-50 text-gray-700 hover:bg-gray-100 border border-gray-200",
        success: "bg-green-50 text-green-700 hover:bg-green-100 border border-green-200",
        info: "bg-cyan-50 text-cyan-700 hover:bg-cyan-100 border border-cyan-200",
        warning: "bg-yellow-50 text-yellow-700 hover:bg-yellow-100 border border-yellow-200",
        danger: "bg-red-50 text-red-700 hover:bg-red-100 border border-red-200",
    };
    return (
        <button
            onClick={onClick}
            className={`${base} ${variants[variant] || variants.primary} ${className}`}
            {...rest}
        >
            {children}
        </button>
    );
}

export default function Card({ title, children, className = "", variant = "default" }) {
    const variants = {
        default: "bg-white border border-gray-100",
        primary: "bg-blue-50 text-blue-800 border border-blue-100",
        success: "bg-green-50 text-green-800 border border-green-100",
        info: "bg-cyan-50 text-cyan-800 border border-cyan-100",
        warning: "bg-yellow-50 text-yellow-800 border border-yellow-100",
        danger: "bg-red-50 text-red-800 border border-red-100",
    };

    return (
        <div className={`rounded shadow-sm p-4 ${variants[variant] || variants.default} ${className}`}>
            {title && <h3 className={`text-lg font-semibold mb-3 ${variant === 'default' ? 'text-gray-800' : 'opacity-90'}`}>{title}</h3>}
            <div>
                {children}
            </div>
        </div>
    );
}

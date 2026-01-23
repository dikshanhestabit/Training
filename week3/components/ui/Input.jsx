export default function Input({ id, label, type = "text", placeholder = "", className = "", fullWidth, ...rest }) {
    return (
        <div className={`flex flex-col ${fullWidth ? "w-full" : ""} ${className}`}>
            {label && <label htmlFor={id} className="mb-1 text-sm font-medium">{label}</label>}
            <input
                id={id}
                type={type}
                placeholder={placeholder}
                className="border rounded px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-blue-500"
                {...rest}
            />
        </div>
    );
}

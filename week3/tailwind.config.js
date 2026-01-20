/** @type {import('tailwindcss').Config} */
module.exports = {
    content: [
        "./app/**/*.{js,ts,jsx,tsx,mdx}",
        "./components/**/*.{js,ts,jsx,tsx,mdx}",
    ],
    theme: {
        extend: {
            colors: {
                brand: {
                    blue: '#4e73df',
                    dark: '#2e59d9'
                },
                sidebar: {
                    bg: '#4e73df' // Fallback
                }
            },
        },
    },
    plugins: [],
};

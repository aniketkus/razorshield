/** @type {import('tailwindcss').Config} */
export default {
  content: ["./index.html", "./src/**/*.{js,ts,jsx,tsx}"],
  theme: {
    extend: {
      colors: {
        razor: {
          50:  "#fff0f0",
          100: "#ffe0e0",
          500: "#2563eb",
          600: "#1d4ed8",
          700: "#1e3a8a",
          dark: "#0f172a",
        }
      },
      fontFamily: { sans: ["Inter", "ui-sans-serif", "system-ui"] }
    }
  },
  plugins: []
}

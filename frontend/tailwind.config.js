/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        'kids-bg': '#f0f9ff',
        'kids-primary': '#fbbf24',
        'kids-secondary': '#38bdf8',
        'kids-accent': '#ec4899',
      },
      borderRadius: {
        '4xl': '2rem',
      }
    },
  },
  plugins: [],
}

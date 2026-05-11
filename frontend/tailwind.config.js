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
      },
      keyframes: {
        float: {
          '0%, 100%': { transform: 'translateY(0)' },
          '50%': { transform: 'translateY(-10px)' },
        },
        popIn: {
          '0%': { opacity: '0', transform: 'scale(0.8)' },
          '100%': { opacity: '1', transform: 'scale(1)' },
        },
        fadeInUp: {
          '0%': { opacity: '0', transform: 'translateY(20px)' },
          '100%': { opacity: '1', transform: 'translateY(0)' },
        },
        wiggle: {
          '0%, 100%': { transform: 'rotate(-3deg)' },
          '50%': { transform: 'rotate(3deg)' },
        }
      },
      animation: {
        float: 'float 3s ease-in-out infinite',
        popIn: 'popIn 0.5s cubic-bezier(0.175, 0.885, 0.32, 1.275) forwards',
        fadeInUp: 'fadeInUp 0.6s ease-out forwards',
        wiggle: 'wiggle 0.3s ease-in-out infinite',
      }
    },
  },
  plugins: [],
}

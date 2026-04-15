/** @type {import('tailwindcss').Config} */
export default {
  content: ["./app/**/*.html", "./app/**/*.jinja2"],
  theme: {
    extend: {
      animation: {
        float: "floatBottle 3s ease-in-out infinite",
        "fade-up": "fadeInUp 0.7s ease-out both",
      },
      keyframes: {
        floatBottle: {
          "0%, 100%": { transform: "translateY(0)" },
          "50%": { transform: "translateY(-12px)" },
        },
        fadeInUp: {
          from: { opacity: "0", transform: "translateY(30px)" },
          to: { opacity: "1", transform: "translateY(0)" },
        },
      },
      fontFamily: {
        roboto: ["Roboto", "sans-serif"],
      },
      colors: {
        "brew-bg": "#474747",
        "brew-beige": "#FDF7E6",
        "brew-dark": "#222222",
      },
    },
  },
  plugins: [],
};

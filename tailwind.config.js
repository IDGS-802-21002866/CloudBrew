/** @type {import('tailwindcss').Config} */
export default {
  content: ["./app/**/*.html", "./app/**/*.jinja2"],
  theme: {
    extend: {
      colors: {
        "brew-bg": "#474747",
        "brew-beige": "#FDF7E6",
        "brew-dark": "#222222",
      },
    },
  },
  plugins: [],
};

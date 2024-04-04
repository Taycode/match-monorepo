/** @type {import('tailwindcss').Config} */
export default {
  content: ["./index.html", "./src/**/*.{js,ts,jsx,tsx}"],
  theme: {
    extend: {
      colors: {
        primary: "#092470",
        secondary: "#4E5B92",
        gray: "#77767A",
      },
    },
  },
  plugins: [],
};

/** @type {import('tailwindcss').Config} */
module.exports = {
  content: ["./src/**/*.{js,jsx}"],
  theme: {
    colors : {
      'background-color': '#000000',
      'primary-color': '#ffffff',
      'secondary-color': '#61dafb',
    },
    fontFamily: {
      'title': [ '"Major Mono Display"','monospace']
    },
    extend: {},
  },
  plugins: [],
}

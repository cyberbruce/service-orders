/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./app/**/*.{html,py,css,js}",
  ],
  theme: {
    extend: {},
  },
  daisyui: {
    themes: [
      {
        mytheme: {

          "primary": "#0098ff",

          "primary-content": "#f3f4f6",

          "secondary": "#4b5563",

          "secondary-content": "#d8dbde",

          "accent": "#facc15",

          "accent-content": "#150f00",

          "neutral": "#09120a",

          "neutral-content": "#c7c9c7",

          "base-100": "#ffffff",

          "base-200": "#dedede",

          "base-300": "#bebebe",

          "base-content": "#161616",

          "info": "#0085e3",

          "info-content": "#f3f4f6",

          "success": "#16a34a",

          "success-content": "#f3f4f6",

          "warning": "#ffc800",

          "warning-content": "#160f00",

          "error": "#e11d48",

          "error-content": "#ffd8d9",
        },
      },
    ],
  },
  plugins: [
    require('daisyui'),
    require("@tailwindcss/typography"),
    require("tailwindcss-animate"),
   // require('@tailwindcss/forms')
  ],
}


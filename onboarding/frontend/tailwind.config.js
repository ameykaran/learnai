// tailwind.config.js
/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    './src/app/**/*.{js,ts,jsx,tsx,mdx}',
    './src/app/**/*.{js,ts,jsx,tsx,mdx}', // app dir (covers components under src/app)
    './src/components/**/*.{js,ts,jsx,tsx,mdx}', // if you keep separate components dir
    './src/pages/**/*.{js,ts,jsx,tsx,mdx}', // optional for pages router
  ],
  theme: { extend: {} },
  plugins: [],
}

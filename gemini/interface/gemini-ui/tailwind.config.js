import {nextui} from '@nextui-org/theme'

/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    './components/**/*.{js,ts,jsx,tsx,mdx}',
    './app/**/*.{js,ts,jsx,tsx,mdx}',
    './node_modules/@nextui-org/theme/dist/**/*.{js,ts,jsx,tsx}'
  ],
  theme: {
    extend: {
      fontFamily: {
        sans: ["var(--font-sans)"],
        mono: ["var(--font-geist-mono)"],
      },
    },
  },
  darkMode: "class",
  plugins: [nextui({
      themes: {
        light : {
          colors: {
            primary: {
              DEFAULT: "#142A50",
              foreground: "#000000",
            },
            secondary: {
              DEFAULT: "#E7F2E1",
              foreground: "#000000",
            },
            focus: "#BEF264",
          },
        },
      },
    })],
}

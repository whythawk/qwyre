module.exports = {
  purge: [
    "./components/**/*.{vue,js,ts}",
    "./layouts/**/*.vue",
    "./pages/**/*.vue",
    "./plugins/**/*.{js,ts}",
    "./nuxt.config.{js,ts}",
  ],
  darkMode: false, // or 'media' or 'class'
  // https://devdojo.com/tnylea/custom-animations-in-tailwindcss
  theme: {
    extend: {
      backgroundImage: theme => ({
        "join-the-qwyre": "url('/join-the-qwyre.png')",
        "support-the-qwyre": "url('/aaron-burden-6jYoil2GhVk-unsplash.jpg')",
        "lost-the-qwyre": "url('/george-brits-wvO5tPfTpug-unsplash.jpg')",
      }),
      colors: {
        ochre: {
          10: "#fbf9f4",
          50: "#EDE7E3",
          100: "#DBD0C7",
          200: "#C9B8AC",
          300: "#B7A190",
          400: "#ab9381",
          500: "#a68a75",
          600: "#846E5D",
          700: "#635246",
          800: "#42372E",
          900: "#211B17",
        },
        woad: {
          10: "#ABBDD3",
          50: "#97ADC9",
          100: "#DAE3ED",
          200: "#B6C7DB",
          300: "#91ABC9",
          400: "#6D8FB7",
          500: "#4974a5",
          600: "#3A5C84",
          700: "#2B4563",
          800: "#2B4563",
          900: "#1D2E42",
        },
        sinopia: {
          100: "#F7D8CC",
          200: "#F0B299",
          300: "#E88C66",
          400: "#E16633",
          500: "#da4000",
          600: "#C43900",
          700: "#AE3300",
          800: "#982C00",
          900: "#6C2000",
        },
        malachite: {
          100: "#C7DBB6",
          200: "#ABC991",
          300: "#8FB76D",
          400: "#74a549",
          500: "#689441",
          600: "#5C843A",
          700: "#517333",
          800: "#45632B",
          900: "#3A5224",
        },
      },
      keyframes: {
        "fade-in": {
          "0%": {
            opacity: "0",
          },
          "100%": {
            opacity: "1",
          },
        },
        "fade-out": {
          from: {
            opacity: "1",
          },
          to: {
            opacity: "0",
          },
        },
        "fade-out-down": {
          from: {
            opacity: "1",
            transform: "translateY(0px)",
          },
          to: {
            opacity: "0",
            transform: "translateY(10px)",
          },
        },
        "fade-in-up": {
          "0%": {
            opacity: "0",
            transform: "translateY(10px)",
          },
          "100%": {
            opacity: "1",
            transform: "translateY(0)",
          },
        },
      },
      animation: {
        "fade-in": "fade-in 0.5s ease-out",
        "fade-out": "fade-out 0.5s ease-out",
        "fade-out-down": "fade-out-down 0.5s ease-out",
        "fade-in-up": "fade-in-up 0.5s ease-out",
      },
    },
  },
  variants: {
    extend: {},
  },
  plugins: [
    require("@tailwindcss/typography"),
    require("@tailwindcss/forms"),
    require("@tailwindcss/aspect-ratio"),
  ],
}

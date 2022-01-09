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
      backgroundImage: (theme) => ({
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
      typography: (theme) => ({
        DEFAULT: {
          css: {
            "h1,h2,h3,h4,h5,h6,hgroup": {
              textAlign: "center",
              marginTop: "3em",
              marginRight: "0",
              marginBottom: "3em",
              marginLeft: "0",
            },
            "hgroup > *": {
              fontWeight: "normal",
              marginTop: "0",
              marginRight: "0",
              marginBottom: "0",
              marginLeft: "0",
            },
            p: {
              marginTop: "0",
              marginRight: "0",
              marginBottom: "0",
              marginLeft: "0",
              textIndent: "1em",
            },
            "p.continued,h1 + p,h2 + p,h3 + p,h4 + p,h5 + p,h6 + p,header + p,hr + p,hgroup + p,p.first-child,p:first-child":
              {
                hangingPunctuation: "first last",
                textIndent: "0",
              },
            h2: {
              marginTop: "2.28571429em",
              marginBottom: "1.14285714em",
            },
            h3: {
              marginTop: "1.33333333em",
              marginBottom: "1.33333333em",
            },
            h4: {
              marginTop: "1.5em",
              marginBottom: "0",
            },
            header: {
              textAlign: "center",
            },
            "header > * + p": {
              textIndent: "0",
            },
            blockquote: {
              margin: "1.5em 5%",
              display: "block",
              fontStyle: "italic",
              textIndent: "2em",
              borderLeftWidth: "0",
              borderLeftColor: "transparent",
            },
            "blockquote p:first-child": {
              textIndent: "1em",
            },
            a: {
              textDecoration: "underline",
              fontWeight: "700",
              color: "inherit",
              "-webkit-text-fill-color": "inherit",
            },
          },
        },
        "reader-light": {
          css: {
            "h1,h2,h3,h4,h5,h6,hgroup,p,a,ul,li,lo,b,i,strong,em,blockquote,header":
              {
                color: theme("colors.ochre[800]"),
              },
          },
        },
        "reader-dark": {
          css: {
            "h1,h2,h3,h4,h5,h6,hgroup,p,a,ul,li,lo,b,i,strong,em,blockquote,header":
              {
                color: theme("colors.ochre[10]"),
              },
          },
        },
        "reader-compact": {
          css: {
            "h2,h3,h4,h5,h6": {
              textAlign: "left",
              marginTop: "1.5rem",
              marginBottom: "1rem",
            },
            h1: {
              marginTop: "0",
              marginBottom: "1.5rem",
            },
          },
        },
        "reader-5xl": {
          css: {
            h1: {
              fontSize: "8rem",
              lineHeight: "1",
            },
            h2: {
              fontSize: "6rem",
              lineHeight: "1",
            },
            h3: {
              fontSize: "4.5rem",
              lineHeight: "1",
            },
            h4: {
              fontSize: "3.75rem",
              lineHeight: "1",
            },
            "p,a,ul,li,lo,b,i,strong,em,blockquote": {
              fontSize: "3rem",
              lineHeight: "1",
            },
          },
        },
        "reader-4xl": {
          css: {
            h1: {
              fontSize: "6rem",
              lineHeight: "1",
            },
            h2: {
              fontSize: "4.5rem",
              lineHeight: "1",
            },
            h3: {
              fontSize: "3.75rem",
              lineHeight: "1",
            },
            h4: {
              fontSize: "3rem",
              lineHeight: "1",
            },
            "p,a,ul,li,lo,b,i,strong,em,blockquote": {
              fontSize: "2.25rem",
              lineHeight: "2.5rem",
            },
          },
        },
        "reader-3xl": {
          css: {
            h1: {
              fontSize: "4.5rem",
              lineHeight: "1",
            },
            h2: {
              fontSize: "3.75rem",
              lineHeight: "1",
            },
            h3: {
              fontSize: "3rem",
              lineHeight: "1",
            },
            h4: {
              fontSize: "2.25rem",
              lineHeight: "2.5rem",
            },
            "p,a,ul,li,lo,b,i,strong,em,blockquote": {
              fontSize: "1.875rem",
              lineHeight: "2.25rem",
            },
          },
        },
        "reader-2xl": {
          css: {
            h1: {
              fontSize: "3.75rem",
              lineHeight: "1",
            },
            h2: {
              fontSize: "3rem",
              lineHeight: "1",
            },
            h3: {
              fontSize: "2.25rem",
              lineHeight: "2.5rem",
            },
            h4: {
              fontSize: "1.875rem",
              lineHeight: "2.25rem",
            },
            "p,a,ul,li,lo,b,i,strong,em,blockquote": {
              fontSize: "1.5rem",
              lineHeight: "2rem",
            },
          },
        },
        "reader-xl": {
          css: {
            h1: {
              fontSize: "3rem",
              lineHeight: "1",
            },
            h2: {
              fontSize: "2.25rem",
              lineHeight: "2.5rem",
            },
            h3: {
              fontSize: "1.875rem",
              lineHeight: "2.25rem",
            },
            h4: {
              fontSize: "1.5rem",
              lineHeight: "2rem",
            },
            "p,a,ul,li,lo,b,i,strong,em,blockquote": {
              fontSize: "1.25rem",
              lineHeight: "1.75rem",
            },
          },
        },
        "reader-lg": {
          css: {
            h1: {
              fontSize: "2.25rem",
              lineHeight: "2.5rem",
            },
            h2: {
              fontSize: "1.875rem",
              lineHeight: "2.25rem",
            },
            h3: {
              fontSize: "1.5rem",
              lineHeight: "2rem",
            },
            h4: {
              fontSize: "1.25rem",
              lineHeight: "1.75rem",
            },
            "p,a,ul,li,lo,b,i,strong,em,blockquote": {
              fontSize: "1.125rem",
              lineHeight: "1.75rem",
            },
          },
        },
        "reader-base": {
          css: {
            h1: {
              fontSize: "1.875rem",
              lineHeight: "2.25rem",
            },
            h2: {
              fontSize: "1.5rem",
              lineHeight: "2rem",
            },
            h3: {
              fontSize: "1.25rem",
              lineHeight: "1.75rem",
            },
            h4: {
              fontSize: "1.125rem",
              lineHeight: "1.75rem",
            },
            "p,a,ul,li,lo,b,i,strong,em,blockquote": {
              fontSize: "1rem",
              lineHeight: "1.5rem",
            },
          },
        },
        "reader-sm": {
          css: {
            h1: {
              fontSize: "1.5rem",
              lineHeight: "2rem",
            },
            h2: {
              fontSize: "1.25rem",
              lineHeight: "1.75rem",
            },
            h3: {
              fontSize: "1.125rem",
              lineHeight: "1.75rem",
            },
            h4: {
              fontSize: "1rem",
              lineHeight: "1.5rem",
            },
            "p,a,ul,li,lo,b,i,strong,em,blockquote": {
              fontSize: "0.875rem",
              lineHeight: "1.25rem",
            },
          },
        },
        "reader-xs": {
          css: {
            h1: {
              fontSize: "1.25rem",
              lineHeight: "1.75rem",
            },
            h2: {
              fontSize: "1.125rem",
              lineHeight: "1.75rem",
            },
            h3: {
              fontSize: "1rem",
              lineHeight: "1.5rem",
            },
            h4: {
              fontSize: "0.875rem",
              lineHeight: "1.25rem",
            },
            "p,a,ul,li,lo,b,i,strong,em,blockquote": {
              fontSize: "0.75rem",
              lineHeight: "1rem",
            },
          },
        },
      }),
    },
  },
  variants: {
    extend: {},
  },
  plugins: [
    require("@tailwindcss/typography"),
    require("@tailwindcss/forms"),
    require("@tailwindcss/aspect-ratio"),
    require("@tailwindcss/line-clamp"),
  ],
}

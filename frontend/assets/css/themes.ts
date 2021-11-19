const dark = {
  body: {
    background: `#211b17 !important`,
    color: `#fbf9f4 !important`,
  },
  "*": {
    color: "inherit !important",
    background: "inherit !important",
  },
  "a:link": {
    color: `#fbf9f4 !important`,
    "text-decoration": "underline !important",
  },
  "a:link:hover": {
    background: "rgba(0, 0, 0, 0.1) !important",
  },
}

const light = {
  body: {},
  "*": {},
  "a:link": {},
  "a:link:hover": {},
}

const serif = {
  "@font-face": {
    "font-family": "PTSerifRegular",
    src: "url('~assets/fonts/PTF55F_W.woff2') format('woff2')",
    "font-weight": "normal",
    "font-style": "normal",
    "font-display": "swap",
  },
  body: {
    "font-family": "PTSerifRegular",
  },
}

const sanserif = {
  "@font-face": {
    "font-family": "PTSansRegular",
    src: "url('~assets/fonts/PTS55F_W.woff2') format('woff2')",
    "font-weight": "normal",
    "font-style": "normal",
    "font-display": "swap",
  },
  body: {
    "font-family": "PTSansRegular",
  },
}

export { dark, light, serif, sanserif }

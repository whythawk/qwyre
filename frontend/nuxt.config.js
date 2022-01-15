/* import fs from "fs"
import path from "path" */
import i18n from "./config/i18n"

export default {
  // Global page headers: https://go.nuxtjs.dev/config-head
  // https://vue-meta.nuxtjs.org/api/#script
  // https://javascript.info/script-async-defer
  head: {
    title: "Qwyre",
    meta: [
      { charset: "utf-8" },
      { name: "viewport", content: "width=device-width, initial-scale=1" },
      // { name: "monetization", content: process.env.COIL_PAYMENT_POINTER },
      { hid: "description", name: "description", content: "" },
      { src: "https://js.stripe.com/v3", async: true },
      // { src: "https://cdn.coil.com/coil-oauth-wm.v7.beta.js", defer: true },
    ],
    noscript: [{ innerHTML: "This website requires JavaScript." }],
    link: [{ rel: "icon", type: "image/x-icon", href: "/favicon.ico" }],
  },

  // Generate: https://nuxtjs.org/docs/2.x/configuration-glossary/configuration-generate
  generate: {
    fallback: "404.html",
  },

  ssr: true,
  target: "server",

  // Env: https://nuxtjs.org/docs/2.x/configuration-glossary/configuration-env/
  env: {
    baseUrl: process.env.BASE_URL || "http://localhost:3000",
    appName: process.env.VUE_APP_NAME,
    apiWS: process.env.VUE_APP_DOMAIN_WS,
    apiUrl: process.env.VUE_APP_DOMAIN_API,
    idbName: process.env.VUE_IDB_NAME,
    idbVersion: process.env.VUE_IDB_VERSION,
    stripeKey: process.env.STRIPE_PUBLIC_KEY,
    stripeMinimum: process.env.STRIPE_MINIMUM_CHARGE_AMOUNT,
    stripeDefault: process.env.STRIPE_DEFAULT_CHARGE_AMOUNT,
    coilUrl: process.env.COIL_URI || "https://coil.com",
    coilAPIUrl: process.env.COIL_API_URI || "https://api.coil.com",
    coilID: process.env.COIL_CLIENT_ID,
    coilSecret: process.env.COIL_CLIENT_SECRET,
    coilPointer: process.env.COIL_PAYMENT_POINTER,
    coilVerifier: process.env.COIL_RECEIPT_VERIFIER,
    coilRedirect: process.env.COIL_REDIRECT_URI,
  },

  // Global CSS: https://go.nuxtjs.dev/config-css
  css: [],

  // Plugins to run before rendering page: https://go.nuxtjs.dev/config-plugins
  plugins: ["~/plugins/init.client.ts", "~/plugins/vee-validate"],

  // Auto import components: https://go.nuxtjs.dev/config-components
  components: true,

  // Modules for dev and build (recommended): https://go.nuxtjs.dev/config-modules
  buildModules: [
    // https://go.nuxtjs.dev/typescript
    "@nuxt/typescript-build",
    // https://go.nuxtjs.dev/tailwindcss
    "@nuxtjs/tailwindcss",
    // https://github.com/nuxt-community/style-resources-module#readme
    // https://medium.com/@wearethreebears/globally-accessible-css-and-scss-sass-in-your-nuxt-component-files-7c1c012d31bd
    // "@nuxtjs/style-resources",
  ],

  // styleResources: {
  //   scss: ["@/assets/scss/_variables.scss"],
  // },

  // Modules: https://go.nuxtjs.dev/config-modules
  modules: [
    // https://go.nuxtjs.dev/axios
    "@nuxtjs/axios",
    // https://github.com/microcipcip/cookie-universal/tree/master/packages/cookie-universal-nuxt
    "cookie-universal-nuxt",
    // https://go.nuxtjs.dev/pwa
    "@nuxtjs/pwa",
    // https://go.nuxtjs.dev/content
    "@nuxt/content",
    // https://i18n.nuxtjs.org/
    // i18n: https://phrase.com/blog/posts/nuxt-js-tutorial-i18n/
    "nuxt-i18n",
  ],

  // Axios module configuration: https://go.nuxtjs.dev/config-axios
  axios: {},

  // PWA module configuration: https://go.nuxtjs.dev/pwa
  pwa: {
    meta: {
      name: "Qwyre",
      author: "Gavin Chait",
      description:
        "Qwyre.com is a streaming payments platform for collaborative publishing, a simple ebook converter, and an ereader.",
      theme_color: "#211B17",
      ogHost: "https://qwyre.com/",
      twitterCard: "app",
      twitterSite: "@GavinChait",
      twitterCreator: "@GavinChait",
    },
    manifest: {
      name: "Qwyre",
      short_name: "Qwyre",
      description:
        "Qwyre.com is a streaming payments platform for collaborative publishing, a simple ebook converter, and an ereader.",
    },
  },

  // Content module configuration: https://go.nuxtjs.dev/config-content
  content: {},

  // Options: https://i18n.nuxtjs.org/options-reference
  i18n: {
    locales: [
      {
        code: "en",
        name: "English",
        iso: "en",
        isCatchallLocale: true,
      },
      {
        code: "fr",
        name: "Français",
        iso: "fr",
      },
    ],
    defaultLocale: "en",
    vueI18nLoader: true,
    vueI18n: i18n,
    baseUrl: process.env.apiUrl,
    detectBrowserLanguage: {
      useCookie: true,
      cookieKey: "i18n_redirected",
      onlyOnRoot: true, // recommended
    },
  },

  // Build Configuration: https://go.nuxtjs.dev/config-build
  build: {
    /*
     ** You can extend webpack config here
     ** Getting `.mjs` support required: https://github.com/html-to-text/node-html-to-text/issues/229#issuecomment-859147955
     ** and https://github.com/nuxt/nuxt.js/issues/6688
     */
    extend(config, _ctx) {
      // transpile .mjs too
      const babelRule = config.module.rules.find(
        (rule) => `${rule.test}` === "/\\.jsx?$/i"
      )
      if (babelRule) {
        babelRule.test = /\.m?jsx?$/i
      }
    },
    transpile: ["vee-validate/dist/rules", /\.mjs$/],
    // https://nuxtjs.org/docs/2.x/configuration-glossary/configuration-build#standalone
    // https://github.com/nuxt/nuxt.js/issues/9223#issuecomment-840747064
    standalone: true,
  },

  // Server Configuration: https://nuxtjs.org/docs/2.x/configuration-glossary/configuration-server#example-using-https-configuration
  /* server: {
    https: {
      key: fs.readFileSync(
        path.resolve(__dirname, "./certificates/qwyre.com+5-key.pem")
      ),
      cert: fs.readFileSync(
        path.resolve(__dirname, "./certificates/qwyre.com+5.pem")
      ),
    },
    public: "https://localhost:3000/",
  }, */
}

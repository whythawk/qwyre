FROM node:16 AS build
ENV NODE_ENV=development NUXT_HOST=${NUXT_HOST:-0.0.0.0} NUXT_PORT=${NUXT_PORT:-3000} NUXT_TELEMETRY_DISABLED=1
COPY . /app
WORKDIR /app
RUN yarn install --frozen-lockfile --network-timeout 100000 --non-interactive
RUN yarn build --standalone
EXPOSE ${NUXT_PORT}

FROM build AS run-dev
ENTRYPOINT ["yarn"]
CMD ["dev"]

FROM build AS run-start
ENV NODE_ENV=production
ENTRYPOINT ["yarn"]
CMD ["start"]

FROM node:16-alpine AS run-minimal
ARG NUXT_VERSION=^2.15
ARG VEE_VERSION=^3.4.14
ARG NUXT_CONTENT_VERSION=^1.14.0
ARG AXIOS_VERSION=^5.13.1
ARG POSTCSS8_VERSION=^1.1.3
ARG PWA_VERSION=^3.3.5
ARG I18N_VERSION=^6.23.0
ARG STRIPE_JS_VERSION=^1.17.1
ARG ASPECT_RATIO_VERSION=^0.4.0
ARG FORMS_VERSION=^0.4.0
ARG TYPOGRAPHY_VERSION=^0.5.2
ARG LINE_CLAMP_VERSION=^0.3.0
ARG BROWSER_FS_VERSION=^0.25.0
ARG CORE_JS_VERSION=^3.9.1
ARG DAISYUI_VERSION=^2.2.1
ARG EPUBJS_VERSION=^0.3.88
ARG NUXT_PROPERTY_DECORATOR_VERSION=^2.9.1
ARG SWIPER_VERSION=^6.8.0
ARG TAILWINDCSS_VERSION=^3.0.23
ARG WEBSOCKET_VERSION=^1.0.34
ARG WEBSOCKET_AS_PROMISED_VERSION=^2.0.1
ARG COOKIE_UNIVERSAL_NUXT_VERSION=^2.1.5
ARG NUXT_PURGECSS_VERSION=^1.0.0
ENV NODE_ENV=production NUXT_HOST=${NUXT_HOST:-0.0.0.0} NUXT_PORT=${NUXT_PORT:-3000} NUXT_TELEMETRY_DISABLED=1
WORKDIR /app
RUN yarn add @nuxtjs/axios@${AXIOS_VERSION} @nuxt/content@${NUXT_CONTENT_VERSION} @nuxt/postcss8@${POSTCSS8_VERSION} @nuxtjs/pwa@${PWA_VERSION} nuxt-i18n@${I18N_VERSION} nuxt-start@${NUXT_VERSION} @stripe/stripe-js@${STRIPE_JS_VERSION} @tailwindcss/aspect-ratio@${ASPECT_RATIO_VERSION} @tailwindcss/forms@${FORMS_VERSION} @tailwindcss/typography@${TYPOGRAPHY_VERSION} @tailwindcss/line-clamp@${LINE_CLAMP_VERSION} browser-fs-access@${BROWSER_FS_VERSION} core-js@${CORE_JS_VERSION} daisyui@${DAISYUI_VERSION} epubjs@${EPUBJS_VERSION} nuxt-property-decorator@${NUXT_PROPERTY_DECORATOR_VERSION} swiper@${SWIPER_VERSION} tailwindcss@${TAILWINDCSS_VERSION} vee-validate@${VEE_VERSION} websocket@${WEBSOCKET_VERSION} websocket-as-promised@${WEBSOCKET_AS_PROMISED_VERSION} 
cookie-universal-nuxt@${COOKIE_UNIVERSAL_NUXT_VERSION} nuxt-purgecss@${NUXT_PURGECSS_VERSION}
COPY --from=build /app/.nuxt ./.nuxt
COPY --from=build /app/api ./api
COPY --from=build /app/app ./app
COPY --from=build /app/assets ./assets
COPY --from=build /app/components ./components
COPY --from=build /app/config ./config
COPY --from=build /app/content ./content
COPY --from=build /app/interfaces ./interfaces
COPY --from=build /app/layouts ./layouts
COPY --from=build /app/middleware ./middleware
COPY --from=build /app/mixins ./mixins
COPY --from=build /app/pages ./pages
COPY --from=build /app/plugins ./plugins
COPY --from=build /app/static ./static
COPY --from=build /app/store ./store
COPY --from=build /app/utilities ./utilities
COPY --from=build /app/.env ./
COPY --from=build /app/app.html ./
COPY --from=build /app/nuxt.config* ./
COPY --from=build /app/tailwind.config* ./
ENTRYPOINT ["yarn"]
CMD ["nuxt-start"]

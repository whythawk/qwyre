FROM node:lts AS build
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

FROM node:lts-alpine AS run-minimal
ARG NUXT_VERSION=^2.15
ARG VEE_VERSION=^3.4.14
ENV NODE_ENV=production NUXT_HOST=${NUXT_HOST:-0.0.0.0} NUXT_PORT=${NUXT_PORT:-3000} NUXT_TELEMETRY_DISABLED=1
WORKDIR /app
RUN yarn add @nuxtjs/axios @nuxt/content @nuxt/postcss8 @nuxtjs/pwa nuxt-i18n nuxt-start@${NUXT_VERSION} @stripe/stripe-js @tailwindcss/aspect-ratio @tailwindcss/forms @tailwindcss/typography @tailwindcss/line-clamp browser-fs-access core-js daisyui epubjs nuxt-property-decorator swiper tailwindcss vee-validate@${VEE_VERSION} websocket websocket-as-promised cookie-universal-nuxt nuxt-purgecss
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

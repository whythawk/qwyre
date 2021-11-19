<template>
  <div
    class="relative max-w-3xl mx-auto px-6 pt-10 flex flex-col items-center text-center lg:px-0"
  >
    <h1 class="inline-flex text-3xl font-extrabold text-ochre-800 lg:text-5xl">
      You're ready to stream ...
    </h1>
    <p class="mt-8 text-xl text-ochre-800">
      Toggle the Web Monetization icon in the menu to start and stop streaming
      payments.
    </p>
    <div class="inline-flex">
      <span class="mt-8 text-2xl font-semibold text-malachite-400">
        Streaming
        <SvgIcon terms="h-20 w-20" icon="svgMonetizationStatic" />
      </span>
      <span class="mt-8 ml-12 text-2xl font-semibold text-ochre-800">
        Stopped
        <SvgIcon terms="h-20 w-20" icon="svgMonetizationStatic" />
      </span>
    </div>
    <p class="mt-8 text-xl text-ochre-800">
      We receive <span class="font-semibold">36 cents per hour</span> while you
      stream. Thank you.
    </p>
  </div>
</template>

<script lang="ts">
import { Component, Vue } from "nuxt-property-decorator"

@Component
export default class WebMonetizationAuthenticationComplete extends Vue {}
</script>

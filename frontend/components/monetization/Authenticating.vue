<template>
  <div
    class="
      relative
      max-w-3xl
      mx-auto
      px-6
      py-10
      flex flex-col
      items-center
      text-center
      lg:px-0
    "
  >
    <h1 class="inline-flex text-2xl font-extrabold text-ochre-800 sm:text-3xl">
      Thank you :)
    </h1>
    <p class="mt-4 text-xl text-ochre-800">
      We're finalising your authentication...
    </p>
    <p class="mt-8 text-xl text-ochre-800">
      <SvgIcon terms="h-36 w-36" icon="svgRingsSpinner" />
    </p>
  </div>
</template>

<script lang="ts">
import { Component, Vue } from "nuxt-property-decorator"

@Component
export default class WebMonetizationAuthenticating extends Vue {}
</script>

<template>
  <div
    class="relative max-w-3xl mx-auto px-6 pt-10 flex flex-col items-center text-center lg:px-0"
  >
    <p class="mt-9 text-xl text-ochre-800">
      <span class="font-semibold">Web Monetization</span> lets you stream
      micropayments to creators. We would love for you to sign up with
      <span class="font-semibold">Coil</span>, our payments provider.
    </p>
    <a class="mt-9" :href="uri"
      ><SvgIcon terms="w-56 h-10" icon="svgCoilWhite"
    /></a>
    <p class="mt-9 text-xl text-ochre-800">
      We receive <span class="font-semibold">36 cents per hour</span> while you
      stream. Learn more at these links:
    </p>
    <p class="inline-flex mt-8 text-xl text-ochre-800">
      <a href="https://www.grantfortheweb.org/" rel="nofollow"
        ><SvgIcon terms="h-10 w-36" icon="svgGrantForTheWeb"
      /></a>
      <a href="https://webmonetization.org/" rel="nofollow" class="ml-10"
        ><SvgIcon terms="h-9 w-9" icon="svgMonetizationStatic"
      /></a>
      <a href="https://coil.com/" rel="nofollow" class="ml-10"
        ><SvgIcon terms="h-8 w-16" icon="svgCoilLogo"
      /></a>
    </p>
  </div>
</template>

<script lang="ts">
import { Component, Vue, Prop } from "nuxt-property-decorator"

@Component
export default class WebMonetizationSupporUs extends Vue {
  @Prop(String) readonly uri!: String
}
</script>

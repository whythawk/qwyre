<template>
  <div>
    <NuxtLink
      v-if="!coilSub"
      :class="`text-xs sm:text-sm px-3 sm:px-8 pb-1 flex flex-col flex-shrink-0 border border-transparent rounded-md text-ochre-10 ${themeText}`"
      to="/support-us"
      >Support us<SvgIcon
        terms="h-6 w-6 mt-2 mx-auto"
        icon="svgMonetizationStatic"
    /></NuxtLink>
    <div
      v-else
      :class="`text-xs sm:text-sm px-3 sm:px-8 flex flex-col flex-shrink-0 ${
        isStreaming ? themeGreenIcon : themeOchreIcon
      }`"
      @click.prevent="toggleMonetizationStreaming"
    >
      <span v-if="isStreaming">Streaming</span><span v-else>Stopped</span>
      <SvgIcon
        terms="h-6 w-6 fill-current mt-2 mx-auto"
        icon="svgMonetizationStatic"
      />
    </div>
  </div>
</template>

<script lang="ts">
import { Component, Vue, Getter, Prop, Action } from "nuxt-property-decorator"

@Component
export default class MonetizationMenuToggle extends Vue {
  @Prop(Boolean) readonly darkMode!: boolean
  @Getter("monetization/isStreaming") isStreaming
  @Getter("monetization/coilSub") coilSub
  @Getter("monetization/coilPointer") coilPointer
  @Action("monetization/startMonetizationStream") startMonetizationStream
  @Action("monetization/stopMonetizationStream") stopMonetizationStream
  public darkGreenIcon: string = "text-malachite-700 hover:text-malachite-500"
  public lightGreenIcon: string = "text-malachite-100 hover:text-malachite-500"
  public darkOchreIcon: string = "text-ochre-700 hover:text-ochre-500"
  public lightkOchreIcon: string = "text-ochre-100 hover:text-ochre-500"
  public darkText: string = "bg-malachite-400 hover:bg-malachite-600"
  public lightText: string = "bg-malachite-400 hover:bg-malachite-600"

  public get themeText() {
    if (this.darkMode) return this.darkText
    else return this.lightText
  }

  public get themeGreenIcon() {
    if (this.darkMode) return this.darkGreenIcon
    else return this.lightGreenIcon
  }

  public get themeOchreIcon() {
    if (this.darkMode) return this.darkOchreIcon
    else return this.lightkOchreIcon
  }

  public setMonetizationTag() {
    // https://github.com/Techgethr/webmonvuejs/blob/main/index.js
    // https://webmonetization.org/docs/start-stop/
    const monetizationTag = document.querySelector('meta[name="monetization"]')
    if (!monetizationTag && this.coilPointer) {
      const meta = document.createElement("meta")
      meta.name = "monetization"
      meta.content = this.coilPointer
      document.getElementsByTagName("head")[0].appendChild(meta)
    }
    if (monetizationTag && !this.coilPointer) {
      monetizationTag.remove()
    }
  }

  public async toggleMonetizationStreaming() {
    if (!this.isStreaming) await this.startMonetizationStream()
    else await this.stopMonetizationStream()
    this.setMonetizationTag()
  }
}
</script>

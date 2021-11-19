<template>
  <div class="relative flex flex-col max-w-xs sm:max-w-screen-sm mx-auto my-4">
    <div class="relative flex flex-row justify-center">
      <div class="text-xs sm:text-sm text-ochre-100 mx-1 my-auto">0</div>
      <div class="mx-3 my-auto">
        <input
          class="rounded-lg appearance-none bg-woad-100 h-3 w-52"
          type="range"
          name="rangeInput"
          min="0"
          max="1"
          step="0.01"
          :value="completion"
          @change.stop="setReaderPagePercent"
        />
      </div>
      <div class="text-xs sm:text-sm text-ochre-100 mx-1 my-auto">100%</div>
    </div>
  </div>
</template>

<script lang="ts">
import { Component, Vue, Mutation, Prop } from "nuxt-property-decorator"

@Component
export default class NavigationReaderSlider extends Vue {
  @Prop(String) readonly completion!: string
  @Mutation("main/setWatchReaderCFI") setWatchReaderCFI

  public async setReaderPagePercent({ target }) {
    await this.setWatchReaderCFI(`completion-${target.value}`)
  }
}
</script>

<style>
@media screen and (-webkit-min-device-pixel-ratio: 0) {
  input[type="range"]::-webkit-slider-thumb {
    width: 15px;
    -webkit-appearance: none;
    appearance: none;
    height: 15px;
    cursor: ew-resize;
    background: #4974a5;
    border-radius: 40%;
  }
}
</style>

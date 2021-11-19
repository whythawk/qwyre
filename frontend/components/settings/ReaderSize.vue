<template>
  <div class="relative flex flex-col max-w-xs sm:max-w-screen-sm mx-auto my-4">
    <div class="relative flex flex-row justify-center">
      <div class="text-xs text-ochre-100 mx-1 my-auto">Aa</div>
      <div class="mx-3 my-auto">
        <input
          class="rounded-lg appearance-none bg-woad-100 h-3 w-52"
          type="range"
          name="rangeInput"
          min="50"
          max="200"
          step="10"
          :value="pageSize"
          @change.stop="setReaderRangeOption"
        />
      </div>
      <div class="text-3xl text-ochre-100 mx-1 my-auto">Aa</div>
    </div>
  </div>
</template>

<script lang="ts">
import { Component, Vue, Getter, Mutation } from "nuxt-property-decorator"

@Component
export default class SettingsReaderSize extends Vue {
  @Getter("main/pageSize") pageSize
  @Mutation("main/setSize") setSize

  public setReaderRangeOption({ target }) {
    this.setSize(target.value)
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

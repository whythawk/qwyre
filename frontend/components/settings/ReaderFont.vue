<template>
  <div class="relative flex flex-col max-w-xs sm:max-w-screen-sm mx-auto my-4">
    <div class="relative flex flex-row justify-center">
      <button
        v-for="ro in readerOptions"
        :key="`reader-option-${ro.option}-${ro.active}`"
        :class="`${
          ro.active
            ? 'btn-ochre-light-extended-selected'
            : 'btn-ochre-light-extended'
        } text-xs sm:text-sm mx-2 font-${ro.class}`"
        @click.stop="setReaderOption(ro.option)"
      >
        {{ ro.name }}
      </button>
    </div>
  </div>
</template>

<script lang="ts">
import {
  Component,
  Vue,
  Getter,
  Mutation,
  Action,
  Watch,
} from "nuxt-property-decorator"
import { IPageFont } from "@/interfaces"

@Component
export default class SettingsReaderFont extends Vue {
  @Getter("main/pageFont") pageFont
  @Mutation("main/setFont") setFont
  @Action("main/storeThemeState") storeThemeState

  public readerOptions: { [key: string]: string | boolean }[] = [
    {
      name: "Serif",
      option: "serif",
      class: "serif",
      active: false,
    },
    {
      name: "Sans-serif",
      option: "sans_serif",
      class: "sans",
      active: false,
    },
  ]

  @Watch("pageFont")
  public refreshReaderOptions() {
    const currentOption = this.pageFont
    const oldSetting = this.readerOptions.filter((ro) => ro.active)
    if (oldSetting.length === 1) oldSetting[0].active = false
    const newSetting = this.readerOptions.filter(
      (ro) => ro.option === currentOption
    )[0]
    newSetting.active = true
  }

  public async setReaderOption(option: IPageFont) {
    await this.setFont(option)
    await this.storeThemeState()
    // await this.refreshReaderOptions()
  }

  async created() {
    await this.refreshReaderOptions()
  }
}
</script>

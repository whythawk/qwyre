<template>
  <div
    class="
      relative
      flex flex-row
      justify-center
      max-w-xs
      sm:max-w-screen-sm
      mx-auto
      my-4
    "
  >
    <button
      v-for="(ro, i) in readerOptions"
      :key="`reader-option-${ro.option}-${ro.active}`"
      :class="`${
        ro.active
          ? 'btn-ochre-light-extended-selected'
          : 'btn-ochre-light-extended'
      } ${i === 0 ? 'ml-2' : ''} text-xs sm:text-sm -pl-5 mr-2 sm:mx-3 font-${
        ro.class
      }`"
      @click.stop="setReaderOption(ro.option)"
    >
      <SvgIcon terms="w-4 h-3 inline-block mr-1" :icon="ro.icon" />
      <span>{{ ro.name }}</span>
    </button>
  </div>
</template>

<script lang="ts">
import {
  Component,
  Vue,
  Getter,
  Mutation,
  Action,
} from "nuxt-property-decorator"
import { IPageSpacing } from "@/interfaces"

@Component
export default class SettingsReaderSpacing extends Vue {
  @Getter("main/pageSpacing") pageSpacing
  @Mutation("main/setSpacing") setSpacing
  @Action("main/storeThemeState") storeThemeState

  public readerOptions: { [key: string]: string | boolean }[] = [
    {
      name: "Tight",
      option: "tight",
      active: false,
      icon: "svgMenu",
    },
    {
      name: "Default",
      option: "default",
      active: false,
      icon: "svgMenuAlt",
    },
    {
      name: "Double",
      option: "double",
      active: false,
      icon: "svgMinus",
    },
    {
      name: "Source",
      option: "source",
      active: false,
      icon: "svgMenu",
    },
  ]

  public async refreshReaderOptions() {
    const currentOption = await this.pageSpacing
    const oldSetting = this.readerOptions.filter((ro) => ro.active)
    if (oldSetting.length === 1) oldSetting[0].active = false
    const newSetting = this.readerOptions.filter(
      (ro) => ro.option === currentOption
    )[0]
    newSetting.active = true
  }

  public async setReaderOption(option: IPageSpacing) {
    await this.setSpacing(option)
    await this.storeThemeState()
    await this.refreshReaderOptions()
  }

  async created() {
    await this.refreshReaderOptions()
  }
}
</script>

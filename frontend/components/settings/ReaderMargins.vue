<template>
  <div
    class="relative flex flex-row justify-center max-w-xs sm:max-w-screen-sm mx-auto my-4"
  >
    <button
      v-for="ro in readerOptions"
      :key="`reader-option-${ro.option}-${ro.active}`"
      :class="`${
        ro.active
          ? 'btn-ochre-light-extended-selected'
          : 'btn-ochre-light-extended'
      } text-sm mx-3 font-${ro.class}`"
      @click.stop="setReaderOption(ro.option)"
    >
      {{ ro.name }}
    </button>
  </div>
</template>

<script lang="ts">
import { Component, Vue, Getter, Mutation } from "nuxt-property-decorator"
import { PageFont } from "@/store/main/state"

@Component
export default class SettingsReaderFont extends Vue {
  @Getter("main/pageFont") pageFont
  @Mutation("main/setFont") setFont

  public readerOptions: { [key: string]: string | boolean }[] = [
    {
      name: "Serif",
      option: "serif",
      class: "serif",
      active: false,
      icon: "",
    },
    {
      name: "Sans-serif",
      option: "sans_serif",
      class: "sans",
      active: false,
      icon: "",
    },
    {
      name: "Source",
      option: "source",
      class: "serif",
      active: false,
      icon: "",
    },
  ]

  public async refreshReaderOptions() {
    const currentOption = await this.pageFont
    const oldSetting = this.readerOptions.filter((ro) => ro.active)
    if (oldSetting.length === 1) oldSetting[0].active = false
    const newSetting = this.readerOptions.filter(
      (ro) => ro.option === currentOption
    )[0]
    newSetting.active = true
  }

  public async setReaderOption(name: PageFont) {
    await this.setFont(name)
    await this.refreshReaderOptions()
  }

  async created() {
    await this.refreshReaderOptions()
  }
}
</script>

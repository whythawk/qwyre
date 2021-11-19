<template>
  <div class="max-w-xs sm:max-w-screen-sm mx-auto">
    <nav class="relative flex flex-col" aria-label="Tabs">
      <div class="relative flex justify-center -mb-px space-x-0 sm:space-x-8">
        <button
          v-for="(option, i) in navigation"
          :key="`option-${i}`"
          :class="`text-xs sm:text-sm ${
            option.active
              ? 'text-woad-400 hover:text-woad-100 border-woad-400 hover:border-woad-100'
              : 'text-ochre-100 hover:text-ochre-300 hover:border-ochre-300'
          } px-2 sm:px-4 group inline-flex items-center py-4 border-b-2 border-transparent focus:outline-none`"
          @click.stop="setCurrentOption(option.name)"
        >
          <SvgIcon
            :terms="`${
              option.active
                ? 'text-woad-400 group-hover:text-woad-100'
                : 'text-ochre-100 group-hover:text-ochre-300'
            } -ml-0.5 mr-2 h-4 w-4`"
            :icon="option.icon"
          />
          <span>{{ option.name }}</span>
        </button>
      </div>
      <div
        v-show="currentOption === 'Contents'"
        class="relative flex flex-col max-w-xs sm:max-w-screen-sm my-4 mx-auto h-56 sm:h-72"
      >
        <NavigationReaderContents />
        <NavigationReaderSlider :completion="completion" />
      </div>
      <div
        v-show="currentOption === 'Theme'"
        class="relative flex flex-col max-w-xs sm:max-w-screen-sm my-4 mx-auto overflow-y-auto h-56 sm:h-72"
      >
        <div class="text-xs sm:text-sm text-ochre-100">Theme</div>
        <SettingsReaderTheme />
        <div class="text-xs sm:text-sm text-ochre-100">Font</div>
        <SettingsReaderFont />
        <div class="text-xs sm:text-sm text-ochre-100">Size</div>
        <SettingsReaderSize />
      </div>
    </nav>
  </div>
</template>

<script lang="ts">
import { Component, Vue, Getter, Action, Prop } from "nuxt-property-decorator"

@Component
export default class NavigationReaderOptions extends Vue {
  @Prop(String) readonly completion!: string
  @Getter("collections/firstCollection") firstCollection
  @Getter("main/isLoggedIn") isLoggedIn
  @Action("main/logOut") userLogOut

  public navigation = [
    {
      name: "Contents",
      active: true,
      icon: "svgMenu",
    },
    {
      name: "Theme",
      active: false,
      icon: "svgAdjustments",
    },
  ]

  public currentOption: string = "Contents"

  public setCurrentOption(name: string) {
    const oldOption = this.navigation.filter((option) => option.active)[0]
    oldOption.active = false
    const newOption = this.navigation.filter(
      (option) => option.name === name
    )[0]
    newOption.active = true
    this.currentOption = name
  }

  public async logout() {
    await this.userLogOut()
  }
}
</script>

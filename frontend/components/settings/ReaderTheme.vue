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
    <div class="text-xs sm:text-sm text-ochre-100 mx-2 my-auto">Light</div>
    <button
      type="button"
      :class="`${
        theme ? 'bg-ochre-500' : 'bg-ochre-100'
      } relative inline-flex flex-shrink-0 h-6 w-11 border-2 border-transparent rounded-full cursor-pointer transition-colors ease-in-out duration-200 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-ochre-500`"
      role="switch"
      aria-checked="false"
      @click.stop="setReaderOption"
    >
      <span class="sr-only">Use setting</span>
      <!-- Enabled: "translate-x-5", Not Enabled: "translate-x-0" -->
      <span
        aria-hidden="true"
        :class="`${
          theme ? 'translate-x-5' : 'translate-x-0'
        } pointer-events-none inline-block h-5 w-5 rounded-full bg-ochre-10 shadow transform ring-0 transition ease-in-out duration-200`"
      ></span>
    </button>
    <div class="text-xs sm:text-sm text-ochre-100 mx-2 my-auto">Dark</div>
  </div>
</template>

<script lang="ts">
import {
  Component,
  Vue,
  Getter,
  Mutation,
  Watch,
  Action,
} from "nuxt-property-decorator"

@Component
export default class SettingsReaderTheme extends Vue {
  @Getter("main/pageTheme") pageTheme
  @Mutation("main/setTheme") setTheme
  @Action("main/storeThemeState") storeThemeState

  public theme: boolean = false

  public async setReaderOption() {
    this.theme = !this.theme
    if (this.theme) await this.setTheme("dark")
    else await this.setTheme("light")
    await this.storeThemeState()
  }

  @Watch("pageTheme")
  public setPageTheme() {
    this.theme = this.pageTheme === "dark"
  }

  created() {
    this.setPageTheme()
  }
}
</script>

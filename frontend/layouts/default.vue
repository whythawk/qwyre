<template>
  <div class="relative bg-ochre-10">
    <div class="max-w-full mx-auto">
      <div class="bg-ochre-900">
        <NavigationDefaultMenu />
      </div>
      <ConversionSteps />
      <main>
        <div class="max-w-7xl mx-auto sm:px-6 lg:px-8">
          <div class="container mx-auto lg:px-40">
            <div class="min-h-screen flex">
              <Nuxt />
            </div>
          </div>
        </div>
      </main>
      <footer class="mt-12 mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">
        <NotificationsBar />
        <FooterBar />
      </footer>
      <div class="z-40 fixed inset-x-0 bottom-0 w-screen flex">
        <div class="w-screen">
          <div class="bg-ochre-900">
            <div class="relative flex-1 px-4 sm:px-6">
              <NavigationDefaultLowerMenu />
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script lang="ts">
import { Component, Getter, Watch, Vue } from "nuxt-property-decorator"

@Component({
  name: "defaultLayout",
})
export default class DefaultLayout extends Vue {
  @Getter("monetization/btpToken") btpToken
  @Getter("monetization/isStreaming") isStreaming

  @Watch("btpToken", { immediate: true })
  updateCoilMonetizationState() {
    if (
      process.client &&
      Object.prototype.hasOwnProperty.call(document, "coilMonetizationPolyfill")
    )
      try {
        ;(document as any).coilMonetizationPolyfill.refreshBtpToken(
          this.btpToken
        )
      } catch (error) {}
  }

  created() {
    if (
      process.client &&
      Object.prototype.hasOwnProperty.call(document, "coilMonetizationPolyfill")
    )
      try {
        ;(document as any).coilMonetizationPolyfill.init({
          btpToken: this.btpToken,
        })
      } catch (error) {}
  }
}
</script>

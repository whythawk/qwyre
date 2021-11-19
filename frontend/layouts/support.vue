<template>
  <div class="relative bg-ochre-10">
    <!--Header-->
    <div
      class="max-w-full mx-auto md:bg-support-the-qwyre md:bg-no-repeat bg-contain"
    >
      <NavigationCoverMenu />
      <!--Main Container-->
      <main>
        <Nuxt />
      </main>
      <footer class="mt-12 mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">
        <NotificationsBar />
        <FooterBar />
      </footer>
    </div>
  </div>
</template>

<script lang="ts">
import { Component, Getter, Watch, Vue } from "nuxt-property-decorator"

@Component({
  name: "supportLayout",
})
export default class SupportLayout extends Vue {
  @Getter("monetization/btpToken") btpToken
  @Getter("monetization/isStreaming") isStreaming

  @Watch("btpToken", { immediate: true })
  updateCoilMonetizationState() {
    if (
      process.client &&
      Object.prototype.hasOwnProperty.call(document, "coilMonetizationPolyfill")
    )
      (document as any).coilMonetizationPolyfill.refreshBtpToken(this.btpToken)
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

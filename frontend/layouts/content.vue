<template>
  <div class="relative bg-ochre-10 overflow-hidden">
    <div class="max-w-full mx-auto">
      <div class="bg-ochre-900">
        <NavigationDefaultMenu />
      </div>
      <main>
        <div class="container mx-auto">
          <div class="min-h-screen flex justify-center mt-8">
            <article class="max-w-none sm:w-3/5 prose">
              <Nuxt />
            </article>
          </div>
        </div>
      </main>
      <footer class="mt-12 mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">
        <FooterBar />
      </footer>
    </div>
  </div>
</template>

<script lang="ts">
import { Component, Getter, Watch, Vue } from "nuxt-property-decorator"

@Component({
  name: "contentLayout",
})
export default class ContentLayout extends Vue {
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

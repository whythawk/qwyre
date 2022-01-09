<template>
  <div class="relative bg-ochre-10 overflow-hidden">
    <div class="max-w-full mx-auto">
      <div class="bg-ochre-900">
        <NavigationDefaultMenu />
      </div>
      <main>
        <div class="container mx-auto">
          <div class="min-h-screen flex justify-center">
            <article
              class="
                max-w-none
                sm:w-3/5
                prose prose-reader-light prose-reader-base prose-reader-compact
              "
            >
              <Nuxt />
            </article>
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

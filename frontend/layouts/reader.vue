<template>
  <div class="overflow-hidden">
    <main>
      <Nuxt />
    </main>
    <footer class="container mx-auto">
      <NotificationsBar />
    </footer>
  </div>
</template>

<script lang="ts">
import {
  Component,
  Getter,
  Mutation,
  Watch,
  Vue,
} from "nuxt-property-decorator"
import { ICoilMonetizationProgress } from "@/interfaces"

@Component({
  name: "readerLayout",
})
export default class ReaderLayout extends Vue {
  @Mutation("monetization/setCoilReceipt") setCoilReceipt
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

  updateMonetizationProgress(event) {
    this.setCoilReceipt(event.detail.paymentPointer)
  }

  stopMonetizationProgress(_event) {
    this.setCoilReceipt("")
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
    if (
      process.client &&
      Object.prototype.hasOwnProperty.call(document, "monetization")
    ) {
      try {
        ;(document as any).monetization.addEventListener(
          "monetizationprogress",
          this.updateMonetizationProgress
        )
        ;(document as any).monetization.addEventListener(
          "monetizationstop",
          this.stopMonetizationProgress
        )
      } catch (error) {}
    }
  }
}
</script>

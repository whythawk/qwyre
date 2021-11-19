<template>
  <div
    ref="import-work"
    class="grid grid-rows-6 grid-cols-0 gap-1 bg-malachite-100 rounded-lg max-h-full"
  >
    <div class="row-start-2 row-span-2">
      <SvgIcon
        terms="h-10 w-10 sm:h-20 sm:w-16 mx-auto my-auto block text-malachite-600"
        icon="svgBookOpen"
      />
    </div>
    <div class="row-span-3">
      <button
        type="submit"
        class="btn-malachite-sm sm:btn-malachite mx-auto my-auto block"
      >
        <SvgIcon terms="w-5 h-6 sm:w-10 sm:h-8 inline-block" icon="svgPlus" />
      </button>
    </div>
  </div>
</template>

<script lang="ts">
import { fileOpen } from "browser-fs-access"
import { Component, Ref, mixins } from "nuxt-property-decorator"
import importWorkData from "@/mixins/importWorkData"

@Component
export default class ImportWorkCollection extends mixins(importWorkData) {
  @Ref("import-work") readonly openWork!: HTMLButtonElement

  mounted(): void {
    this.openWork.disabled = false
    this.openWork.addEventListener("click", async () => {
      try {
        const blob = await fileOpen({
          mimeTypes: ["application/epub+zip"],
          extensions: [".epub"],
        })
        this.storeWork(blob)
      } catch (err) {
        if (err.name !== "AbortError") {
          return console.error(err)
        }
      }
    })
  }
}
</script>

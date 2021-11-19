<template>
  <div
    :ref="`import-${collection}`"
    :class="`grid grid-rows-6 grid-cols-0 gap-1 bg-malachite-100 rounded-lg max-h-full ${
      collection === 'conversion' ? 'filter sepia' : ''
    }`"
    @click.prevent="submit"
  >
    <div class="row-start-2 row-span-2">
      <SvgIcon
        terms="h-10 w-10 sm:h-20 sm:w-16 mx-auto my-auto block text-malachite-600"
        icon="svgBookmark"
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
import { Component, Mutation, Prop, Vue } from "nuxt-property-decorator"

@Component
export default class CreateCollection extends Vue {
  @Prop(String) readonly collection!: string
  @Mutation("collections/setCollection") setCollection
  @Mutation("conversions/setConversionKey") setConversionKey

  public routerPaths: { [key: string]: string } = {
    conversion: "/convert/description",
    anthology: "/anthology",
    series: "/series",
  }

  submit() {
    if (this.collection === "conversion") this.setConversionKey(null)
    this.$router.push(this.routerPaths[this.collection])
  }
}
</script>

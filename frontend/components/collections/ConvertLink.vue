<template>
  <div>
    <button
      type="submit"
      class="btn-sinopia-extended flex items-center"
      @click.prevent="submit"
    >
      <SvgIcon terms="w-5 h-4 inline-block mr-1 mb-1" icon="svgBookOpen" />
      <span class="text-sm">Publish</span>
    </button>
  </div>
</template>

<script lang="ts">
import { Component, Mutation, Vue } from "nuxt-property-decorator"

@Component
export default class CollectionsConvertLink extends Vue {
  @Mutation("conversions/setConversionKey") setConversionKey

  submit() {
    this.setConversionKey(null)
    this.$router.push("/write/describe")
  }
}
</script>

<template>
  <div>
    <button
      type="submit"
      class="btn-woad-extended-sm flex items-center h-8"
      @click.prevent="submit"
    >
      <SvgIcon terms="w-5 h-4 inline-block mr-1 mb-1" icon="svgDocumentText" />
      <span class="text-sm">Convert .docx</span>
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
    this.$router.push("/convert/description")
  }
}
</script>

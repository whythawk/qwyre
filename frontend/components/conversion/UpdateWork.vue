<template>
  <div class="max-w-2xl mx-auto">
    <button
      type="submit"
      class="btn-malachite-extended"
      @click.prevent="update"
    >
      <SvgIcon terms="w-5 h-4 inline-block mr-1" icon="svgBookOpen" />
      <span>Update work</span>
    </button>
  </div>
</template>

<script lang="ts">
import { Component, Mutation, Prop, Vue } from "nuxt-property-decorator"
import { idb } from "@/api"

@Component
export default class ConversionUpdateWork extends Vue {
  @Prop(String) readonly workId!: string
  @Prop(String) readonly workUid!: string
  @Mutation("conversions/setConversionKey") setConversionKey

  public async update() {
    let checkKey = 0
    checkKey = await idb.hasKey("conversion", this.workUid)
    if (checkKey === 1) this.setConversionKey(this.workUid)
    this.$router.push({
      path: "/write/describe",
      query: {
        work: this.workId,
      },
    })
  }
}
</script>

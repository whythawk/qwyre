<template>
  <div>
    <button type="submit" class="focus:outline-none" @click.prevent="submit">
      <SvgIcon terms="w-5 h-6 pt-1 text-sinopia-700" icon="svgTrash" />
    </button>
  </div>
</template>

<script lang="ts">
import { Component, Action, Prop, Vue } from "nuxt-property-decorator"

@Component
export default class CreateCollection extends Vue {
  @Prop(String) readonly collection!: string
  @Prop(String) readonly collectionKey!: string
  @Action("collections/removeCollectionPayload") removeCollectionPayload

  submit() {
    this.removeCollectionPayload({
      collection: this.collection,
      key: this.collectionKey,
    })
  }
}
</script>

<template>
  <div
    v-if="!src"
    class="
      inline-block
      bg-ochre-100
      rounded-lg
      h-16
      w-9
      sm:h-24 sm:w-14
      md:h-32 md:w-20
    "
  >
    <div class="mt-6">
      <SvgIcon
        terms="h-6 w-6 sm:h-8 sm:w-8 mx-auto my-auto block text-ochre-600"
        icon="svgBookmark"
      />
    </div>
  </div>
  <div v-else>
    <img
      :src="src"
      :alt="alt"
      class="inline-block rounded-lg max-h-16 sm:max-h-24 md:max-h-32"
    />
  </div>
</template>

<script lang="ts">
import { Component, Prop, Vue } from "nuxt-property-decorator"

@Component
export default class SourcesCoverImage extends Vue {
  @Prop(String) readonly src!: String
  @Prop(String) readonly alt!: String
}
</script>

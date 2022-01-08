<template>
  <div v-if="work">
    <p
      v-for="(spine, i) in work.spine"
      :key="`spine-${i}`"
      class="text-sm py-3"
    >
      {{ spine }}
    </p>
  </div>
</template>

<script lang="ts">
import { Component, Prop, Vue } from "nuxt-property-decorator"
import { IWorkSummary } from "@/interfaces"

@Component
export default class CollectionsWorkSummarySpineTab extends Vue {
  @Prop(Object) readonly work!: IWorkSummary
}
</script>

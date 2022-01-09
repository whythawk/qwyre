<template>
  <div v-if="work">
    <!--- eslint-disable-next-line vue/no-v-html -->
    <div v-html="work.first500"></div>
  </div>
</template>

<script lang="ts">
import { Component, Prop, Vue } from "nuxt-property-decorator"
import { IWorkSummary } from "@/interfaces"

@Component
export default class CollectionsWorkSummaryFirst500Tab extends Vue {
  @Prop(Object) readonly work!: IWorkSummary
}
</script>

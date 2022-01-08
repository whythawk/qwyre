<template>
  <div class="container min-h-screen mx-auto">
    <TitleBar title="Library" />
    <CollectionsLibrary />
  </div>
</template>

<script lang="ts">
import { Component, Vue } from "nuxt-property-decorator"

@Component({
  middleware: "refresh-authentication",
  layout: "working",
})
export default class Library extends Vue {
  public collection: string = "work"
  public isFilterOpen: boolean = false
}
</script>

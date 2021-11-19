<template>
  <div class="container min-h-screen mx-auto">
    <div class="text-center py-16 px-4 sm:px-6 lg:px-8">
      <h1 class="text-4xl font-extrabold tracking-tight text-gray-900">
        Reading collection
      </h1>
    </div>
    <CollectionsLibrary collection="work" />
  </div>
</template>

<script lang="ts">
import { Component, Vue } from "nuxt-property-decorator"

@Component({
  middleware: "anonymous",
  layout: "working",
})
export default class Library extends Vue {
  public collection: string = "work"
  public isFilterOpen: boolean = false
}
</script>

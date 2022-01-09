<template>
  <div class="container min-h-screen mx-auto flex flex-col">
    <TitleBar title="Creator" />
  </div>
</template>

<script lang="ts">
import { Component, Vue } from "nuxt-property-decorator"

@Component({
  layout: "working",
  middleware: "refresh-authentication",
})
export default class WorkshopLink extends Vue {
  async asyncData({ store, route, redirect }) {
    const creator = await store.getters["main/creatorProfile"]
    if (creator && creator.identifier === route.params.id) {
      redirect("/creator")
    }
  }
}
</script>

<template>
  <div>
    <TitleBar :title="page.title" />
    <div class="-mt-12">
      <nuxt-content :document="page" />
    </div>
  </div>
</template>

<script lang="ts">
import { Component, Vue } from "nuxt-property-decorator"

@Component({
  layout: "content",
  middleware: "refresh-authentication",
})
export default class ShortStoryContent extends Vue {
  async asyncData({ $content }) {
    const page = await $content("short-story").fetch()
    return {
      page,
    }
  }
}
</script>

<template>
  <div>
    <TitleBar title="Redirecting" />
  </div>
</template>

<script lang="ts">
import { Component, Vue } from "nuxt-property-decorator"

@Component({
  layout: "content",
  middleware: "refresh-authentication",
})
export default class ShortStoryContent extends Vue {
  asyncData({ redirect }) {
    redirect("/creators-fund")
  }
}
</script>

<template>
  <div>
    <TitleBar title="Series" />
  </div>
</template>

<script lang="ts">
import { Component, Vue } from "nuxt-property-decorator"

@Component({
  layout: "working",
  middleware: "refresh-authentication",
})
export default class Series extends Vue {}
</script>

<template>
  <div>
    <TitleBar title="Anthology" />
  </div>
</template>

<script lang="ts">
import { Component, Vue } from "nuxt-property-decorator"

@Component({
  layout: "working",
  middleware: "refresh-authentication",
})
export default class Anthology extends Vue {}
</script>

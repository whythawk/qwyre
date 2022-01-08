<template>
  <div>
    <TitleBar title="Moderate" />
  </div>
</template>

<script lang="ts">
import { Component, Vue } from "nuxt-property-decorator"

@Component({
  layout: "working",
  middleware: "authenticated",
})
export default class Moderate extends Vue {}
</script>

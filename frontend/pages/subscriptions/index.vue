<template>
  <div>
    <TitleBar title="Subscriptions" />
  </div>
</template>

<script lang="ts">
import { Component, Vue } from "nuxt-property-decorator"

@Component({
  layout: "working",
  middleware: "refresh-authentication",
})
export default class Subscriptions extends Vue {}
</script>

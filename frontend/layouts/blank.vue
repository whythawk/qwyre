<template>
  <div class="relative bg-ochre-10">
    <Nuxt />
  </div>
</template>

<script lang="ts">
import { Component, Vue } from "nuxt-property-decorator"

@Component({
  name: "blankLayout",
})
export default class BlankLayout extends Vue {}
</script>

<template>
  <header v-if="headingTitle">
    <div class="max-w-7xl mx-auto -mt-4 pb-6 px-4 sm:px-6 lg:px-8">
      <h1 class="mt-8 mb-8 text-3xl text-ochre-900">
        {{ headingTitle }}
      </h1>
    </div>
  </header>
</template>

<script lang="ts">
import { Component, Vue, Getter } from "nuxt-property-decorator"

@Component
export default class HeadingBar extends Vue {
  @Getter("settings/headingTitle") headingTitle
}
</script>

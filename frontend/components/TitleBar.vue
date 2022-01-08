<template>
  <header v-if="title">
    <div
      class="
        text-center
        pt-10
        pb-8
        sm:pt-16 sm:pb-14
        px-4
        sm:px-6
        lg:px-8
        mt-16
      "
    >
      <h1 class="text-4xl font-extrabold tracking-tight text-gray-900">
        {{ title }}
      </h1>
    </div>
  </header>
</template>

<script lang="ts">
import { Component, Vue, Prop } from "nuxt-property-decorator"

@Component
export default class TitleBar extends Vue {
  @Prop(String) readonly title!: string
}
</script>

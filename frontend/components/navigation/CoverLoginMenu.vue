<template>
  <div>
    <NuxtLink
      v-if="!isLoggedIn"
      class="
        text-xs
        sm:text-sm
        text-ochre-100
        hover:text-ochre-500
        px-3
        sm:px-8
        flex flex-col flex-shrink-0
      "
      to="/login"
      >Sign in
      <SvgIcon terms="h-6 w-6 fill-current mt-2 mx-auto" icon="svgUser" />
    </NuxtLink>
    <NuxtLink
      v-else
      class="
        text-xs
        sm:text-sm
        text-ochre-100
        hover:text-ochre-500
        px-3
        sm:px-8
        flex flex-col flex-shrink-0
      "
      to="/creator"
      >Profile<SvgIcon terms="h-6 w-6 fill-current mt-2 mx-auto" icon="svgUser"
    /></NuxtLink>
  </div>
</template>

<script lang="ts">
import { Component, Vue, Getter } from "nuxt-property-decorator"

@Component
export default class NavigationCoverLoginMenu extends Vue {
  @Getter("main/isLoggedIn") isLoggedIn
}
</script>

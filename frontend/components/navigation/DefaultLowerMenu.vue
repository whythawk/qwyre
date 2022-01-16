<template>
  <div class="max-w-full sm:max-w-screen mx-auto">
    <nav class="relative flex justify-center max-h-16 py-1" aria-label="Global">
      <NuxtLink
        v-for="(nav, i) in navigation"
        :key="`nav-${i}`"
        :to="nav.to"
        class="
          text-xs
          sm:text-sm
          text-ochre-100
          hover:text-ochre-500
          px-7
          sm:px-14
          flex flex-col flex-shrink-0
        "
        >{{ nav.name }}
        <SvgIcon terms="h-6 w-6 fill-current mt-2 mx-auto" :icon="nav.icon" />
      </NuxtLink>
      <MonetizationMenuToggle :dark-mode="monetizationDark" />
    </nav>
  </div>
</template>

<script lang="ts">
import { Component, Vue } from "nuxt-property-decorator"

@Component
export default class NavigationDefaultLowerMenu extends Vue {
  public monetizationDark: boolean = false

  public navigation = [
    {
      name: "Home",
      to: "/",
      icon: "svgHome",
    },
    {
      name: "Search",
      to: "/search",
      icon: "svgSearch",
    },
    {
      name: "Library",
      to: "/library",
      icon: "svgBookOpen",
    },
  ]
}
</script>

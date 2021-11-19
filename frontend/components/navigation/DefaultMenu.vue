<template>
  <div class="max-w-full sm:max-w-screen mx-auto">
    <nav class="relative flex justify-center max-h-16 py-1" aria-label="Global">
      <NuxtLink
        v-for="(nav, i) in navigation"
        :key="`nav-${i}`"
        :to="nav.centre && cover ? '/read' : nav.to"
        class="text-xs sm:text-sm text-ochre-100 hover:text-ochre-500 px-3 sm:px-8 flex flex-col flex-shrink-0"
        >{{ nav.name }}
        <div v-if="nav.centre">
          <div v-if="cover">
            <img
              class="mx-auto h-20 border border-ochre-900 rounded-lg shadow-xl"
              :src="cover"
            />
          </div>
          <div v-else>
            <SvgIcon
              terms="h-20 w-20 fill-current mx-auto bg-ochre-900 rounded-full shadow-xl mt-2 p-4"
              :icon="nav.icon"
            />
          </div>
        </div>
        <div v-else>
          <SvgIcon terms="h-6 w-6 fill-current mt-2 mx-auto" :icon="nav.icon" />
        </div>
      </NuxtLink>
      <MonetizationMenuToggle :dark-mode="monetizationDark" />
    </nav>
  </div>
</template>

<script lang="ts">
import { Component, Vue, Getter, Action } from "nuxt-property-decorator"
import { idb } from "@/api"

@Component
export default class NavigationDefaultMenu extends Vue {
  @Getter("collections/firstCollection") firstCollection
  @Action("collections/restoreCollection") restoreCollection
  @Getter("main/isLoggedIn") isLoggedIn
  @Action("main/logOut") userLogOut
  public monetizationDark: boolean = false
  public cover: string | null = null

  public navigation = [
    {
      name: "Home",
      to: "/",
      icon: "svgHome",
    },
    {
      name: "Library",
      to: "/library",
      icon: "svgBookOpen",
    },
    {
      name: "",
      to: "/",
      icon: "qwyreLogo",
      centre: true,
    },
    {
      name: "Conversions",
      to: "/library/conversions",
      icon: "svgBookmark",
    },
  ]

  public async logout() {
    await this.userLogOut()
  }

  public async created() {
    const workKey = await this.firstCollection("work")
    try {
      this.cover = (await idb.getPayload("cover", workKey)) as string | null
    } catch (error) {
      console.log("error: ---->", error)
    }
  }
}
</script>

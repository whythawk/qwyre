<template>
  <div
    class="
      z-40
      absolute
      inset-x-0
      top-0
      max-w-full
      sm:max-w-screen
      mx-auto
      bg-ochre-900
    "
  >
    <nav class="relative flex justify-center max-h-16 py-1" aria-label="Global">
      <NuxtLink
        v-for="(nav, i) in navigation"
        :key="`nav-${i}`"
        :to="nav.centre && cover ? readLink : nav.to"
        class="
          text-xs
          sm:text-sm
          text-ochre-100
          hover:text-ochre-500
          px-3
          sm:px-8
          flex flex-col flex-shrink-0
        "
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
      <NavigationCoverLoginMenu />
    </nav>
  </div>
</template>

<script lang="ts">
import { Component, Vue, Getter, Action } from "nuxt-property-decorator"
import { idb } from "@/api"
import { IKeyable } from "@/interfaces"

@Component
export default class NavigationDefaultMenu extends Vue {
  @Getter("collections/firstCollection") firstCollection
  @Action("collections/restoreCollection") restoreCollection
  public monetizationDark: boolean = false
  public cover: string | null = null
  public readLink: string = "/read"

  public navigation = [
    {
      name: "Workshop",
      to: "/workshop",
      icon: "svgPencilAlt",
    },
    {
      name: "",
      to: "/",
      icon: "qwyreLogo",
      centre: true,
    },
  ]

  public async created() {
    this.readLink = "/"
    if (process.client) {
      let libraryKey = await this.firstCollection("library")
      if (!libraryKey) {
        await this.restoreCollection({ collection: "library" })
        libraryKey = await this.firstCollection("library")
      }
      if (libraryKey) {
        try {
          const cover = await idb.getPayload("cover", libraryKey)
          if (cover && typeof cover !== "string" && Object.keys(cover).length) {
            this.cover = (cover as IKeyable).data as string | null
            this.readLink = `/stream/${libraryKey}`
          } else {
            this.cover = cover as string | null
            this.readLink = "/read"
          }
        } catch (error) {}
      }
    }
  }
}
</script>

<template>
  <div class="flex flex-col">
    <div
      class="
        container
        relative
        max-w-full
        md:max-w-2xl
        mx-auto
        pt-28
        pb-12
        md:pt-32 md:pb-16
        text-center
        break-normal
        bg-ochre-900
        md:bg-opacity-0
        z-0
      "
    >
      <!-- Quotation -->
      <blockquote>
        <p
          class="
            mt-2
            text-center
            italic
            text-ochre-10 text-base
            sm:text-lg
            md:text-xl
          "
        >
          Writing is easy. You simply sit down at the typewriter, <br />open
          your veins, and bleed.
        </p>
        <p
          class="
            text-right
            mt-2
            mr-10
            text-xs
            sm:text-sm
            md:text-base
            sm:mt-5
            md:mt-5
          "
        >
          <cite class="text-malachite-100">Paul Gallico &amp; Red Smith</cite>
        </p>
      </blockquote>
      <!-- Header block -->
      <h1
        class="
          mt-8
          sm:mt-12
          text-3xl
          sm:text-4xl
          md:text-5xl
          font-extrabold
          text-ochre-10
        "
      >
        <span class="inline">Join the</span>
        <span class="inline tracking-wide text-woad-500">Qwyre ...</span>
      </h1>
    </div>
    <!-- Collections -->
    <div class="container relative mx-auto max-w-7xl">
      <div class="bg-ochre-900 md:bg-opacity-0">
        <div class="pb-12 md:pb-16 mx-2 md:mx-0">
          <SearchBar />
        </div>
      </div>
      <div class="mx-0 md:mx-6">
        <!--Lead Card-->
        <div
          class="bg-ochre-10 rounded bg-opacity-90 overflow-hidden shadow-lg"
        >
          <!-- Reading -->
          <transition
            enter-active-class="transition ease-out duration-100"
            enter-class="transform opacity-0 scale-95"
            enter-to-class="transform opacity-100 scale-100"
            leave-active-class="transition ease-in duration-75"
            leave-class="transform opacity-100 scale-100"
            leave-to-class="transform opacity-0 scale-95"
          >
            <div
              v-if="!libraryCollection.length"
              class="transition ease-in duration-200"
            >
              <!-- Slogan -->
              <p
                class="
                  mt-4
                  text-lg text-center
                  sm:text-xl
                  md:text-3xl
                  text-ochre-800
                "
              >
                A simple ebook
                <span class="text-malachite-500">reader</span> &amp;
                <span class="text-malachite-500">collaborative publisher</span>
              </p>
              <p
                class="
                  mt-4
                  text-md text-center
                  sm:text-lg
                  md:text-xl
                  text-ochre-700
                "
              >
                <span class="font-semibold">Go on ...</span> click this link and
                <span class="font-semibold">see what happens.</span>
              </p>
              <div class="my-8 max-w-2xl mx-auto flex justify-center">
                <button
                  class="btn-woad-extended-sm flex items-center h-10"
                  @click="readMe"
                >
                  Read me
                </button>
              </div>
            </div>
          </transition>
          <transition
            enter-active-class="transition ease-out duration-100"
            enter-class="transform opacity-0 scale-95"
            enter-to-class="transform opacity-100 scale-100"
            leave-active-class="transition ease-in duration-75"
            leave-class="transform opacity-100 scale-100"
            leave-to-class="transform opacity-0 scale-95"
          >
            <div
              v-if="libraryCollection.length"
              class="transition ease-in duration-200"
            >
              <h2
                class="relative mt-2 ml-4 text-lg font-extrabold text-ochre-800"
              >
                <span>Library</span>
                <span
                  class="
                    inline-flex
                    text-right
                    mr-4
                    text-woad-500
                    hover:text-woad-300
                  "
                >
                  <NuxtLink to="/library">... all</NuxtLink>
                  <SvgIcon
                    terms="h-5 w-5 mt-1 fill-current"
                    icon="svgChevronRight"
                  />
                </span>
              </h2>
              <CollectionsSwipeLibrary
                :library-collection="libraryCollection"
              />
            </div>
          </transition>
        </div>
        <!--/Lead Card-->
      </div>
    </div>
  </div>
</template>

<script lang="ts">
import {
  Component,
  Watch,
  Mutation,
  Getter,
  Vue,
} from "nuxt-property-decorator"
import { idb, api } from "@/api"
import { ILibrary } from "@/interfaces"
import { generateUUID } from "@/utilities"

@Component({
  layout: "cover",
  middleware: "refresh-authentication",
})
export default class CoverPage extends Vue {
  @Mutation("main/setChangeWatcher") setChangeWatcher
  @Getter("collections/collectionWatcher") collectionWatcher
  public forceRefresh: boolean = false
  public collection: string = "library"
  public libraryCollection: ILibrary[] = []

  public readMe() {
    this.$router.push(
      "/?import=https%3A%2F%2Fqwyre.com%2Fif-only-they-couldn't-talk.epub"
    )
    this.setChangeWatcher(`readme-${generateUUID()}`)
  }

  @Watch("collectionWatcher")
  public async refreshCollection() {
    if (
      (process.client && this.forceRefresh) ||
      (this.collectionWatcher &&
        ["library", "stream", "work"].includes(
          this.collectionWatcher.split("-")[0]
        ))
    ) {
      this.libraryCollection = []
      this.forceRefresh = false
      try {
        this.libraryCollection = (await idb.getLatestPayloads(
          this.collection
        )) as ILibrary[]
      } catch (e) {}
    }
  }

  async mounted() {
    this.forceRefresh = true
    await this.refreshCollection()
  }
}
</script>

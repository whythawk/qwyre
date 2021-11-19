<template>
  <div class="flex flex-col">
    <div
      class="container relative max-w-full md:max-w-2xl mx-auto pt-28 pb-12 md:pt-32 md:pb-16 text-center break-normal bg-ochre-900 md:bg-opacity-0 z-0"
    >
      <!-- Quotation -->
      <blockquote>
        <p
          class="mt-2 text-center italic text-ochre-10 text-base sm:text-lg md:text-xl"
        >
          Writing is easy. You simply sit down at the typewriter, <br />open
          your veins, and bleed.
        </p>
        <p
          class="text-right mt-2 mr-10 text-xs sm:text-sm md:text-base sm:mt-5 md:mt-5"
        >
          <cite class="text-malachite-100">Paul Gallico &amp; Red Smith</cite>
        </p>
      </blockquote>
      <!-- Header block -->
      <h1
        class="mt-8 sm:mt-12 text-3xl sm:text-4xl md:text-5xl font-extrabold text-ochre-10"
      >
        <span class="inline">Join the</span>
        <span class="inline tracking-wide text-woad-500">Qwyre ...</span>
      </h1>
      <!-- Slogan -->
      <p
        class="pt-8 text-lg sm:text-xl md:text-3xl text-ochre-50 sm:mt-5 md:mt-5"
      >
        A simple ebook <span class="text-malachite-100">converter</span> &amp;
        <span class="text-malachite-100">reader</span>.
      </p>
    </div>
    <!-- Collections -->
    <div class="container relative mx-auto max-w-7xl">
      <div class="mx-0 md:mx-6">
        <!--Lead Card-->
        <div
          class="bg-ochre-10 rounded bg-opacity-90 overflow-hidden shadow-lg"
        >
          <!-- Conversion -->
          <h2 class="relative mt-2 ml-4 text-lg font-extrabold text-ochre-800">
            <span>Conversion collection</span>
            <span
              class="inline-flex text-right mr-4 text-woad-500 hover:text-woad-300"
            >
              <NuxtLink to="/library/conversions">... all</NuxtLink>
              <SvgIcon
                terms="h-5 w-5 mt-1 fill-current"
                icon="svgChevronRight"
              />
            </span>
          </h2>
          <CollectionsSwipeLatest collection="conversion" />
          <!-- Reading -->
          <h2 class="relative mt-2 ml-4 text-lg font-extrabold text-ochre-800">
            <span>Reading collection</span>
            <span
              class="inline-flex text-right mr-4 text-woad-500 hover:text-woad-300"
            >
              <NuxtLink to="/library">... all</NuxtLink>
              <SvgIcon
                terms="h-5 w-5 mt-1 fill-current"
                icon="svgChevronRight"
              />
            </span>
          </h2>
          <CollectionsSwipeLatest collection="work" />
        </div>
        <!--/Lead Card-->
      </div>
    </div>
  </div>
</template>

<script lang="ts">
import { Component, Vue } from "nuxt-property-decorator"

@Component({
  layout: "cover",
})
export default class CoverPage extends Vue {}
</script>

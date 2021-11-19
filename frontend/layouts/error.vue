<template>
  <main class="min-h-screen bg-cover bg-top sm:bg-top bg-lost-the-qwyre">
    <div
      class="
        max-w-7xl
        mx-auto
        px-4
        py-10
        text-center
        sm:px-6 sm:py-16
        lg:px-8 lg:py-20
      "
    >
      <p
        v-show="error.statusCode === 404"
        class="text-sm font-semibold text-ochre-800 uppercase tracking-wide"
      >
        404 error
      </p>
      <h1
        class="
          mt-2
          text-4xl
          font-extrabold
          text-white
          tracking-tight
          sm:text-5xl
        "
      >
        Oy, vey! Are you ever lost.
      </h1>
      <p class="mt-2 text-lg font-medium text-ochre-50">
        If you want the library, it's over there.
      </p>
      <div class="mt-6">
        <NuxtLink
          to="/"
          class="
            inline-flex
            items-center
            px-4
            py-2
            border-2 border-ochre-10 border-opacity-0
            ring-2 ring-ochre-10 ring-opacity-75
            sm:ring-opacity-25
            text-sm
            font-medium
            rounded-full
            text-ochre-800 text-opacity-75
            bg-ochre-10 bg-opacity-75
            sm:bg-opacity-25 sm:hover:bg-opacity-50
          "
        >
          Go back home
        </NuxtLink>
      </div>
    </div>
  </main>
</template>

<script lang="ts">
import { Component, Prop, Vue } from "nuxt-property-decorator"

@Component({
  name: "Layout404",
  layout: "blank",
})
export default class Layout404 extends Vue {
  @Prop() readonly error!: any
}
</script>

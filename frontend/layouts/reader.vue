<template>
  <div class="relative bg-ochre-10 overflow-hidden">
    <div class="max-w-7xl mx-auto">
      <main>
        <div class="container mx-auto">
          <div class="h-screen flex justify-center">
            <article>
              <Nuxt />
            </article>
          </div>
        </div>
      </main>
    </div>
  </div>
</template>

<script lang="ts">
import { Component, Vue } from "nuxt-property-decorator"

@Component({
  name: "readerLayout",
})
export default class ReaderLayout extends Vue {}
</script>

<template>
  <div
    class="
      relative
      mx-auto
      px-3
      py-3
      sm:px-6 sm:py-10
      flex flex-col
      items-center
      text-center
      lg:px-0
    "
  >
    <div class="w-full flex justify-between px-2 sm:px-16 space-x-3">
      <div class="flex-1">
        <h1 class="text-lg font-semibold text-ochre-800">
          This isn't the end
          <span v-if="streamFields.title">
            of <span class="italic">{{ streamFields.title }}</span>
          </span>
          ...
        </h1>
      </div>
      <div v-if="streamFields.cover">
        <SourcesCoverImage :src="streamFields.cover" />
      </div>
    </div>
    <p class="mt-2 sm:mt-6 text-md text-ochre-800">
      Toggle the Monetization icon in the menu-bar to start and stop streaming
      payments.
    </p>
    <div class="inline-flex">
      <span
        class="
          mt-2
          sm:mt-6
          text-lg
          font-semibold
          text-malachite-400
          flex flex-col flex-shrink-0
        "
      >
        Streaming
        <SvgIcon terms="h-10 w-10 mx-auto mt-2" icon="svgMonetizationStatic" />
      </span>
      <span
        class="
          mt-2
          sm:mt-6
          ml-12
          text-lg
          font-semibold
          text-ochre-800
          flex flex-col flex-shrink-0
        "
      >
        Stopped
        <SvgIcon terms="h-10 w-10 mx-auto mt-2" icon="svgMonetizationStatic" />
      </span>
    </div>
    <p v-if="streamFields.author" class="mt-2 sm:mt-6 text-md text-ochre-800">
      {{ streamFields.author }} will receive
      <span class="font-semibold">36 cents per hour</span> while you stream.
    </p>
    <p v-if="!streamFields.author" class="mt-2 sm:mt-6 text-md text-ochre-800">
      We will receive <span class="font-semibold">36 cents per hour</span> while
      you stream.
    </p>
    <p class="sm:mt-2 text-md text-ochre-800">Thank you.</p>
  </div>
</template>

<script lang="ts">
import { Component, Getter, Prop, Vue } from "nuxt-property-decorator"
import { IKeyable } from "@/interfaces"

@Component
export default class MonetizationCallStream extends Vue {
  @Getter("main/showOptionsCall") showOptionsCall
  @Prop(Object) readonly streamFields!: IKeyable
}
</script>

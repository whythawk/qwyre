<template>
  <div v-if="creator && Object.keys(creator).length">
    <TitleBar v-if="creator.creator" :title="creator.creator" />
    <TitleBar v-else title="Anonymous" />
    <p v-show="creator.description" class="text-sm py-2 font-bold">
      {{ creator.description }}
    </p>
    <div class="m-1 space-x-1">
      <span
        v-for="subject in creator.subject"
        :key="`subject-${subject.identifier}`"
        class="
          flex-shrink-0
          inline-block
          px-2
          py-0.5
          text-woad-800 text-xs
          font-medium
          bg-woad-100
          rounded-full
        "
        >{{ subject.term }}</span
      >
    </div>
  </div>
</template>

<script lang="ts">
import { Component, Prop, Vue } from "nuxt-property-decorator"
import { ICreatorSummary } from "@/interfaces"

@Component
export default class CreatorSummaryMetadata extends Vue {
  @Prop(Object) readonly creator!: ICreatorSummary
}
</script>

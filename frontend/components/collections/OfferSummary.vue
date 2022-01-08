<template>
  <div class="flex flex-wrap overflow-hidden">
    <div
      v-if="offer.work && offer.work.metadata"
      class="my-1 px-1 w-2/3 text-ochre-800"
    >
      <!-- Description -->
      <h1 class="text-4xl font-medium">{{ offer.work.metadata.title }}</h1>
      <p class="text-sm py-3">
        <span
          v-for="(creator, i) in offer.work.metadata.creator"
          :key="`creator-${i}`"
        >
          <span
            v-if="
              offer.work.metadata.creator.length > 1 &&
              offer.work.metadata.creator.length < i - 1 &&
              i > 0
            "
            >,
          </span>
          <span
            v-if="
              offer.work.metadata.creator.length > 1 &&
              offer.work.metadata.creator.length === i
            "
          >
            &amp;
          </span>
          <NuxtLink :to="`/creator/${creator.identifier}`" class="underline"
            ><span v-if="creator.creator">{{ creator.creator }}</span
            ><span v-else>Anonymous</span></NuxtLink
          >
        </span>
      </p>
      <p
        v-show="offer.work.metadata.description"
        class="text-sm py-2 font-bold"
      >
        {{ offer.work.metadata.description }}
      </p>
      <div class="border-b border-gray-200">
        <nav class="-mb-px flex space-x-8" aria-label="Tabs">
          <button
            v-for="tab in workTabs"
            :key="`worktab-button-${tab.id}`"
            :class="`${
              tab.id === selected
                ? 'border-woad-500 text-woad-600'
                : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'
            }
              whitespace-nowrap
              py-4
              px-1
              border-b-2
              font-medium
              text-sm
            `"
            @click.prevent="selected = tab.id"
          >
            {{ tab.name }}
          </button>
        </nav>
      </div>
      <CollectionsOfferSummaryMetadataTab
        v-if="selected === 'METADATA'"
        :offer="offer"
      />
      <CollectionsWorkSummaryFirst500Tab
        v-if="selected === 'FIRST500'"
        :work="offer.work"
      />
    </div>
    <div v-if="offer.work" class="my-1 px-1 w-1/3 flex flex-col">
      <!-- Cover -->
      <div
        class="
          relative
          mx-auto
          my-5
          w-60
          h-96
          filter
          drop-shadow-lg
          shadow
          transition
          ease-in
          duration-200
        "
      >
        <img
          :src="cover.data"
          class="
            object-cover object-center
            min-h-full min-w-full
            animate-fade-in
            rounded-lg
          "
        />
      </div>
      <div class="mt-8 flex mx-auto justify-center w-2/3">
        <div v-if="canMakeCreativeOffers">
          <CreatorExpressOfferInterestButton :contract-id="offer.identifier" />
        </div>
        <div v-else>
          <CreatorValidationRequirements />
        </div>
      </div>
    </div>
  </div>
</template>

<script lang="ts">
import { Component, Prop, Action, Getter, Vue } from "nuxt-property-decorator"
import { IContract, IParty, IDataSource } from "@/interfaces"
import { readableDate } from "@/utilities"

@Component
export default class CollectionsOfferSummary extends Vue {
  @Prop(Object) readonly offer!: IContract
  @Prop(Object) readonly cover!: IDataSource
  @Getter("main/canMakeCreativeOffers") canMakeCreativeOffers
  public selected: string = "METADATA"
  public workTabs: object[] = [
    {
      name: "Metadata",
      id: "METADATA",
    },
    {
      name: "First 500",
      id: "FIRST500",
    },
  ]

  public getReadableDate(dataString: string): string {
    return readableDate(dataString)
  }
}
</script>

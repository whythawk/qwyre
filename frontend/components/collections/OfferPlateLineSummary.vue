<template>
  <div class="aspect-h-12 aspect-w-10">
    <div
      class="col-span-1 flex flex-col text-center bg-white rounded-lg shadow"
    >
      <div class="w-full flex justify-between p-3 space-x-3">
        <div class="flex-1 line-clamp-5">
          <h3 class="mt-1 text-gray-900 text-sm font-semibold truncate">
            {{ offer.contract.work.metadata.title }}
          </h3>
          <p class="mt-1 text-gray-500 text-sm line-clamp-5">
            {{ offer.contract.work.metadata.description }}
          </p>
        </div>
        <SourcesCoverImage :src="offer.cover.data" />
      </div>
      <div class="m-1 space-x-1 line-clamp-2">
        <span
          v-for="subject in offer.contract.work.metadata.subject"
          :key="`subject-${offer.contract.work.identifier}-${subject.identifier}`"
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
      <div class="my-3 w-full">
        <h3 class="text-gray-900 text-sm font-semibold">Initial offer</h3>
        <div class="flex justify-between text-gray-500 text-xs my-1 mt-3 mx-10">
          <span>Revenue share</span>
          <span class="font-semibold capitalize"
            >{{ editor.proportion }} %</span
          >
        </div>
        <p class="text-gray-500 text-sm line-clamp-2">
          {{ offer.contract.description }}
        </p>
      </div>
      <div class="absolute inset-x-0 bottom-0">
        <div class="-mt-px flex">
          <div class="w-0 flex-1 flex">
            <NuxtLink
              :to="`/offers/${offer.contract.identifier}`"
              class="
                relative
                -mr-px
                flex-1
                inline-flex
                items-center
                justify-center
                py-4
                text-sm text-gray-700
                font-medium
                border border-transparent
                rounded-br-lg
                hover:text-gray-500
              "
            >
              <SvgIcon terms="w-5 h-5 text-gray-400" icon="svgPencilAlt" />
              <span class="ml-3">Review</span>
            </NuxtLink>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script lang="ts">
import { Component, Prop, Vue } from "nuxt-property-decorator"
import { IDataSource, IContract, IParty } from "@/interfaces"

@Component
export default class CollectionsOfferPlateLineSummary extends Vue {
  @Prop(Object) readonly offer!: {
    contract: IContract
    cover: IDataSource
  }

  public get editor(): IParty | undefined {
    const creatorIDs = this.offer.contract.work.metadata.creator.map(
      ({ identifier }) => identifier
    )
    return this.offer.contract.parties.find(
      (x) => !x.creator || !creatorIDs.includes(x.creator.identifier)
    )
  }
}
</script>

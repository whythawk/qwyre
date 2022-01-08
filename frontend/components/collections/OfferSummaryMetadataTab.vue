<template>
  <div v-if="offer.work && offer.work.metadata">
    <h3 class="my-2 font-semibold">Offer</h3>
    <div class="my-2">{{ offer.description }}</div>
    <!-- General metadata table -->
    <table class="table-fixed text-sm w-full">
      <thead>
        <tr>
          <th class="w-1/3"></th>
          <th class="w-2/3"></th>
        </tr>
      </thead>
      <tbody>
        <tr>
          <td class="font-semibold py-2">Editor's revenue share</td>
          <td class="text-right py-2">{{ editor.proportion }} %</td>
        </tr>
      </tbody>
    </table>
    <h3 class="my-2 font-semibold">Work pitch &amp; Metadata</h3>
    <div class="my-2" v-html="offer.work.metadata.long_description"></div>
    <!-- General metadata table -->
    <table class="table-fixed text-sm w-full">
      <thead>
        <tr>
          <th class="w-1/3"></th>
          <th class="w-2/3"></th>
        </tr>
      </thead>
      <tbody>
        <tr v-show="offer.work.metadata.language">
          <td class="font-semibold py-2">Language</td>
          <td class="text-right py-2">{{ offer.work.metadata.language }}</td>
        </tr>
        <tr
          v-show="
            offer.work.metadata.subject && offer.work.metadata.subject.length
          "
        >
          <td class="font-semibold py-2">Subject</td>
          <td class="text-right py-2 space-x-1 space-y-1">
            <span
              v-for="subject in offer.work.metadata.subject"
              :key="`subject-${offer.work.identifier}-${subject.identifier}`"
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
          </td>
        </tr>
        <tr v-if="offer.work.metadata.word_count">
          <td class="font-semibold py-2">Word count</td>
          <td class="text-right py-2">
            {{ offer.work.metadata.word_count.toLocaleString() }}
          </td>
        </tr>
      </tbody>
    </table>
  </div>
</template>

<script lang="ts">
import { Component, Prop, Vue } from "nuxt-property-decorator"
import { IContract, IParty } from "@/interfaces"
import { readableDate } from "@/utilities"

@Component
export default class CollectionsWorkSummaryMetadataTab extends Vue {
  @Prop(Object) readonly offer!: IContract

  public getReadableDate(dataString: string): string {
    return readableDate(dataString)
  }

public get editor(): IParty | undefined {
    const creatorIDs = this.offer.work.metadata.creator.map(
      ({ identifier }) => identifier
    )
    return this.offer.parties.find(
      (x) => !x.creator || !creatorIDs.includes(x.creator.identifier)
    )
  }
}
</script>

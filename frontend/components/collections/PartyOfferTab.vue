<template>
  <div v-if="contract && Object.keys(contract).length !== 0">
    <div class="my-2 italic text-right text-sm">
      {{ getReadableDate(contract.created) }}
    </div>
    <h3 class="my-8 font-semibold">Contract offer</h3>
    <div class="my-8">{{ contract.description }}</div>
    <div
      v-for="party in contract.parties"
      :key="`contract-party-${party.identifier}`"
      class="mt-4 mx-auto justify-center"
    >
      <div class="font-semibold text-sm">
        <span v-if="party.creator"
          >{{ getCreatorRole(party.creator.identifier) }}:
          <NuxtLink
            :to="`/creator/${party.creator.identifier}`"
            class="underline"
            ><span v-if="party.creator.creator">{{
              party.creator.creator
            }}</span
            ><span v-else>Anonymous</span></NuxtLink
          ></span
        >
        <span v-else>Editor (not assigned)</span>
      </div>
      <div class="mt-4 flex mx-auto justify-center">
        <table class="table-fixed text-sm w-4/5">
          <thead>
            <tr>
              <th class="w-1/2"></th>
              <th class="w-1/4"></th>
              <th class="w-1/4"></th>
            </tr>
          </thead>
          <tbody>
            <tr>
              <td class="font-semibold py-0">Proportion</td>
              <td class="text-right py-0 capitalize">
                {{ party.proportion }}%
              </td>
              <td class="text-right py-0 capitalize"></td>
            </tr>
            <tr>
              <td class="font-semibold py-0">Contract approved</td>
              <td class="text-right py-0 capitalize">
                <span v-if="party.isApproved">Approved</span>
                <span v-else>Not approved</span>
              </td>
              <td class="float-right py-2">
                <CreatorContractResponseButton
                  v-if="
                    editorAssigned &&
                    party.creator &&
                    party.creator.identifier === creatorProfile.identifier &&
                    !contract.isApproved &&
                    !contract.publicationApproved
                  "
                  :toggle-publication="false"
                  :contract-id="contract.identifier"
                  :party="party"
                />
              </td>
            </tr>
            <tr>
              <td class="font-semibold py-0">Publication approved</td>
              <td class="text-right py-0 capitalize">
                <span v-if="party.publicationApproved">Approved</span>
                <span v-else>Not approved</span>
              </td>
              <td class="float-right py-2">
                <CreatorContractResponseButton
                  v-if="
                    party.creator &&
                    party.creator.identifier === creatorProfile.identifier &&
                    party.isApproved &&
                    contract.isApproved &&
                    !contract.publicationApproved
                  "
                  :toggle-publication="true"
                  :contract-id="contract.identifier"
                  :party="party"
                />
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
    <div
      v-if="isWorkCreator(creatorProfile.identifier) && !contract.isApproved"
    >
      <p class="mt-8">
        Until you assign an editor, and all parties to this contract approve it,
        you may make changes to its terms, including withdrawing the offer, or
        revoking an offer to edit.
      </p>
      <div class="flex mx-auto justify-center mt-4">
        <NuxtLink
          :to="`/offers/${contract.work.identifier}/edit`"
          class="btn-woad-extended-sm flex items-center h-8"
        >
          <SvgIcon terms="w-5 h-4 inline-block mr-1 mb-1" icon="svgPencilAlt" />
          <span class="text-sm">Edit contract</span>
        </NuxtLink>
      </div>
      <h3 v-if="canUpdateContractEdit" class="my-8 font-semibold">
        Editor responses
      </h3>
      <table class="table-fixed text-sm w-4/5">
        <thead>
          <tr>
            <th class="w-3/4"></th>
            <th class="w-1/4"></th>
          </tr>
        </thead>
        <tbody>
          <tr
            v-for="offer in contract.offers"
            :key="`work-contract-offer-${offer.identifier}`"
          >
            <td class="font-semibold">
              <NuxtLink
                :to="`/creator/${offer.identifier}`"
                class="underline"
                >{{ offer.creator }}</NuxtLink
              >
            </td>
            <td class="float-right">
              <CreatorOfferChoiceButtons
                :contract-id="contract.identifier"
                :creator-id="offer.identifier"
              />
            </td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
</template>

<script lang="ts">
import { Component, Prop, Getter, Vue } from "nuxt-property-decorator"
import { IContract } from "@/interfaces"
import { readableDate } from "@/utilities"

@Component
export default class CollectionsPartyOfferTab extends Vue {
  @Prop(Object) readonly contract!: IContract
  @Prop(String) readonly workId!: string
  @Getter("conversions/workEditCreatorIdentifiers") workEditCreatorIdentifiers
  @Getter("main/creatorProfile") creatorProfile
  @Getter("conversions/canUpdateContractEdit") canUpdateContractEdit

  public get editorAssigned() {
    let assigned = true
    if (
      this.contract &&
      Object.keys(this.contract).length &&
      this.contract.parties.length
    ) {
      for (const party of this.contract.parties) {
        if (!party.creator) assigned = false
      }
    }
    return assigned
  }

  public isWorkCreator(identifier: string): boolean {
    return this.workEditCreatorIdentifiers.includes(identifier)
  }

  public getCreatorRole(identifier: string): string {
    let role = "Editor"
    if (this.isWorkCreator(identifier)) role = "Author"
    return role
  }

  public get creatorName() {
    if (this.creatorProfile.creator) return this.creatorProfile.creator
    else return "Anonymous"
  }

  public getReadableDate(dataString: string): string {
    return readableDate(dataString)
  }
}
</script>

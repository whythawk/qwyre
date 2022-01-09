<template>
  <div class="flex space-x-2">
    <button
      type="submit"
      :class="`btn-sinopia-sm ${!toggleState ? 'opacity-50' : ''}`"
      :disabled="!toggleState"
      @click.prevent="submit"
    >
      <SvgIcon terms="w-4 h-4 mx-auto my-auto" icon="svgX" />
    </button>
    <button
      type="submit"
      :class="`btn-malachite-sm ${toggleState ? 'opacity-50' : ''}`"
      :disabled="toggleState"
      @click.prevent="submit"
    >
      <SvgIcon terms="w-4 h-4 mx-auto my-auto" icon="svgCheck" />
    </button>
  </div>
</template>

<script lang="ts">
import { Component, Vue, Action, Prop } from "nuxt-property-decorator"
import { IParty } from "@/interfaces"

@Component
export default class CreatorContractResponseButton extends Vue {
  @Prop(Boolean) readonly togglePublication!: boolean
  @Prop(String) readonly contractId!: string
  @Prop(Object) readonly party!: IParty
  @Action("conversions/togglePartyContractAcceptance")
  togglePartyContractAcceptance

  @Action("conversions/togglePartyContractPublication")
  togglePartyContractPublication

  public get toggleState() {
    if (this.togglePublication) return this.party.publicationApproved
    else return this.party.isApproved
  }

  public async submit() {
    if (this.togglePublication)
      await this.togglePartyContractPublication(this.contractId)
    else await this.togglePartyContractAcceptance(this.contractId)
  }
}
</script>

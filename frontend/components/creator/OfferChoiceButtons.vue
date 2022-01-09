<template>
  <div class="flex space-x-2">
    <button type="submit" class="btn-sinopia-sm" @click.prevent="reject">
      <SvgIcon terms="w-4 h-4 mx-auto my-auto" icon="svgX" />
    </button>
    <button type="submit" class="btn-malachite-sm" @click.prevent="approve">
      <SvgIcon terms="w-4 h-4 mx-auto my-auto" icon="svgCheck" />
    </button>
  </div>
</template>

<script lang="ts">
import { Component, Vue, Action, Prop } from "nuxt-property-decorator"

@Component
export default class CreatorOfferChoiceButtons extends Vue {
  @Prop(String) readonly contractId!: string
  @Prop(String) readonly creatorId!: string
  @Action("conversions/rejectContractOffer") rejectContractOffer
  @Action("conversions/acceptContractOffer") acceptContractOffer

  public async approve() {
    const payload = {
      contractID: this.contractId,
      creatorID: this.creatorId,
    }
    await this.acceptContractOffer(payload)
  }

  public async reject() {
    const payload = {
      contractID: this.contractId,
      creatorID: this.creatorId,
    }
    await this.rejectContractOffer(payload)
  }
}
</script>

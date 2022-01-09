<template>
  <div>
    <TitleBar title="Offer" />
    <CollectionsOfferSummary :offer="offer" :cover="cover" />
  </div>
</template>

<script lang="ts">
import { Component, Action, Getter, Vue } from "nuxt-property-decorator"
import { api } from "@/api"
import { IContract, IParty, IDataSource } from "@/interfaces"

@Component({
  layout: "working",
  middleware: "refresh-authentication",
})
export default class ReviewOffer extends Vue {
  @Action("collections/getOffer") getOffer
  @Getter("collections/offer") offer
  public cover: IDataSource = {} as IDataSource

  public async getCoverImage(sourceID: string): Promise<IDataSource> {
    let coverImage = {} as IDataSource
    try {
      const response = await api.getCoverPublic(sourceID, "cover")
      if (response.data) {
        coverImage = response.data
      }
    } catch (error) {}
    return coverImage
  }

  public async created() {
    await this.getOffer(this.$route.params.id)
    this.cover = await this.getCoverImage(this.offer.work.identifier)
  }
}
</script>

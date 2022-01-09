<template>
  <div class="container min-h-screen mx-auto">
    <TitleBar title="Offers" />
    <CollectionsOffersFilteredGrid :offer-list="offerList" />
  </div>
</template>

<script lang="ts">
import { Component, Getter, Action, Vue } from "nuxt-property-decorator"
import { api } from "@/api"
import { IContract, IDataSource } from "@/interfaces"

@Component({
  layout: "working",
  middleware: "refresh-authentication",
})
export default class Offers extends Vue {
  @Action("collections/getOffers") getOffers
  @Getter("collections/offers") offers
  public offerList: { contract: IContract; cover: IDataSource }[] = []

  public async getCoverImage(sourceID: string): Promise<IDataSource> {
    let coverImage = {} as IDataSource
    try {
      const response = await api.getCoverPublic(sourceID, "thumbnail")
      if (response.data) {
        coverImage = response.data
      }
    } catch (error) {}
    return coverImage
  }

  public async created() {
    await this.getOffers()
    for (const contract of this.offers) {
      const cover = await this.getCoverImage(contract.work.identifier)
      this.offerList.push({
        contract,
        cover,
      })
    }
  }
}
</script>

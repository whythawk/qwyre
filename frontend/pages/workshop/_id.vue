<template>
  <div>
    <TitleBar title="Review" />
    <CollectionsWorkSummary
      v-if="showSummary"
      :work="workEdit"
      :cover="cover"
      :contract="contractEdit"
    />
  </div>
</template>

<script lang="ts">
import { Component, Getter, Action, Vue, Watch } from "nuxt-property-decorator"
import { api } from "@/api"
import { IDataSource } from "@/interfaces"

@Component({
  layout: "working",
  middleware: "authenticated",
})
export default class WorkshopEdit extends Vue {
  @Action("conversions/getWorkToEdit") getWorkToEdit
  @Action("conversions/getContractToEdit") getContractToEdit
  @Getter("conversions/workEdit") workEdit
  @Getter("conversions/contractEdit") contractEdit
  @Getter("main/changeWatcher") changeWatcher
  public cover: IDataSource = {} as IDataSource
  public showSummary: boolean = false

  public async getCoverImage(sourceID: string): Promise<IDataSource> {
    let coverImage = {} as IDataSource
    try {
      const response = await api.getCoverAuthenticated(
        (this as any).$cookies.get("token"),
        sourceID,
        "cover"
      )
      if (response.data) {
        coverImage = response.data
      }
    } catch (error) {}
    return coverImage
  }

  @Watch("changeWatcher")
  public async initialise() {
    await this.getWorkToEdit(this.$route.params.id)
    if (
      this.workEdit &&
      Object.keys(this.workEdit).length &&
      this.workEdit.identifier
    ) {
      this.cover = await this.getCoverImage(this.workEdit.identifier)
      await this.getContractToEdit(this.workEdit.identifier)
      this.showSummary = true
    }
  }

  public async created() {
    await this.initialise()
  }
}
</script>

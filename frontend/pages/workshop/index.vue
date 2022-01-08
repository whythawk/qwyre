<template>
  <div class="container min-h-screen mx-auto">
    <TitleBar title="Workshop" />
    <div class="max-w-screen-md mx-auto">
      <div class="flex space-x-4 w-full justify-center">
        <NuxtLink
          to="/convert/description"
          class="btn-woad-extended-sm flex items-center h-8"
        >
          <SvgIcon
            terms="w-5 h-4 inline-block mr-1 mb-1"
            icon="svgDocumentText"
          />
          <span class="text-sm">Convert .docx</span>
        </NuxtLink>
        <CollectionsImportWork />
        <CollectionsImportLink />
        <NuxtLink
          to="/offers"
          class="btn-ochre-extended-sm flex items-center h-8"
        >
          <SvgIcon terms="w-5 h-4 inline-block mr-1 mb-1" icon="svgSearchDoc" />
          <span class="text-sm">Review offers</span>
        </NuxtLink>
      </div>
    </div>
    <div class="border-b border-gray-200">
      <nav class="-mb-px flex space-x-8" aria-label="Tabs">
        <button
          v-for="tab in tabs"
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
    <div v-if="selected === 'WORKS'">
      <CollectionsWorkshopFilteredGrid
        v-if="workList.length"
        :work-list="workList"
      />
      <div
        v-if="!workList.length"
        class="max-w-7xl mx-auto overflow-hidden sm:px-6 lg:px-8 pt-8"
      >
        <p class="text-sm">
          You haven't created any works. Start by importing an
          <span class="italic">.epub ebook</span> and prepare your work for
          publication.
        </p>
        <p class="text-sm">
          If you'd like to express your creativity in other ways, support
          authors as an editor, and earn a share of their earnings for your
          work,
          <NuxtLink to="/offers" class="underline">
            <span class="text-sm">review current offers</span> </NuxtLink
          >.
        </p>
        <p class="text-sm mt-1">
          To learn more,
          <NuxtLink to="/get-streaming" class="underline">
            <span class="ml-1">read our guide to streaming</span>.
          </NuxtLink>
        </p>
      </div>
    </div>
    <div v-if="selected === 'CONTRIBUTIONS'">
      <CollectionsWorkshopFilteredGrid
        v-if="contributorList.length"
        :work-list="contributorList"
      />
      <div
        v-if="!contributorList.length"
        class="max-w-7xl mx-auto overflow-hidden sm:px-6 lg:px-8 pt-8"
      >
        <p class="text-sm">
          You haven't contributed to any works. If you'd like to support authors
          as an editor, and earn a share of their earnings for your work,
          <NuxtLink to="/offers" class="underline">
            <span class="text-sm">review current offers</span> </NuxtLink
          >.
        </p>
        <p class="text-sm mt-1">
          To learn more,
          <NuxtLink to="/get-streaming" class="underline">
            <span class="ml-1">read our guide to streaming</span>.
          </NuxtLink>
        </p>
      </div>
    </div>
    <CollectionsConversionFilteredGrid v-if="selected === 'CONVERSIONS'" />
  </div>
</template>

<script lang="ts">
import { Component, Getter, Action, Watch, Vue } from "nuxt-property-decorator"
import { api, idb } from "@/api"
import { IWorkLineSummary, IDataSource } from "@/interfaces"

@Component({
  layout: "working",
  middleware: "refresh-authentication",
})
export default class Workshop extends Vue {
  @Action("conversions/getWorkSummaries") getWorkSummaries
  @Action("collections/getPartyContributions") getPartyContributions
  @Getter("conversions/workSummaries") workSummaries
  @Getter("collections/partyContributions") partyContributions
  @Getter("main/token") token
  @Getter("main/changeWatcher") changeWatcher
  public selected: string = "CONVERSIONS"
  public tabs: object[] = [
    {
      name: "Conversions",
      id: "CONVERSIONS",
    },
    {
      name: "Works",
      id: "WORKS",
    },
    {
      name: "Contributions",
      id: "CONTRIBUTIONS",
    },
    // {
    //   name: "Statistics",
    //   id: "STATISTICS",
    // },
  ]

  public workList: { work: IWorkLineSummary; cover: IDataSource }[] = []
  public contributorList: { work: IWorkLineSummary; cover: IDataSource }[] = []

  public async getCoverImage(sourceID: string): Promise<IDataSource> {
    let coverImage = {} as IDataSource
    try {
      const response = await api.getCoverAuthenticated(
        this.token,
        sourceID,
        "thumbnail"
      )
      if (response.data) {
        coverImage = response.data
      }
    } catch (error) {}
    return coverImage
  }

  @Watch("changeWatcher")
  public async initialise() {
    await this.getWorkSummaries()
    if (this.workSummaries && Object.keys(this.workSummaries).length !== 0)
      for (let work of this.workSummaries) {
        work = JSON.parse(JSON.stringify(work))
        const cover = await this.getCoverImage(work.identifier)
        if (work.metadata.uid) {
          const hasKey = await idb.hasKey("epub", work.metadata.uid)
          if (!hasKey) work.metadata.uid = ""
        }
        this.workList.push({
          work,
          cover,
        })
      }
    // These two sets have nothing in common
    await this.getPartyContributions()
    if (
      this.partyContributions &&
      Object.keys(this.partyContributions).length !== 0
    )
      for (let contract of this.partyContributions) {
        contract = JSON.parse(JSON.stringify(contract))
        const cover = await this.getCoverImage(contract.work.identifier)
        if (contract.work.metadata.uid) {
          const hasKey = await idb.hasKey("epub", contract.work.metadata.uid)
          if (!hasKey) contract.work.metadata.uid = ""
        }
        this.contributorList.push({
          work: contract.work,
          cover,
        })
      }
  }

  public async created() {
    await this.initialise()
  }
}
</script>

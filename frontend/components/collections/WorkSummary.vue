<template>
  <div class="flex flex-wrap overflow-hidden">
    <div v-if="work && work.metadata" class="my-1 px-1 w-2/3 text-ochre-800">
      <!-- Description -->
      <h1 class="text-4xl font-medium">{{ work.metadata.title }}</h1>
      <p class="text-sm py-3">
        <span
          v-for="(creator, i) in work.metadata.creator"
          :key="`creator-${i}`"
        >
          <span
            v-if="
              work.metadata.creator.length > 1 &&
              work.metadata.creator.length < i - 1 &&
              i > 0
            "
            >,
          </span>
          <span
            v-if="
              work.metadata.creator.length > 1 &&
              work.metadata.creator.length === i
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
      <div
        v-show="work.dedication && work.dedication.length"
        class="text-sm py-3 font-light text-center italic"
      >
        <p
          v-for="(dedict, i) in work.dedication"
          :key="`dedication-${i}`"
          class="py-1"
        >
          {{ dedict }}
        </p>
      </div>
      <p v-show="work.metadata.description" class="text-sm py-2 font-bold">
        {{ work.metadata.description }}
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
      <CollectionsWorkSummaryMetadataTab
        v-if="selected === 'METADATA'"
        :work="work"
      />
      <CollectionsWorkSummarySpineTab
        v-if="selected === 'CONTENTS'"
        :work="work"
      />
      <CollectionsWorkSummaryFirst500Tab
        v-if="selected === 'FIRST500'"
        :work="work"
      />
      <CollectionsPartyOfferTab
        v-if="selected === 'CONTRACT'"
        :contract="contract"
        :work-id="work.metadata.identifier"
      />
      <ConversionImportEpub
        v-if="selected === 'UPDATE'"
        :work-id="work.identifier"
      />
    </div>
    <div v-if="work" class="my-1 px-1 w-1/3 flex flex-col">
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
      <div class="mt-8 flex mx-auto justify-center">
        <table class="table-fixed text-sm w-2/3">
          <thead>
            <tr>
              <th class="w-1/3"></th>
              <th class="w-2/3"></th>
            </tr>
          </thead>
          <tbody>
            <tr>
              <td class="font-semibold py-0">Work status</td>
              <td class="text-right py-0 capitalize">
                <span
                  :class="`
                    inline-flex
                    items-center
                    px-3
                    py-0.5
                    rounded-full
                    text-sm
                    font-medium
                    ${
                      ['withdrawn', 'suspended'].includes(work.state)
                        ? 'bg-sinopia-200'
                        : 'bg-woad-100'
                    }
                    text-gray-800
                  `"
                >
                  {{ work.state }}
                </span>
              </td>
            </tr>
            <tr>
              <th class="text-center py-8 font-normal" colspan="2">
                <div
                  v-if="!contract || Object.keys(contract).length === 0"
                  class="flex mx-auto justify-center"
                >
                  <NuxtLink
                    :to="`/offers/${work.metadata.identifier}/edit`"
                    class="btn-sinopia-extended-sm flex items-center h-8"
                  >
                    <SvgIcon
                      terms="w-5 h-4 inline-block mr-1 mb-1"
                      icon="svgBookOpen"
                    />
                    <span class="text-sm">Prepare contract</span>
                  </NuxtLink>
                </div>
                <div
                  v-if="
                    isWorkCreator &&
                    contract &&
                    Object.keys(contract).length !== 0 &&
                    ['submitted', 'updated'].includes(work.state)
                  "
                  class="flex mx-auto justify-center"
                >
                  <button
                    class="btn-woad-extended-sm flex items-center h-8"
                    @click.prevent="publishContract"
                  >
                    <SvgIcon
                      terms="w-5 h-4 inline-block mr-1 mb-1"
                      icon="svgBookmark"
                    />
                    <span class="text-sm">Publish contract</span>
                  </button>
                </div>
                <div
                  v-if="
                    isWorkCreator &&
                    contract &&
                    Object.keys(contract).length !== 0 &&
                    work.state === 'offered'
                  "
                  class="flex mx-auto justify-center"
                >
                  <button
                    class="btn-sinopia-extended-sm flex items-center h-8"
                    @click.prevent="publishContract"
                  >
                    <SvgIcon
                      terms="w-5 h-4 inline-block mr-1 mb-1"
                      icon="svgBookmark"
                    />
                    <span class="text-sm">Unpublish contract</span>
                  </button>
                </div>
                <div
                  v-if="
                    isWorkCreator &&
                    contract &&
                    contract.publicationApproved &&
                    work.state !== 'published'
                  "
                  class="flex mx-auto justify-center"
                >
                  <button
                    class="btn-malachite-extended-sm flex items-center h-8"
                    @click.prevent="publishWorkBook"
                  >
                    <SvgIcon
                      terms="w-5 h-4 inline-block mr-1 mb-1"
                      icon="svgBookOpen"
                    />
                    <span class="text-sm">Publish work</span>
                  </button>
                </div>
                <div
                  v-if="
                    isWorkCreator &&
                    contract &&
                    contract.publicationApproved &&
                    work.state === 'published'
                  "
                  class="flex mx-auto justify-center"
                >
                  <button
                    class="btn-sinopia-extended-sm flex items-center h-8"
                    @click.prevent="publishWorkBook"
                  >
                    <SvgIcon
                      terms="w-5 h-4 inline-block mr-1 mb-1"
                      icon="svgBookOpen"
                    />
                    <span class="text-sm">Unpublish work</span>
                  </button>
                </div>
              </th>
            </tr>
            <tr>
              <td class="font-semibold py-0">This version</td>
              <td class="text-right py-0">
                {{ getReadableDate(work.created) }}
              </td>
            </tr>
            <tr>
              <td class="font-semibold py-0">Max price</td>
              <td class="text-right py-0">
                {{ work.price }}
              </td>
            </tr>
            <tr>
              <td class="font-semibold py-0">Start page</td>
              <td class="text-right py-0">
                {{ work.start_page }}
              </td>
            </tr>
            <tr v-if="contract">
              <td class="font-semibold py-0">Contract</td>
              <td class="text-right py-0 capitalize">
                <span v-if="contract.isApproved">Approved</span>
                <span v-else>Not approved</span>
              </td>
            </tr>
            <tr v-if="contract">
              <td class="font-semibold py-0">Publication</td>
              <td class="text-right py-0 capitalize">
                <span v-if="contract.publicationApproved">Approved</span>
                <span v-else>Not approved</span>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
      <div v-if="isWorkCreator" class="mt-8 flex mx-auto justify-center">
        <CollectionsDeleteWork
          :work-key="work.identifier"
          :status="work.state"
        />
      </div>
    </div>
  </div>
</template>

<script lang="ts">
import {
  Component,
  Prop,
  Action,
  Getter,
  Vue,
  Watch,
} from "nuxt-property-decorator"
import { IKeyable, IWorkSummary, IDataSource, IContract } from "@/interfaces"
import { readableDate } from "@/utilities"

@Component
export default class CollectionsWorkSummary extends Vue {
  @Prop(Object) readonly work!: IWorkSummary
  @Prop(Object) readonly cover!: IDataSource
  @Prop(Object) readonly contract!: IContract
  @Action("conversions/publishWorkContract") publishWorkContract
  @Action("conversions/publishWork") publishWork
  @Getter("conversions/workEditCreatorIdentifiers") workEditCreatorIdentifiers
  @Getter("main/creatorProfile") creatorProfile
  public selected: string = "METADATA"
  public workTabs: IKeyable[] = [
    {
      name: "Metadata",
      id: "METADATA",
    },
    {
      name: "Contents",
      id: "CONTENTS",
    },
    {
      name: "First 500",
      id: "FIRST500",
    },
  ]

  public get isWorkCreator() {
    return this.workEditCreatorIdentifiers.includes(
      this.creatorProfile.identifier
    )
  }

  public getReadableDate(dataString: string): string {
    return readableDate(dataString)
  }

  public async publishContract() {
    if (this.contract && Object.keys(this.contract).length !== 0)
      await this.publishWorkContract(this.work.identifier)
  }

  public async publishWorkBook() {
    if (this.contract && Object.keys(this.contract).length !== 0)
      await this.publishWork(this.work.identifier)
  }

  @Watch("contract")
  public initialise() {
    if (
      this.contract &&
      Object.keys(this.contract).length !== 0 &&
      !this.workTabs.some((tab) => tab.id === "CONTRACT")
    )
      this.workTabs.push({
        name: "Publication Contract",
        id: "CONTRACT",
      })
    if (this.isWorkCreator && !this.workTabs.some((tab) => tab.id === "UPDATE"))
      this.workTabs.push({
        name: "Update Work",
        id: "UPDATE",
      })
  }

  public created() {
    this.initialise()
  }
}
</script>

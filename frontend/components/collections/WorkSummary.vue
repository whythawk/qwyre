<template>
  <div>
    <div
      class="card card-compact rounded-md bg-base-100 shadow-sm lg:mx-10 mb-4 -mt-4"
    >
      <div class="card-body flex">
        <div class="flex items-start">
          <div class="flex-shrink-0">
            <SvgIcon
              terms="h-6 w-6 text-malachite-400"
              icon="svgInformationCircle"
            />
          </div>
          <div class="ml-3 w-0 flex-1 pt-0.5">
            <p class="text-sm font-medium text-gray-900">
              Successfully {{ work.state }}.
            </p>
            <p
              v-if="tasksForState[work.state]"
              class="mt-1 text-sm text-gray-500"
            >
              {{ tasksForState[work.state] }}
            </p>
            <p v-else class="mt-1 text-sm text-gray-500">
              <span v-if="Object.entries(contract).length === 0">{{
                tasksForState.submitted
              }}</span>
              <span v-else>
                <span v-if="contract.isApproved">{{
                  tasksForState.contracted
                }}</span>
                <span v-else>{{ tasksForState.offered }}</span>
              </span>
            </p>
          </div>
          <div class="ml-4 flex-shrink-0 flex">
            <ConversionUpdateWork
              v-if="canUpdateWork"
              :work-id="work.identifier"
              :work-uid="work.metadata.uid"
            />
            <span
              v-else
              :class="`inline-flex items-center px-3 py-0.5 rounded-full text-sm font-medium capitalize
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
          </div>
        </div>
      </div>
    </div>
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
              } ${tab.id === 'CONTRACT' ? 'font-bold' : 'font-medium'}
              whitespace-nowrap
              py-4
              px-1
              border-b-2
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
        <ConversionUpdateWork
          v-if="selected === 'UPDATE'"
          :work-id="work.identifier"
          :work-uid="work.metadata.uid"
        />
      </div>
      <div v-if="work" class="my-1 px-1 w-1/3 flex flex-col">
        <!-- Cover -->
        <div
          class="relative mx-auto my-5 w-60 h-96 filter rounded-lg drop-shadow-lg shadow transition ease-in duration-200"
        >
          <img
            :src="cover.data"
            class="object-cover object-center min-h-full min-w-full animate-fade-in rounded-lg"
          />
        </div>
        <div class="mb-8 flex mx-auto justify-center">
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
        </div>
        <CollectionsSubmissionSteps
          :work-state="work.state"
          :contract-state="contract.isApproved"
        />
        <div v-if="isWorkCreator" class="mt-8 flex mx-auto justify-center">
          <CollectionsDeleteWork
            :work-key="work.identifier"
            :status="work.state"
          />
        </div>
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
  public canUpdateWork: boolean = false
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

  public tasksForState: IKeyable = {
    submitted:
      "You must prepare a contract and offer your work for editing before you can publish.",
    offered:
      "Review offers, or engage with potential editors. Agree a contract.",
    contracted:
      "Collaborate with your editor to polish your work for publication.",
    edited: "Publish your work.",
    published: "Are you ready to write something new?",
    withdrawn: "This work has been withdrawn pending moderator review.",
    reviewed:
      "This work has been reviewed and does not contravene our terms of publication. It has been republished.",
    suspended:
      "This work contravenes our terms of publication and has been suspended.",
  }

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
    if (
      this.isWorkCreator &&
      ["submitted", "updated", "offered", "contracted"].includes(
        this.work.state
      )
    )
      this.canUpdateWork = true
  }

  public created() {
    this.initialise()
  }
}
</script>

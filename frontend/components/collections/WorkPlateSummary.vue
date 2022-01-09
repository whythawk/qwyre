<template>
  <div class="group relative p-4 sm:p-6">
    <div v-if="showNew">
      <div v-if="collection === 'work'">
        <div class="aspect-h-16 aspect-w-10">
          <CollectionsImportLibrary />
        </div>
        <div class="pt-10 pb-4 text-center">
          <h3 class="text-lg font-semibold text-ochre-800">
            Import to your collection
          </h3>
          <p class="text-md py-1 font-semibold text-ochre-600">
            Start reading a new book
          </p>
        </div>
      </div>
      <div v-else>
        <div class="aspect-h-16 aspect-w-10">
          <CollectionsCreate :collection="collection" />
        </div>
        <div class="pt-10 pb-4 text-center">
          <h3 class="text-lg font-semibold text-ochre-800">
            Add to your collection
          </h3>
          <p class="text-md py-1 font-semibold text-ochre-600">
            Start a new {{ collection }}
          </p>
        </div>
      </div>
    </div>
    <div v-else>
      <CollectionsCover
        :collection="collection"
        :collection-key="collectionKey"
      />
      <div class="pt-10 pb-4 text-center">
        <h3 class="text-lg font-semibold text-ochre-800">
          {{ collectionFields.title }}
        </h3>
        <p class="text-md py-1 font-semibold text-ochre-600">
          {{ collectionFields.creator }}
        </p>
        <p
          v-show="collectionFields.subjects && collectionFields.subjects.length"
          class="text-sm py-1 font-medium italic text-malachite-600"
        >
          {{ collectionFields.subjects }}
        </p>
        <div class="grid grid-cols-4 content-start">
          <CollectionsDelete
            v-show="showDelete"
            :collection="collection"
            :collection-key="collectionKey"
          />
          <p
            v-show="collectionFields.date_created"
            class="
              col-span-3
              text-right text-sm
              py-1
              font-medium
              text-ochre-500
            "
          >
            {{ collectionFields.date_created }}
          </p>
        </div>
      </div>
    </div>
  </div>
</template>

<script lang="ts">
import { Component, Prop, Vue } from "nuxt-property-decorator"
import { idb } from "@/api"
import {
  IOpinion,
  IAnthology,
  IConversion,
  ISeries,
  IWork,
  IStream,
  ICreatorSummary,
  ISubject,
} from "@/interfaces"

@Component
export default class CollectionsWorkPlateSummary extends Vue {
  @Prop(String) readonly collection!: string
  @Prop(String) readonly collectionKey!: string
  @Prop(Boolean) readonly showDelete!: boolean
  @Prop(Boolean) readonly showNew!: boolean

  public collectionFields: {
    [key: string]: string | string[] | IOpinion | null | undefined
  } = {}

  public parseISOString(isodate: string): string {
    // https://stackoverflow.com/a/27013409/295606
    const b = isodate.split(/\D+/).map((x) => +x)
    const d = new Date(Date.UTC(b[0], --b[1], b[2]))
    return `${d.getUTCDate()} ${d.toLocaleString("default", {
      month: "short",
    })} ${d.getUTCFullYear()}`
  }

  public parseStringList(stringList: string[]): string {
    switch (stringList.length) {
      case 0:
        return ""
      case 1:
        return stringList[0]
      case 2:
        return stringList.join(" & ")
      default:
        return `${stringList.slice(0, -1).join(", ")} & ${
          stringList.slice(-1)[0]
        }`
    }
  }

  public checkBy(name: string | null): string {
    if (!name) return "Anonymous"
    return name
  }

  public async getCollectionFields() {
    if (this.showNew) return {}
    const c = (await idb.getPayload(this.collection, this.collectionKey)) as
      | IConversion
      | IWork
      | IStream
      | IAnthology
      | ISeries
    let title = ""
    let creator: string[] | string | ICreatorSummary[] = []
    let description: string | undefined
    /* eslint-disable camelcase */
    let date_created: string | undefined
    let subjects: string[] | string | ISubject[] | undefined
    let opinion: IOpinion | undefined
    if (Object.prototype.hasOwnProperty.call(c, "metadata")) {
      title = (c as IConversion | IWork | IStream).metadata.title
      creator = (c as IConversion | IWork | IStream).metadata.creator
      if (typeof creator === "string") {
        creator = [creator]
      }
      if (this.collection === "stream") {
        const authors: string[] = []
        for (const a of creator) {
          authors.push(this.checkBy((a as ICreatorSummary).creator))
        }
        creator = authors
      }
      description = (c as IConversion | IWork | IStream).metadata.description
      subjects = (c as IConversion | IWork | IStream).metadata.subject
      if (typeof subjects === "string") {
        subjects = [subjects]
      }
      if (subjects && this.collection === "stream") {
        const terms: string[] = []
        for (const t of subjects) {
          terms.push((t as ISubject).term)
        }
        subjects = terms
      }
      if (
        Object.prototype.hasOwnProperty.call(
          (c as IConversion | IWork).metadata,
          "date"
        )
      )
        date_created = (c as any).metadata.date
      else if (
        Object.prototype.hasOwnProperty.call(
          (c as IConversion | IWork).metadata,
          "isodate"
        )
      )
        date_created = (c as IWork | IConversion).metadata.isodate
      else if (
        Object.prototype.hasOwnProperty.call(
          (c as IConversion | IWork).metadata,
          "pubdate"
        )
      )
        date_created = (c as any).metadata.pubdate
    } else {
      title = (c as IAnthology | ISeries).name as string
      description = (c as IAnthology | ISeries).description
      if (Object.prototype.hasOwnProperty.call(c, "date_created"))
        date_created = (c as IAnthology | ISeries).date_created.toISOString()
    }
    if (Object.prototype.hasOwnProperty.call(c, "opinion"))
      opinion = (c as IAnthology | ISeries | IWork).opinion
    if (date_created) date_created = this.parseISOString(date_created as string)
    if (creator) creator = this.parseStringList(creator as string[])
    if (subjects) subjects = this.parseStringList(subjects as string[])
    return {
      title,
      creator,
      description,
      date_created,
      subjects,
      opinion,
      key: this.collectionKey,
    }
  }

  async created() {
    this.collectionFields = await this.getCollectionFields()
  }
}
</script>

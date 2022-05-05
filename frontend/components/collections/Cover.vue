<template>
  <div class="cursor-pointer" @click.prevent="submit">
    <div v-if="!collectionFields.src" class="aspect-h-16 aspect-w-10">
      <div class="grid grid-rows-6 gap-1 bg-ochre-100 rounded-lg max-h-full">
        <div class="row-start-2 row-span-2">
          <SvgIcon
            terms="h-8 w-8 sm:h-10 sm:w-10 md:h-20 md:w-16 mx-auto my-auto block text-ochre-600"
            icon="svgBookmark"
          />
        </div>
        <div class="row-span-2">
          <div
            class="text-center text-xs sm:text-base md:text-xl text-ochre-800"
          >
            {{ collectionFields.title }}
          </div>
        </div>
      </div>
    </div>
    <div v-else>
      <div class="aspect-h-16 aspect-w-10">
        <img
          :src="collectionFields.src"
          :class="`rounded-lg max-h-full ${
            collection === 'conversion' ? 'filter sepia' : ''
          }`"
        />
      </div>
    </div>
  </div>
</template>

<script lang="ts">
import { Component, Mutation, Prop, Vue } from "nuxt-property-decorator"
import { idb } from "@/api"
import {
  IAnthology,
  IConversion,
  ISeries,
  IWork,
  IStream,
  IKeyable,
} from "@/interfaces"

@Component
export default class CollectionCover extends Vue {
  @Prop(String) readonly collection!: string
  @Prop(String) readonly collectionKey!: string
  @Mutation("collections/setCollection") setCollection
  @Mutation("conversions/setConversionKey") setConversionKey

  public routerPaths: { [key: string]: string } = {
    stream: "/stream/",
    work: "/read",
    conversion: "/write/describe",
    anthology: "/anthology",
    series: "/series",
  }

  public collectionFields: IKeyable = {} as IKeyable

  public getCoverImage() {
    // IndexedDB takes a really long time to update
    const coverImage = new Promise<string | IKeyable | null>((resolve) => {
      setTimeout(() => {
        resolve(
          idb.getPayload("cover", this.collectionKey) as unknown as
            | string
            | IKeyable
            | null
        )
      }, 100)
    })
    return coverImage
  }

  public async getCollectionFields() {
    const c = (await idb.getPayload(this.collection, this.collectionKey)) as
      | IConversion
      | IWork
      | IStream
      | IAnthology
      | ISeries
    let coverImage: string | IKeyable | null = await this.getCoverImage()
    if (coverImage && this.collection === "stream")
      coverImage = (coverImage as unknown as IKeyable).data
    let title = ""
    if (Object.prototype.hasOwnProperty.call(c, "metadata"))
      title = (c as IConversion | IWork).metadata.title
    else title = (c as IAnthology | ISeries).name as string
    return {
      title,
      src: coverImage || null,
      key: this.collectionKey,
    }
  }

  async submit() {
    if (this.collectionKey) {
      await this.setCollection({
        collection: this.collection,
        key: this.collectionKey,
      })
    }
    if (["work", "stream"].includes(this.collection))
      await this.setCollection({
        collection: "library",
        key: this.collectionKey,
      })
    if (this.collection === "conversion")
      this.setConversionKey(this.collectionKey)
    const newRoute: string =
      this.collection === "stream"
        ? `${this.routerPaths[this.collection]}${this.collectionKey}`
        : this.routerPaths[this.collection]
    this.$router.push(newRoute)
  }

  async created() {
    this.collectionFields = await this.getCollectionFields()
  }
}
</script>

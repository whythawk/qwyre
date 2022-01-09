<template>
  <div class="max-w-xl mx-auto bg-ochre-900 opacity-90 rounded-lg shadow-xl">
    <div class="container relative mx-auto max-w-xl">
      <div class="p-1">
        <!--Lead Card-->
        <div
          class="bg-ochre-50 rounded bg-opacity-90 overflow-hidden shadow-lg"
        >
          <!--- WEB MONETIZATION --->
          <MonetizationCallSign
            v-if="!coilSub"
            :uri="coilRequestURI"
            :stream-fields="streamFields"
          />
          <MonetizationCallStream
            v-if="coilSub"
            :stream-fields="streamFields"
          />
        </div>
      </div>
    </div>
  </div>
</template>

<script lang="ts">
import { Component, Getter, Action, Watch, Vue } from "nuxt-property-decorator"
import { IStream, IKeyable, ICreatorSummary } from "@/interfaces"
import { idb, coil } from "@/api"

@Component
export default class MonetizationStreamWork extends Vue {
  @Getter("main/showOptionsCall") showOptionsCall
  @Getter("monetization/coilState") coilState
  @Getter("monetization/coilSub") coilSub
  @Action("monetization/storeCoilResourceState") storeCoilResourceState
  public coilRequestURI: string = ""
  public stream: IStream = {} as IStream
  public streamFields: IKeyable = {} as IKeyable

  public checkBy(name: string | null): string {
    if (!name) return "Anonymous"
    return name
  }

  public makeAuthorString(authors: ICreatorSummary[]): string {
    if (authors.length === 1) {
      return this.checkBy(authors[0].creator)
    }
    if (authors.length >= 2) {
      const authorList: string[] = []
      for (const author of authors.slice(0, -1))
        authorList.push(this.checkBy(author.creator))
      return `${authorList.join(", ")} &amp; ${this.checkBy(
        authors.slice(-1)[0].creator
      )}`
    }
    return "Anonymous"
  }

  public async getStreamingWork() {
    try {
      this.stream = (await idb.getPayload(
        "stream",
        this.$route.params.id
      )) as IStream
    } catch (e) {}
  }

  public getCoverImage() {
    // IndexedDB takes a really long time to update
    const coverImage = new Promise<string | IKeyable | null>((resolve) => {
      setTimeout(() => {
        resolve(
          idb.getPayload("cover", this.$route.params.id) as unknown as
            | string
            | IKeyable
            | null
        )
      }, 100)
    })
    return coverImage
  }

  public async getStreamFields() {
    await this.getStreamingWork()
    let coverImage: string | IKeyable | null = await this.getCoverImage()
    coverImage = (coverImage as unknown as IKeyable).data
    let title = ""
    let author = ""
    if (Object.prototype.hasOwnProperty.call(this.stream, "metadata")) {
      title = this.stream.metadata.title
      author = this.makeAuthorString(
        this.stream.metadata.creator as ICreatorSummary[]
      )
    }
    this.streamFields = {
      title,
      author,
      cover: coverImage || null,
    }
  }

  @Watch("showOptionsCall")
  async initialise(): Promise<void> {
    if (!this.coilSub && this.showOptionsCall) {
      await this.storeCoilResourceState({ coilRoute: this.$route.path })
      this.coilRequestURI = coil.getUserResource(this.coilState)
    }
    if (this.showOptionsCall) await this.getStreamFields()
  }
}
</script>

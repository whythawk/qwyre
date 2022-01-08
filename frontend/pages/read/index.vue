<template>
  <div
    :class="`mx-auto ${pageTheme === 'light' ? 'bg-ochre-10' : 'bg-ochre-900'}
    `"
  >
    <div class="h-screen flex justify-center">
      <article>
        <OverlaysReaderOptions :completion="completion" />
        <!-- Invisible overlay for reader input -->
        <div
          ref="reader-input"
          class="z-30 fixed inset-0 overflow-hidden outline-none"
          aria-hidden="true"
          tabindex="0"
        >
          <div class="absolute inset-0 bg-opacity-0" aria-hidden="true"></div>
        </div>
        <client-only placeholder="Loading...">
          <div
            ref="reader-view"
            class="z-1 relative h-screen w-screen sm:max-w-xl sm:mx-auto"
          ></div>
        </client-only>
      </article>
    </div>
  </div>
</template>

<script lang="ts">
import {
  Component,
  Ref,
  Vue,
  Getter,
  Mutation,
  Action,
  Watch,
} from "nuxt-property-decorator"
import { Book, Rendition } from "epubjs"
import {
  clickXListener,
  keyListener,
  swipeListener,
  wheelListener,
} from "@/mixins/readerListeners"
import { IWork } from "@/interfaces"
import { idb } from "@/api"
import { dark, light, serif, sanserif } from "@/assets/css/themes"
import { generateUUID } from "@/utilities"
// import Section from "epubjs/types/section"
// import { readerIframeView } from "@/interfaces/reader"

@Component({
  middleware: "refresh-authentication",
  layout: "reader",
})
export default class Reader extends Vue {
  @Ref("reader-view") readonly readerView!: HTMLElement
  @Ref("reader-input") readonly readerInput!: HTMLElement
  @Mutation("main/setChangeWatcher") setChangeWatcher
  @Action("collections/restoreCollection") restoreCollection
  @Getter("collections/latestCollections") latestCollections
  @Getter("collections/firstCollection") firstCollection
  @Getter("main/showOptions") showOptions
  @Mutation("main/setShowOptions") setShowOptions
  @Action("collections/storeCollectionPayload") storeCollectionPayload
  @Action("main/recoverThemeState") recoverThemeState
  @Getter("main/pageTheme") pageTheme
  @Getter("main/pageSize") pageSize
  @Getter("main/pageFont") pageFont
  @Getter("main/watchReaderCFI") watchReaderCFI

  public work: IWork = {} as IWork
  public cover: string = ""
  public epub: File = {} as File
  public book: Book = {} as Book
  public rendition: Rendition = {} as Rendition
  public currentCFI: string | undefined = undefined
  public locations: string[] = []
  public completion: string = "0"

  public async updateReadingWork() {
    await this.storeCollectionPayload({
      collection: "work",
      payload: this.work,
      key: this.work.key,
    })
  }

  public changeReaderCFI() {
    this.currentCFI = this.work.currentCFI
    this.rendition.display(this.currentCFI)
    const currentLocation = this.rendition.currentLocation()
    this.completion = String((currentLocation as any).start.percentage)
  }

  @Watch("watchReaderCFI")
  public async watchReaderContents() {
    const watchResponse = this.watchReaderCFI.split("-")
    if (watchResponse[0] === "contents") {
      this.work = (await idb.getPayload("work", this.work.key)) as IWork
      await this.changeReaderCFI()
    } else if (watchResponse[0] === "completion") {
      const newLocation = this.book.locations.cfiFromPercentage(
        parseFloat(watchResponse[1])
      )
      this.work.currentCFI = newLocation
      await this.changeReaderCFI()
      await this.updateReadingWork()
    }
  }

  @Watch("pageFont")
  public changeReaderFont() {
    this.rendition.themes.font(this.pageFont.split("_").join("-"))
    this.rendition.start()
  }

  @Watch("pageSize")
  public changeReaderSize() {
    const checkSize = parseInt(this.pageSize)
    if (!checkSize || checkSize < 50 || checkSize > 200) return
    const newSize = `${this.pageSize}%`
    this.rendition.themes.fontSize(newSize)
    this.rendition.start()
  }

  @Watch("pageTheme")
  public changeReaderTheme() {
    this.rendition.themes.select(this.pageTheme)
    this.rendition.start()
  }

  public async listenerResponse(direction: string) {
    if (!this.showOptions) {
      if (direction === "next")
        (this.book as any).package.metadata.direction === "rtl"
          ? this.rendition.prev()
          : this.rendition.next()
      else if (direction === "prev")
        (this.book as any).package.metadata.direction === "rtl"
          ? this.rendition.next()
          : this.rendition.prev()
      else this.setShowOptions(true)
      // Get the current Canonical Fragment Identifier (CFI)
      // http://idpf.org/epub/linking/cfi/epub-cfi.html
      const currentLocation = this.rendition.currentLocation()
      if (!this.showOptions) {
        this.work.currentCFI = (currentLocation as any).start.cfi
        await this.updateReadingWork()
      }
      this.completion = String((currentLocation as any).start.percentage)
    }
  }

  public async initiliase() {
    const workKey = this.work.key
    if (Object.keys(this.work).length !== 0) {
      // Get the epub and cover
      this.epub = (await idb.getPayload("epub", workKey)) as File
      this.cover = (await idb.getPayload("cover", workKey)) as string
      // Get the work EPUB settings
      if (this.work.currentCFI) this.currentCFI = this.work.currentCFI
      if (this.work.locations && this.work.locations.length > 0)
        this.locations = this.work.locations
      this.setShowOptions(false)
      // @ts-expect-error
      this.book = new Book(this.epub)
      this.rendition = new Rendition(this.book, {
        manager: "continuous",
        spread: "none",
        width: "100%",
        height: "100%",
        snap: true,
      })
      // The entire chapter is rendered, with a discrete iframe for each view
      // When the next chapter is loaded, it triggers the process again
      // However ... each iframe is rendered twice, causing two page-turns / frame
      this.book.ready
        .then(() => {
          // Set the listeners
          clickXListener(
            this.readerInput,
            this.listenerResponse,
            this.readerView.clientWidth
          )
          keyListener(this.readerInput, this.listenerResponse)
          swipeListener(this.readerInput, this.listenerResponse)
          wheelListener(this.readerInput, this.listenerResponse)
          // Render the current page
          this.rendition.attachTo(this.readerView)
          this.rendition.display(this.currentCFI)
          this.rendition.themes.registerRules("dark", dark)
          this.rendition.themes.registerRules("light", light)
          this.rendition.themes.registerRules("serif", serif)
          this.rendition.themes.registerRules("sans-serif", sanserif)
          this.rendition.themes.select(this.pageTheme)
          this.rendition.themes.font(this.pageFont.split("_").join("-"))
          const newSize = `${this.pageSize}%`
          this.rendition.themes.fontSize(newSize)
          this.rendition.start()
          if (this.locations.length > 0)
            // @ts-expect-error
            return this.book.locations.load(this.locations)
          // Number of characters to split by
          else return this.book.locations.generate(50)
        })
        .then((location) => {
          if (!this.locations || this.locations.length === 0) {
            this.work.locations = location as string[]
            this.updateReadingWork()
          }
        })
      await this.book.ready
      await this.recoverThemeState()
      await this.setChangeWatcher(`newstream-${generateUUID()}`)
    }
  }

  async created() {
    let key = this.firstCollection("library")
    if (!key) {
      await this.restoreCollection({ collection: "work" })
      key = this.firstCollection("library")
    }
    if (key) {
      this.work = (await idb.getPayload("work", key)) as IWork
    }
    if (key && Object.keys(this.work).length !== 0) await this.initiliase()
    else this.$router.push("/")
  }
}
</script>

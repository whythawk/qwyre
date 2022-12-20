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
            :class="`z-1 relative h-screen w-screen sm:max-w-xl sm:mx-auto prose ${
              pageTheme === 'light' ? 'prose-reader-light' : 'prose-reader-dark'
            } ${
              pageFont === 'serif' ? 'font-serif' : 'font-sans'
            } ${readerFontSize}`"
          ></div>
        </client-only>
      </article>
    </div>
  </div>
</template>

<script lang="ts">
import WebSocketAsPromised from "websocket-as-promised"
import {
  Component,
  Action,
  Ref,
  Mutation,
  Getter,
  Watch,
  Vue,
} from "nuxt-property-decorator"
import {
  clickXListener,
  keyListener,
  swipeListener,
  wheelListener,
} from "@/mixins/readerListeners"
import { api, idb } from "@/api"
import { generateUUID } from "@/utilities"
import {
  ISocketDataStream,
  ISocketResponse,
  IStream,
  IStreamIn,
  IDataSource,
  IKeyable,
} from "@/interfaces"

@Component({
  layout: "reader",
  middleware: "refresh-authentication",
})
export default class Stream extends Vue {
  @Ref("reader-view") readonly readerView!: HTMLElement
  @Ref("reader-input") readonly readerInput!: HTMLElement
  @Action("collections/restoreCollection") restoreCollection
  @Action("collections/storePayload") storePayload
  @Action("collections/storeCollectionPayload") storeCollectionPayload
  @Mutation("collections/removeCollection") removeCollection
  @Getter("collections/firstCollection") firstCollection
  @Mutation("main/addNotification") addNotification
  @Mutation("main/setChangeWatcher") setChangeWatcher
  @Getter("main/isLoggedIn") isLoggedIn
  @Getter("main/showOptions") showOptions
  @Mutation("main/setShowOptions") setShowOptions
  @Mutation("main/setShowOptionsCall") setShowOptionsCall
  @Action("main/recoverThemeState") recoverThemeState
  @Getter("main/pageTheme") pageTheme
  @Getter("main/pageSize") pageSize
  @Getter("main/pageFont") pageFont
  @Getter("main/watchReaderCFI") watchReaderCFI
  @Getter("monetization/isStreaming") isMonetized
  @Getter("monetization/coilReceipt") coilReceipt
  @Getter("monetization/coilPointer") coilPointer
  @Mutation("monetization/setCoilPointer") setCoilPointer
  @Mutation("monetization/setCoilReceipt") setCoilReceipt
  @Mutation("monetization/setMonetizationWatcher") setMonetizationWatcher
  @Action("monetization/startMonetizationStream") startMonetizationStream
  @Action("monetization/stopMonetizationStream") stopMonetizationStream
  public token: string = ""
  public wsp: WebSocketAsPromised = {} as WebSocketAsPromised
  public stream: IStream = {} as IStream
  public streamIn: IStreamIn = {} as IStreamIn
  public streamOut: object = {}
  public currentPage: number = 0
  public currentPosition: number = 0
  public startPosition: number = 0
  public endPosition: number = 0
  public completion: string = "0"
  public readerFontSize: string = "prose-reader-base"
  public monetizing: boolean = false
  public inLibrary: boolean = false
  public owned: boolean = false
  public pointer: string = ""

  public async getStreamingWork() {
    try {
      this.stream = (await idb.getPayload(
        "stream",
        this.$route.params.id
      )) as IStream
      if (this.stream && Object.keys(this.stream).length !== 0)
        this.inLibrary = true
    } catch (e) {}
  }

  public async updateStreamingWork() {
    this.stream.currentPage = this.currentPage
    this.stream.currentPosition = this.currentPosition
    await this.storeCollectionPayload({
      collection: "stream",
      payload: this.stream,
      key: this.$route.params.id,
    })
    this.inLibrary = true
  }

  public getCompletion() {
    // https://stackoverflow.com/a/39887884/295606
    const totalCount = this.stream.stream.flat().length
    const completionCount = this.stream.stream
      .slice(0, this.currentPage)
      .flat().length
    const completion = completionCount / totalCount
    if (completion <= 1 && completion >= 0) this.completion = String(completion)
    else if (completion > 1) this.completion = "1"
    else this.completion = "0"
  }

  public getPositionFromCompletion(completion: number) {
    if (completion > 1 || completion < 0) return
    const totalLength = this.stream.stream.flat().length
    let position: number = Math.floor(completion * totalLength) - 1
    let newPage: number = 0
    let newPosition: number = 0
    while (newPosition < position) {
      if (this.stream.stream[newPage].length >= position) newPosition = position
      else {
        position -= this.stream.stream[newPage].length
        newPage += 1
      }
    }
    this.currentPage = newPage
    if (newPosition / this.stream.stream[newPage].length > 0.5) {
      this.startPosition = newPosition
      this.fillReaderView("prev")
    } else {
      this.endPosition = newPosition
      this.fillReaderView("next")
    }
  }

  @Watch("watchReaderCFI")
  public watchReaderContents() {
    const watchResponse = this.watchReaderCFI.split("-")
    let change
    if (["contents", "completion"].includes(watchResponse[0])) {
      change = watchResponse[1]
    }
    if (watchResponse[0] === "contents") {
      this.currentPage = parseInt(change)
      this.endPosition = 0
      this.startPosition = 0
      this.fillReaderView("next")
    } else if (watchResponse[0] === "completion") {
      this.getPositionFromCompletion(parseFloat(change))
    }
  }

  @Watch("pageSize")
  public changeReaderFontSize() {
    const checkSize = parseInt(this.pageSize)
    if (!checkSize || checkSize < 50 || checkSize > 200) return
    if (checkSize >= 50 && checkSize < 75)
      this.readerFontSize = "prose-reader-xs"
    if (checkSize >= 75 && checkSize < 100)
      this.readerFontSize = "prose-reader-sm"
    if (checkSize >= 100 && checkSize < 125)
      this.readerFontSize = "prose-reader-base"
    if (checkSize >= 125 && checkSize < 150)
      this.readerFontSize = "prose-reader-lg"
    if (checkSize >= 150 && checkSize < 175)
      this.readerFontSize = "prose-reader-xl"
    if (checkSize >= 175 && checkSize <= 200)
      this.readerFontSize = "prose-reader-2xl"
  }

  public async storeCoverImage(sourceID: string) {
    let cover = {} as IDataSource
    try {
      const response = await api.getCoverPublic(sourceID, "cover")
      if (response.data) {
        cover = response.data
        await this.storePayload({
          collection: "cover",
          payload: cover,
          key: this.$route.params.id,
        })
      }
    } catch (error) {}
  }

  public async updateStream() {
    if (
      !this.streamIn ||
      !Object.keys(this.streamIn).length ||
      !Object.prototype.hasOwnProperty.call(this.streamIn, "stream")
    )
      return
    if (this.stream.page === null || typeof this.stream.page === 'undefined') this.stream.page = 0
    if (this.streamIn.stream.length && this.streamIn.stream[0].length) {
      this.stream.stream[this.stream.page] = this.stream.stream[
        this.stream.page
      ].concat(this.streamIn.stream[0])
    }
    if (this.streamIn.stream.length >= 2 && this.streamIn.stream[1].length) {
      this.stream.stream = this.stream.stream.concat(
        this.streamIn.stream.slice(1)
      )
    }
    if (
      this.currentPage === this.stream.page &&
      this.currentPosition === this.stream.position
    ) {
      this.currentPage = this.streamIn.page
      this.currentPosition = this.streamIn.position
    }
    this.stream.page = this.streamIn.page
    this.stream.position = this.streamIn.position
    await this.updateStreamingWork()
  }

  @Watch("isMonetized")
  public async watchMonetization() {
    if (this.monetizing && !this.isMonetized) this.closeSocket()
    if (!this.monetizing && this.isMonetized) await this.initialiseSocket()
  }

  public async watchSocket(response: ISocketResponse) {
    switch (response.state) {
      case "initialise":
        this.stream = (response.data as ISocketDataStream).stream as IStream
        this.checkInitialPosition()
        if (!this.inLibrary) {
          if (
            this.currentPage === this.stream.page &&
            (this.currentPosition === this.stream.position ||
              this.currentPosition === 0)
          ) {
            this.fillReaderView("next")
          } else if (this.currentPosition === 0) {
            // Most likely, an initial fill
            this.fillReaderView("next")
          }
        }
        await this.updateStreamingWork()
        await this.setChangeWatcher(`newstream-${generateUUID()}`)
        await this.storeCoverImage(this.$route.params.id)
        this.setCoilReceipt(process.env.coilPointer as string)
        this.sendSocketResponse()
        break
      case "payment":
        this.monetizing = false
        if (this.isMonetized) {
          this.stopMonetizationStream()
          this.setMonetizationWatcher(generateUUID())
        }
        this.closeSocket()
        break
      case "pointer":
        this.pointer = (response.data as ISocketDataStream).pointer as string
        this.setCoilPointer(this.pointer)
        this.setMonetizationWatcher(generateUUID())
        break
      case "reading":
        this.streamIn = (response.data as ISocketDataStream).stream
        await this.updateStream()
        if (this.streamIn.page - this.stream.page > 0)
          await this.setChangeWatcher(`newstream-${generateUUID()}`)
        if (this.currentPage === this.stream.stream.length - 1) {
          this.endPosition = this.startPosition
          this.fillReaderView("next")
        }
        this.sendSocketResponse()
        break
      case "error":
        this.addNotification({
          content: `Error: ${response.error}.`,
          color: "error",
        })
        this.closeSocket()
        break
      case "complete":
        this.addNotification({
          content: "Import process complete.",
          color: "success",
        })
        this.owned = true
        this.closeSocket()
        break
    }
  }

  public async initialiseSocket() {
    this.wsp = api.socketStreamWork(this.$route.params.id)
    await this.wsp.open()
    this.wsp.onUnpackedMessage.addListener((data) => this.watchSocket(data))
    const jsonData: IKeyable = {
      token: "",
      paying: false,
      receipt: "",
      page: null,
      position: null,
    }
    if (this.isLoggedIn) {
      this.setCoilReceipt(this.coilPointer)
      if (this.stream && Object.keys(this.stream).length) {
        jsonData.token = this.token
        jsonData.paying = this.isMonetized
        jsonData.receipt = this.coilReceipt
        jsonData.page = this.stream.page
        jsonData.position = this.stream.position
      } else {
        jsonData.token = this.token
        jsonData.paying = this.isMonetized
        jsonData.receipt = this.coilReceipt
      }
    }
    if (!this.isLoggedIn) {
      if (this.stream && Object.keys(this.stream).length) {
        jsonData.paying = this.isMonetized
        jsonData.receipt = this.coilReceipt
        jsonData.page = this.stream.page
        jsonData.position = this.stream.position
      } else {
        jsonData.paying = this.isMonetized
        jsonData.receipt = this.coilReceipt
      }
    }
    this.wsp.sendPacked(jsonData)
    if (this.isMonetized) this.monetizing = true
  }

  public closeSocket() {
    if (this.monetizing) {
      this.wsp.close()
      this.monetizing = false
    }
  }

  public sendSocketResponse() {
    this.streamOut = { paying: this.isMonetized, receipt: this.coilReceipt }
    try {
      this.wsp.sendPacked(this.streamOut)
    } catch (e) {}
  }

  public checkInitialPosition() {
    if (this.stream.currentPage)
      this.currentPage = this.stream.currentPage as number
    else
      this.currentPage = this.stream.start_page
        ? this.stream.start_page
        : this.currentPage
    if (this.stream.currentPosition)
      this.currentPosition = this.stream.currentPosition as number
    if (this.currentPage > this.stream.stream.length - 1) {
      this.currentPage = this.stream.stream.length - 1
      this.currentPosition = 0
    }
    if (this.currentPosition > this.stream.stream[this.currentPage].length - 1)
      this.currentPosition = 0
    this.getCompletion()
  }

  public checkOverflow(): boolean {
    // https://stackoverflow.com/a/52194914/295606
    // https://stackoverflow.com/a/143889/295606
    // https://codepen.io/anon/pen/ZMJMZZ?editors=0011
    const curOverflow = this.readerView.style.overflow
    if (!curOverflow || curOverflow === "visible")
      this.readerView.style.overflow = "hidden"
    const isOverflowing =
      this.readerView.clientWidth < this.readerView.scrollWidth ||
      this.readerView.clientHeight < this.readerView.scrollHeight
    this.readerView.style.overflow = curOverflow
    return isOverflowing
  }

  public doFillReaderViewNext(): boolean {
    const oldContent = this.readerView.innerHTML
    let newContent = ""
    let doFill: boolean = false
    // fill the page until it overflows
    if (this.endPosition >= this.stream.stream[this.currentPage].length) {
      return false
    }
    newContent = ""
    for (
      let i = this.startPosition;
      i < this.stream.stream[this.currentPage].length - 25;
      i++
    ) {
      newContent += this.stream.stream[this.currentPage][i] + " "
    }
    if (newContent.charAt(0) !== "<") {
      // put beginning tags if missing
      let i = this.startPosition
      while (
        i >= 0 &&
        (this.stream.stream[this.currentPage][i].charAt(0) !== "<" ||
          this.stream.stream[this.currentPage][i].substr(0, 2) === "</")
      ) {
        i--
      }
      if (
        this.stream.stream[this.currentPage][i].charAt(0) === "<" &&
        this.stream.stream[this.currentPage][i].substr(0, 2) !== "</"
      )
        newContent = this.stream.stream[this.currentPage][i] + newContent
    }
    this.readerView.innerHTML = newContent
    // if one word fills the existing page, then do next
    doFill = this.checkOverflow()
    this.readerView.innerHTML = oldContent
    return doFill
  }

  public fillReaderView(direction) {
    let oldContent = ""
    let newContent = ""
    this.readerView.innerHTML = ""
    while (!this.checkOverflow()) {
      // fill the page until it overflows
      if (
        this.endPosition >= this.stream.stream[this.currentPage].length &&
        direction === "next"
      ) {
        return
      }
      oldContent = newContent
      newContent = ""
      for (let i = this.startPosition; i < this.endPosition; i++) {
        newContent += this.stream.stream[this.currentPage][i] + " "
      }
      this.readerView.innerHTML = newContent
      if (direction === "next") {
        this.endPosition++
      }
      if (direction === "prev") {
        this.startPosition--
        if (this.startPosition <= 25) {
          this.endPosition -= this.startPosition
          this.startPosition = 0
          direction = "next"
        }
      }
    }
    this.readerView.innerHTML = oldContent
    if (oldContent.charAt(0) !== "<") {
      // put beginning tags if missing
      let i = this.startPosition
      while (
        i >= 0 &&
        (this.stream.stream[this.currentPage][i].charAt(0) !== "<" ||
          this.stream.stream[this.currentPage][i].substr(0, 2) === "</")
      ) {
        i--
      }
      if (
        this.stream.stream[this.currentPage][i].charAt(0) === "<" &&
        this.stream.stream[this.currentPage][i].substr(0, 2) !== "</"
      )
        this.readerView.innerHTML =
          this.stream.stream[this.currentPage][i] + oldContent
    }
    this.currentPosition = this.endPosition
  }

  public async listenerResponse(direction: string) {
    if (!this.showOptions) {
      if (direction === "next") {
        if (
          this.currentPage < this.stream.stream.length - 1 &&
          this.endPosition >= this.stream.stream[this.currentPage].length - 1
        ) {
          // Start at the beginning of the next chapter
          this.currentPage += 1
          this.endPosition = 0
        }
        if (
          !this.owned &&
          !this.monetizing &&
          this.currentPage === this.stream.stream.length - 1 &&
          this.endPosition >= this.stream.stream[this.currentPage].length - 1
        ) {
          // toggle the damn thing
          this.currentPosition = this.endPosition
          await this.setShowOptionsCall(false)
          await this.setShowOptionsCall(true)
          await this.setShowOptions(true)
        } else if (
          !this.owned &&
          this.monetizing &&
          this.currentPage === this.stream.stream.length - 1
        ) {
          if (this.doFillReaderViewNext()) {
            this.startPosition = this.endPosition
            this.fillReaderView("next")
          }
        } else {
          this.startPosition = this.endPosition
          this.fillReaderView("next")
        }
      } else if (direction === "prev") {
        if (this.startPosition === 0 && this.currentPage > 0) {
          // Start at the end of the previous chapter
          this.currentPage -= 1
          this.startPosition = this.stream.stream[this.currentPage].length - 1
        }
        this.endPosition = this.startPosition
        this.fillReaderView("prev")
      } else this.setShowOptions(true)
      if (!this.showOptions) {
        await this.updateStreamingWork()
        this.getCompletion()
      }
    }
  }

  async initiliase() {
    // Don't need to be logged in, or monetized, to get the initial stream
    if (this.stream && Object.keys(this.stream).length) {
      this.checkInitialPosition()
      // Fill the page back from the current page & position
      this.startPosition = this.currentPosition
      this.endPosition = this.currentPosition
      this.fillReaderView("prev")
    }
    this.changeReaderFontSize()
    // Set the UI listeners
    clickXListener(
      this.readerInput,
      this.listenerResponse,
      this.readerView.clientWidth
    )
    keyListener(this.readerInput, this.listenerResponse)
    swipeListener(this.readerInput, this.listenerResponse)
    wheelListener(this.readerInput, this.listenerResponse)
    this.setShowOptions(false)
    await this.recoverThemeState()
    // Only now, initialise the socket
    await this.initialiseSocket()
  }

  beforeRouteLeave(to, from, next) {
    this.closeSocket()
    if (this.isMonetized) {
      this.setCoilPointer(process.env.coilPointer as string)
      this.setMonetizationWatcher(generateUUID())
    }
    this.setCoilReceipt("")
    next()
  }

  async created() {
    if (process.client) {
      if ((this as any).$cookies.get("token"))
        this.token = (this as any).$cookies.get("token")
      await this.getStreamingWork()
      if (this.stream && Object.keys(this.stream).length !== 0) {
        let key = this.firstCollection("library")
        if (!key) {
          await this.restoreCollection({ collection: "stream" })
          key = this.firstCollection("library")
        }
        if (!key || key !== this.stream.key)
          await this.storeCollectionPayload({
            collection: "stream",
            payload: this.stream,
            key: this.$route.params.id,
          })
      }
      await this.initiliase()
      await this.setChangeWatcher(`newstream-${generateUUID()}`)
    }
  }
}
</script>

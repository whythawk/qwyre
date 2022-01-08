import { fileOpen } from "browser-fs-access"
import { Book } from "epubjs"
import { Action, Component, Mutation, Vue } from "nuxt-property-decorator"
import { prxy } from "@/api"
import { isValidHttpUrl } from "@/utilities"
import { IWorkMetadata, IWorkContents, IWork } from "@/interfaces"

@Component
export default class ImportWorkData extends Vue {
  @Action("collections/storePayload") storePayload
  @Action("collections/storeCollectionPayload") storeCollectionPayload
  @Mutation("main/addNotification") addNotification
  public workURL: string = ""
  public blob: File = {} as File

  public async importWorkFromURL() {
    const checkURL = isValidHttpUrl(this.workURL)
    if (!checkURL) {
      this.addNotification({
        content: "URL to epub is not a valid link.",
        color: "error",
      })
    } else {
      try {
        const workBlob = await prxy.proxyGetBlob(this.workURL)
        this.blob = await this.getFileFromBase64(
          workBlob.data,
          this.workURL.split("/").slice(-1)[0],
          "application/epub+zip"
        )
      } catch (e) {
        this.addNotification({
          content: "Please import a valid epub.",
          color: "error",
        })
      }
    }
  }

  public async importWorkFromClick() {
    try {
      this.blob = await fileOpen({
        mimeTypes: ["application/epub+zip"],
        extensions: [".epub"],
      })
    } catch (e) {
      this.addNotification({
        content: "Please import a valid epub.",
        color: "error",
      })
    }
  }

  public async getFileFromBase64(
    payload: string,
    filename: string,
    mimeType: string
  ) {
    // https://stackoverflow.com/a/38935990/295606
    // https://developer.mozilla.org/en-US/docs/Learn/JavaScript/Asynchronous/Async_await
    const response = await fetch(payload)
    const responseBuffer = await response.arrayBuffer()
    return new File([responseBuffer], filename, { type: mimeType })
  }

  public getBase64FromFile(file: File) {
    // https://stackoverflow.com/a/57272491/295606
    return new Promise((resolve, reject) => {
      const reader = new FileReader()
      reader.readAsDataURL(file)
      reader.onload = () => resolve(reader.result)
      reader.onerror = (error) => reject(error)
    })
  }

  public getBase64FromCoverUrl(src: string) {
    // https://javascript.info/blob
    // https://stackoverflow.com/questions/20424279/canvas-todataurl-securityerror
    // https://stackoverflow.com/a/64747517/295606
    // https://stackoverflow.com/questions/46399223/async-await-in-image-loading
    // https://stackoverflow.com/a/20285053/295606
    return new Promise<string>((resolve) => {
      const img = new Image()
      img.setAttribute("crossOrigin", "anonymous")
      img.onload = () => {
        const canvas = document.createElement("canvas")
        // Shrink the cover size slightly
        const canvasWidth = img.naturalWidth > 800 ? 800 : img.naturalWidth
        const canvasHeight =
          (canvasWidth * img.naturalHeight) / img.naturalWidth
        canvas.width = canvasWidth
        canvas.height = canvasHeight
        const ctx = canvas.getContext("2d") as CanvasRenderingContext2D
        ctx.drawImage(
          img,
          0,
          0,
          img.naturalWidth,
          img.naturalHeight,
          0,
          0,
          canvas.width,
          canvas.height
        )
        resolve(canvas.toDataURL())
      }
      img.src = src
    })
  }

  public storeWork(blob: File | string, reset: boolean = true) {
    // Open the epub
    // https://stackoverflow.com/a/61040339/295606
    // epubjs is confuse ...
    // @ts-expect-error
    const book: Book = new Book(blob)
    const work: IWork = {} as IWork
    book.ready.then(async () => {
      // Get the metadata and populate the work
      work.metadata = {
        ...(book.packaging.metadata as unknown as IWorkMetadata),
      }
      work.key = book.packaging.metadata.identifier
      work.date_created = new Date(book.packaging.metadata.pubdate)
      // https://stackoverflow.com/a/52311223/295606
      const firstChapter = book.navigation.landmarks.find((landmark) =>
        landmark.type!.toLowerCase().includes("bodymatter")
      )
      if (
        firstChapter &&
        Object.prototype.hasOwnProperty.call(firstChapter, "href")
      )
        work.currentCFI = firstChapter.href
      // Generate the table of contents
      const contents: IWorkContents[] = []
      for (const content of book.navigation.toc) {
        contents.push({
          title: content.label.replace(/\r/g, "").trim(),
          href: content.href.trim(),
        })
      }
      work.contents = contents.slice(0)
      await this.storeCollectionPayload({
        collection: "work",
        payload: work,
        key: work.key,
      })
      await this.storePayload({
        collection: "epub",
        payload: blob,
        key: work.key,
      })
      // Save the cover
      book.coverUrl().then(async (url) => {
        let cover
        if (url) cover = await this.getBase64FromCoverUrl(url)
        await this.storePayload({
          collection: "cover",
          payload: cover,
          key: work.key,
        })
      })
    })
    if (reset) {
      this.blob = {} as File
      this.workURL = ""
    }
  }
}

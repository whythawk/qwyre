<template>
  <div class="container min-h-screen mx-auto flex flex-col">
    <!-- Import via URL -->
    <form @submit.prevent="submit">
      <div class="mt-8 max-w-2xl mx-auto">
        <div class="grid grid-cols-1 gap-4 w-full">
          <!-- Title -->
          <label class="block">
            <span class="text-ochre-600 text-xs ml-3">Paste remote link</span>
            <span class="inpt-span">
              <input
                id="workURL"
                v-model="workURL"
                name="workURL"
                type="text"
                class="inpt-text rounded-l-full"
                placeholder="URL to an online version of the '.epub' you wish to import."
            /></span>
          </label>
        </div>
      </div>
    </form>
    <!-- Import via local file -->
    <div class="flex flex-col md:flex-row mx-auto mt-8">
      <div
        ref="import-work"
        class="
          grid grid-rows-6 grid-cols-0
          gap-1
          bg-malachite-100
          rounded-lg
          max-h-full
          w-60
          h-96
        "
      >
        <div class="row-start-2 row-span-2">
          <SvgIcon
            terms="h-10 w-10 sm:h-20 sm:w-16 mx-auto my-auto block text-malachite-600"
            icon="svgBookOpen"
          />
        </div>
        <div class="row-span-3">
          <button
            type="submit"
            class="btn-malachite-sm sm:btn-malachite mx-auto my-auto block"
          >
            <SvgIcon
              terms="w-5 h-6 sm:w-10 sm:h-8 inline-block"
              icon="svgPlus"
            />
          </button>
        </div>
      </div>
    </div>
    <!-- Call to action -->
    <div class="mt-8 max-w-2xl mx-auto">
      <button type="submit" class="btn-woad-extended" @click.prevent="submit">
        <SvgIcon terms="w-5 h-4 inline-block mr-1" icon="svgReturn" />
        <span>Import work</span>
      </button>
    </div>
  </div>
</template>

<script lang="ts">
import { fileOpen } from "browser-fs-access"
import WebSocketAsPromised from "websocket-as-promised"
import {
  Component,
  Ref,
  Getter,
  Mutation,
  Prop,
  mixins,
} from "nuxt-property-decorator"
import { prxy, api, idb } from "@/api"
import { isValidHttpUrl } from "@/utilities"
import importWorkData from "@/mixins/importWorkData"
import { ISocketResponse } from "@/interfaces"

@Component
export default class ConversionUpdateEpub extends mixins(importWorkData) {
  @Prop(String) readonly workId!: string
  @Ref("import-work") readonly openWork!: HTMLButtonElement
  @Mutation("main/addNotification") addNotification
  @Mutation("main/removeNotification") removeNotification
  @Getter("collections/firstCollection") firstCollection
  public workURL: string = ""
  public blob: File = {} as File
  public wsp: WebSocketAsPromised = {} as WebSocketAsPromised
  public hasSocket: boolean = false

  public watchSocket(response: ISocketResponse) {
    const processingNotification = {
      content: "Processing import.",
      showProgress: true,
      color: "info",
    }
    switch (response.state) {
      case "received":
        this.addNotification({
          content: "Import received.",
          color: "info",
        })
        break
      case "error":
        this.addNotification({
          content: `Error: ${response.error}.`,
          color: "error",
        })
        this.wsp.close()
        break
      case "working":
        this.removeNotification(processingNotification)
        this.addNotification(processingNotification)
        break
      case "complete":
        this.removeNotification(processingNotification)
        this.addNotification({
          content: "Import process complete.",
          color: "success",
        })
        this.wsp.close()
        break
    }
  }

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

  public async getCover(): Promise<string | null> {
    const workKey = await this.firstCollection("work")
    return (await idb.getPayload("cover", workKey)) as string | null
  }

  public async submit(): Promise<void> {
    if (this.workURL) {
      await this.importWorkFromURL()
    }
    try {
      if (this.blob) {
        const token = (this as any).$cookies.get("token")
          ? (this as any).$cookies.get("token")
          : ""
        this.storeWork(this.blob)
        const newBlob = await this.getBase64FromFile(this.blob)
        // const newCover = await this.getCover()
        const jsonData = {
          work: newBlob,
          token,
          save: true,
        }
        await this.wsp.open()
        this.wsp.onUnpackedMessage.addListener((data) => this.watchSocket(data))
        this.wsp.sendPacked(jsonData)
      }
    } catch (e) {
      this.addNotification({
        content: "Please import a valid epub.",
        color: "error",
      })
    }
  }

  public initialiseSocket() {
    if (!this.hasSocket) {
      this.wsp = api.socketUpdateWork(this.workId)
      this.hasSocket = true
    }
  }

  created() {
    this.initialiseSocket()
  }

  mounted(): void {
    this.openWork.disabled = false
    this.openWork.addEventListener("click", async () => {
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
    })
  }
}
</script>

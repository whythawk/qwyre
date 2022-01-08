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
    <span class="text-ochre-600 text-xs ml-3 mt-6 text-center"
      >Drag 'n drop or click from file</span
    >
    <div class="flex flex-col md:flex-row mx-auto mt-1">
      <div
        ref="import-work"
        class="
          grid grid-rows-6 grid-cols-0
          gap-1
          bg-malachite-100
          rounded-lg
          max-h-full
          w-60
          h-80
        "
      >
        <img
          v-show="blob && Object.keys(blob).length"
          class="
            object-cover object-center
            rounded-lg
            min-h-full min-w-full
            animate-fade-in
          "
          src="/never-talk-to-strangers.jpg"
          alt=""
        />
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
import { isValidHttpUrl, generateUUID } from "@/utilities"
import importWorkData from "@/mixins/importWorkData"
import { ISocketResponse } from "@/interfaces"

@Component
export default class ConversionImportEpub extends mixins(importWorkData) {
  @Prop(String) readonly workId!: string
  @Ref("import-work") readonly openWork!: HTMLButtonElement
  @Mutation("main/addNotification") addNotification
  @Mutation("main/removeNotification") removeNotification
  @Mutation("main/setChangeWatcher") setChangeWatcher
  @Getter("main/token") token
  @Getter("collections/firstCollection") firstCollection
  public workURL: string = ""
  public blob: File = {} as File
  public wsp: WebSocketAsPromised = {} as WebSocketAsPromised
  public hasSocket: boolean = false

  public reset() {
    this.workURL = ""
    this.blob = {} as File
    this.hasSocket = false
  }

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
        this.reset()
        this.setChangeWatcher(generateUUID())
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

  public async submit(): Promise<void> {
    if (this.workURL) {
      await this.importWorkFromURL()
    }
    try {
      if (this.blob) {
        this.storeWork(this.blob, false)
        const newBlob = await this.getBase64FromFile(this.blob)
        const jsonData = {
          work: newBlob,
          token: this.token,
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
      if (this.workId) this.wsp = api.socketUpdateWork(this.workId)
      else this.wsp = api.socketImportWork()
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

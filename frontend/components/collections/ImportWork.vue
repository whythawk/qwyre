<template>
  <div>
    <button
      type="submit"
      class="btn-sinopia-extended-sm flex items-center h-8"
      @click.prevent="showModal = true"
    >
      <SvgIcon terms="w-5 h-4 inline-block mr-1 mb-1" icon="svgBookOpen" />
      <span class="text-sm">Import .epub</span>
    </button>
    <div
      v-show="showModal"
      class="relative z-10 inset-0 overflow-y-auto"
      aria-labelledby="modal-title"
      role="dialog"
      aria-modal="true"
    >
      <div
        class="
          flex
          items-end
          justify-center
          min-h-screen
          pt-4
          px-4
          pb-20
          text-center
          sm:block sm:p-0
        "
      >
        <div v-show="showModal" class="fixed inset-0">
          <span
            class="hidden sm:inline-block sm:align-middle sm:h-screen"
            aria-hidden="true"
            >&#8203;</span
          >
          <transition
            enter-active-class="transition ease-out duration-300"
            enter-class="transform opacity-0 translate-y-4 sm:translate-y-0 sm:scale-95"
            enter-to-class="transform opacity-100 translate-y-0 sm:scale-100"
            leave-active-class="transition ease-in duration-200"
            leave-class="transform opacity-100 translate-y-0 sm:scale-100"
            leave-to-class="transform opacity-0 translate-y-4 sm:translate-y-0 sm:scale-95"
          >
            <div
              v-show="showModal"
              class="
                inline-block
                align-bottom
                bg-white
                rounded-lg
                px-4
                pt-5
                pb-4
                text-left
                overflow-hidden
                shadow-xl
                transform
                transition-all
                sm:my-8 sm:align-middle sm:max-w-sm sm:w-full sm:p-6
              "
            >
              <div class="mx-auto flex flex-col">
                <div class="flex-1 flex text-center mx-auto">
                  <SvgIcon
                    terms="flex-shrink-0 w-6 h-6 mx-2 text-ochre-700"
                    icon="svgBookOpen"
                  />
                  <h3 class="text-base font-semibold text-center">
                    Import to your workspace
                  </h3>
                </div>
                <!-- Import via URL -->
                <form @submit.prevent="submit">
                  <div class="mt-8 max-w-2xl mx-auto">
                    <div class="grid grid-cols-1 gap-4 w-full">
                      <!-- Title -->
                      <label class="block">
                        <span class="text-ochre-600 text-xs ml-3"
                          >Paste remote link</span
                        >
                        <span class="inpt-span">
                          <input
                            id="workURL"
                            v-model="workURL"
                            name="workURL"
                            type="text"
                            class="inpt-text rounded-l-full"
                            placeholder="URL to online version of the '.epub'."
                        /></span>
                      </label>
                    </div>
                  </div>
                </form>
                <!-- Import via local file -->
                <span class="text-ochre-600 text-xs ml-3 mt-6"
                  >Drag 'n drop or click from file</span
                >
                <div class="flex flex-col md:flex-row mx-auto mt-1">
                  <div
                    class="
                      grid grid-rows-3 grid-cols-0
                      gap-1
                      bg-malachite-100
                      ring-malachite-600
                      border-malachite-10 border-2
                      shadow
                      rounded-lg
                      max-h-full
                      h-32
                      w-64
                    "
                    @click.prevent="importWorkFromClick"
                  >
                    <img
                      v-show="blob && Object.keys(blob).length"
                      class="
                        object-cover object-center
                        h-32
                        w-64
                        rounded-lg
                        animate-fade-in
                      "
                      src="/never-talk-to-strangers.jpg"
                      alt=""
                    />
                    <div class="row-start-2 row-span-3">
                      <button
                        type="submit"
                        class="
                          btn-malachite-sm
                          sm:btn-malachite
                          mx-auto
                          my-auto
                          block
                        "
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
                <div class="flex space-x-4 mt-8 w-full justify-center">
                  <button
                    type="cancel"
                    class="btn-sinopia-extended"
                    @click.prevent="cancel"
                  >
                    <SvgIcon terms="w-5 h-4 inline-block mr-1" icon="svgX" />
                    <span>Cancel</span>
                  </button>
                  <button
                    type="submit"
                    class="btn-woad-extended"
                    @click.prevent="submit"
                  >
                    <SvgIcon
                      terms="w-5 h-4 inline-block mr-1"
                      icon="svgReturn"
                    />
                    <span>Import</span>
                  </button>
                </div>
              </div>
            </div>
          </transition>
        </div>
      </div>
    </div>
  </div>
</template>

<script lang="ts">
import WebSocketAsPromised from "websocket-as-promised"
import { Component, Getter, Mutation, mixins } from "nuxt-property-decorator"
import { api } from "@/api"
import importWorkData from "@/mixins/importWorkData"
import { ISocketResponse } from "@/interfaces"

@Component
export default class CollectionsImportWork extends mixins(importWorkData) {
  @Mutation("main/addNotification") addNotification
  @Mutation("main/removeNotification") removeNotification
  @Getter("main/token") token
  @Getter("collections/firstCollection") firstCollection
  public workURL: string = ""
  public blob: File = {} as File
  public wsp: WebSocketAsPromised = {} as WebSocketAsPromised
  public hasSocket: boolean = false
  public showModal: boolean = false

  public cancel() {
    this.showModal = false
    this.workURL = ""
    this.blob = {} as File
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
        this.cancel()
        break
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
      this.wsp = api.socketImportWork()
      this.hasSocket = true
    }
  }

  created() {
    this.initialiseSocket()
  }
}
</script>

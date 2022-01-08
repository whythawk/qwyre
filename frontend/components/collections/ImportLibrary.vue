<template>
  <div class="aspect-h-16 aspect-w-10">
    <div
      class="
        grid grid-rows-6 grid-cols-0
        gap-1
        bg-malachite-100
        hover:bg-malachite-200
        rounded-lg
        max-h-full
      "
      @click.prevent="showModal = true"
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
          <SvgIcon terms="w-5 h-6 sm:w-10 sm:h-8 inline-block" icon="svgPlus" />
        </button>
      </div>
    </div>
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
                    Import to your library
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
import { Component, mixins } from "nuxt-property-decorator"
import importWorkData from "@/mixins/importWorkData"
import { isValidHttpUrl } from "@/utilities"

@Component
export default class CollectionsImportLibrary extends mixins(importWorkData) {
  public showModal: boolean = false

  public cancel() {
    this.showModal = false
    this.workURL = ""
  }

  public async submit(): Promise<void> {
    if (this.workURL) {
      await this.importWorkFromURL()
    }
    try {
      if (this.blob) {
        this.storeWork(this.blob)
        this.cancel()
      }
    } catch (e) {
      this.addNotification({
        content: "Please import a valid epub.",
        color: "error",
      })
    }
  }
}
</script>

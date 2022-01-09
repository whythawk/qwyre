<template>
  <div>
    <button
      type="submit"
      class="btn-malachite-extended-sm flex items-center h-8"
      @click.prevent="showModal = true"
    >
      <SvgIcon terms="w-4 h-3 inline-block mr-1 mb-1" icon="svgLink" />
      <span class="text-sm">Generate link</span>
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
                    icon="svgLink"
                  />
                  <h3 class="text-base font-semibold text-center">
                    Generate a link from your work
                  </h3>
                </div>
                <!-- Import via URL -->
                <form>
                  <div class="mt-8 max-w-2xl mx-auto">
                    <div class="grid grid-cols-1 gap-4 w-full">
                      <label class="block">
                        <span class="text-ochre-600 text-xs ml-3"
                          >Paste your remote link</span
                        >
                        <span class="inpt-span">
                          <input
                            id="workURL"
                            v-model="workURL"
                            name="workURL"
                            type="text"
                            class="inpt-text rounded-l-full"
                            placeholder="URL to a remote '.epub'."
                        /></span>
                      </label>
                    </div>
                  </div>
                </form>
                <!-- Import via local file -->
                <span class="text-ochre-600 text-xs ml-3 mt-6"
                  >Copy this generated link</span
                >

                <span class="inpt-span-area">
                  <textarea
                    id="shareURL"
                    v-model="shareURL"
                    name="shareURL"
                    type="text"
                    class="inpt-textarea"
                    rows="4"
                    placeholder="Copy the validated link generated for you."
                  ></textarea>
                </span>

                <!-- Call to action -->
                <div class="flex space-x-4 mt-8 w-full justify-center">
                  <button
                    type="submit"
                    class="btn-sinopia-extended"
                    @click.prevent="close"
                  >
                    <SvgIcon terms="w-5 h-4 inline-block mr-1" icon="svgX" />
                    <span>Close</span>
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
import { Component, Mutation, Watch, Vue } from "nuxt-property-decorator"
import { isValidHttpUrl } from "@/utilities"

@Component
export default class CollectionsImportLink extends Vue {
  @Mutation("main/addNotification") addNotification
  public showModal: boolean = false
  public workURL: string = ""
  public shareURL: string = ""

  public close() {
    this.showModal = false
    this.workURL = ""
    this.shareURL = ""
  }

  @Watch("workURL")
  public encodeLink() {
    if (this.workURL && isValidHttpUrl(this.workURL)) {
      this.shareURL = `${window.location.origin}?import=${encodeURIComponent(
        this.workURL
      )}`
    }
  }
}
</script>

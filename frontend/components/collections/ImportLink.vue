<template>
  <div>
    <label
      for="create-link"
      class="btn-malachite-extended-sm flex items-center h-8 cursor-pointer"
    >
      <SvgIcon terms="w-4 h-3 inline-block mr-1 mb-1" icon="svgLink" />
      <span class="text-sm">Link</span>
    </label>
    <input id="create-link" type="checkbox" class="modal-toggle" />
    <label for="create-link" class="modal cursor-pointer">
      <label
        for=""
        class="modal-box relative"
        aria-labelledby="modal-title"
        role="dialog"
        aria-modal="true"
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
          <p class="text-sm mt-1">
            Create a link so your readers can import an ebook hosted on your
            website into Qwyre. The ebook will be stored in your reader's
            browser and is never uploaded to Qwyre.
          </p>
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
            <label
              for="create-link"
              class="btn-sinopia-extended-sm flex items-center h-8"
            >
              <SvgIcon terms="w-5 h-4 inline-block mr-1 mb-1" icon="svgX" />
              <span>Close</span>
            </label>
          </div>
        </div>
      </label>
    </label>
  </div>
</template>

<script lang="ts">
import { Component, Mutation, Watch, Vue } from "nuxt-property-decorator"
import { isValidHttpUrl } from "@/utilities"

@Component
export default class CollectionsImportLink extends Vue {
  @Mutation("main/addNotification") addNotification
  public workURL: string = ""
  public shareURL: string = ""

  public close() {
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

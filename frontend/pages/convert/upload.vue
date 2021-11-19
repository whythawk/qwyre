<template>
  <div class="flex flex-col mx-auto">
    <div>
      <p class="pb-1">
        <span class="font-semibold">Qwyre</span> will generate your epub,
        including the cover and table of contents, from the files you upload.
      </p>
      <div class="grid gap-y-0 gap-x-4 grid-cols-7 py-1">
        <div class="col-span-7 sm:col-span-5">
          <p class="py-1">
            Your <span class="font-semibold">Word</span>
            <span class="italic font-semibold">.docx</span> file must contain
            only the creative content you wish included in the table of
            contents. Your document must be correctly marked up with headers for
            chapter creation. If you see anything weird in structure or in the
            table of contents in your epub, review the requirements.
          </p>
          <p>
            There is no standard for cover size, dimensions or resolution
            required for an EPUB. We recommend an image (<span
              class="italic font-semibold"
              >.jpeg, .jpg or .png</span
            >) of 1,600 by 2,400 pixels, and less than 5Mb in size. Create your
            cover (or have someone create it for you) exactly as you wish it to
            appear. Nothing will be added, removed, or changed.
            <span class="font-semibold italic"
              >Ensure you have appropriate rights to use your cover image, and
              acknowledge the creator on the description page.</span
            >
          </p>
        </div>
        <SvgIcon
          terms="hidden py-2 sm:block sm:col-span-1 sm:w-30 sm:h-44"
          icon="svgCoverAspectRatio"
        />
      </div>
      <nuxt-link
        class="flex flex-row text-woad-500 underline pt-1"
        to="/get-started"
      >
        <SvgIcon terms="h-6 w-6 inline-flex" icon="svgInformationCircle" />
        <p>Read the Guide for more details...</p>
      </nuxt-link>
    </div>
    <div class="flex flex-col md:flex-row mx-auto mt-8">
      <form ref="cover-form">
        <div
          class="relative flex flex-col justify-center m-1 w-60 h-96 bg-ochre-400 hover:bg-ochre-700 text-ochre-50 filter drop-shadow-lg shadow transition ease-in duration-200"
        >
          <img
            v-show="coverFileString"
            ref="preview-cover"
            class="object-cover object-center min-h-full min-w-full animate-fade-in"
          />
          <label
            for="clickCoverUpload"
            class="absolute text-center text-lg bg-ochre-600 bg-opacity-70 hover:bg-opacity-90 transition ease-in duration-200"
          >
            <span
              ref="new-cover-uploaded"
              hidden
              class="absolute top-2 right-2"
            >
              <span
                class="animate-ping absolute inline-flex h-3 w-3 rounded-full bg-malachite-100 opacity-75"
              ></span>
              <span
                class="relative inline-flex rounded-full mb-2 h-3 w-3 bg-malachite-200"
              ></span>
            </span>
            <SvgIcon terms="h-16 w-16 mx-auto" icon="svgBookOpen" />
            <span v-if="!coverFileString"
              >Drag 'n drop, or click here, to upload your cover.</span
            >
            <span v-else
              >Drag 'n drop, or click here, to update your cover.</span
            >
            <br />[<i>.jpg</i>, <i>.jpeg</i> or <i>.png</i> only]
          </label>
          <input
            id="clickCoverUpload"
            type="file"
            class="invisible"
            accept="image/jpeg, image/png, image/jpg"
            @change="coverFileUpload($event)"
          />
        </div>
      </form>
      <form ref="work-form">
        <div
          class="relative flex flex-col justify-center m-1 w-60 h-96 bg-woad-400 hover:bg-woad-700 text-ochre-50 filter drop-shadow-lg shadow transition ease-in duration-200"
        >
          <img
            v-show="workFileString"
            class="object-cover object-center min-h-full min-w-full animate-fade-in"
            src="/never-talk-to-strangers.jpg"
            alt=""
          />
          <label
            for="clickWorkUpload"
            class="absolute text-center text-lg bg-woad-600 bg-opacity-70 hover:bg-opacity-90 transition ease-in duration-200"
          >
            <span ref="new-work-uploaded" hidden class="absolute top-2 right-2">
              <span
                class="animate-ping absolute inline-flex h-3 w-3 rounded-full bg-malachite-100 opacity-75"
              ></span>
              <span
                class="relative inline-flex rounded-full mb-2 h-3 w-3 bg-malachite-200"
              ></span>
            </span>
            <SvgIcon terms="h-16 w-16 mx-auto" icon="svgDocumentText" />
            <span v-if="!workFileString"
              >Drag 'n drop, or click here, to upload your work.</span
            >
            <span v-else
              >Drag 'n drop, or click here, to update your work.</span
            >
            <br />[<i>.docx</i> only]
          </label>
          <input
            id="clickWorkUpload"
            type="file"
            class="invisible"
            accept="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
            @change="workFileUpload($event)"
          />
        </div>
      </form>
    </div>
    <!-- Call to action -->
    <div class="mt-8 max-w-2xl mx-auto">
      <button type="submit" class="btn-woad-extended" @click.prevent="submit">
        <SvgIcon terms="w-5 h-4 inline-block mr-1" icon="svgReturn" />
        <span>Store files</span>
      </button>
    </div>
  </div>
</template>

<script lang="ts">
/* eslint-disable camelcase */
import {
  Component,
  Vue,
  Getter,
  Watch,
  Ref,
  Action,
  Mutation,
} from "nuxt-property-decorator"
import { idb } from "@/api"

@Component
export default class UploadWork extends Vue {
  @Getter("conversions/conversionKey") conversionKey
  @Action("collections/storePayload") storePayload
  @Action("conversions/updateConversionState") updateConversionState
  @Mutation("main/addNotification") addNotification
  @Ref("cover-form") readonly coverForm!: HTMLFormElement
  @Ref("preview-cover") readonly coverPreview!: HTMLImageElement
  @Ref("work-form") readonly workForm!: HTMLFormElement
  @Ref("new-work-uploaded") readonly newWorkUpload!: HTMLSpanElement
  @Ref("new-cover-uploaded") readonly newCoverUpload!: HTMLSpanElement
  public dragAndDropCapable: boolean = false
  public coverFile: File | null = null
  public coverFileString: string = ""
  public workFile: File | null = null
  public workFileString: string = ""

  public async submit(): Promise<void> {
    if (this.coverFileString && this.workFileString) {
      // Store coverFileString
      await this.storePayload({
        collection: "cover",
        payload: this.coverFileString,
        key: this.conversionKey,
      })
      // Store workFileString
      await this.storePayload({
        collection: "docx",
        payload: this.workFileString,
        key: this.conversionKey,
      })
      // Update the conversion state
      await this.updateConversionState({
        conversionKey: this.conversionKey,
        conversionStep: "upload",
      })
      this.$router.push("/convert/dedication")
    } else {
      this.addNotification({
        content: "Please upload all required files.",
        color: "error",
      })
    }
  }

  public coverFileUpload(event): void {
    if (event.target && event.target.files.length) {
      this.coverFile = event.target.files[0]
    }
  }

  public workFileUpload(event): void {
    if (event.target && event.target.files.length) {
      this.workFile = event.target.files[0]
    }
  }

  @Watch("coverFile")
  public getCoverImagePreview() {
    const imageError = {
      content: "Not a valid image file. Must be one of .png, .jpg, or .jpeg.",
      color: "error",
    }
    // https://hacks.mozilla.org/2012/02/saving-images-and-files-in-localstorage/
    // https://stackoverflow.com/a/19183658/295606
    if (this.coverFile && /\.(jpe?g|png)$/i.test(this.coverFile.name)) {
      const reader = new FileReader()
      reader.addEventListener(
        "load",
        (): void => {
          if (
            reader.result &&
            String(reader.result).match(/^data:image\/(png|jpe?g);base64,/)
          ) {
            this.coverPreview.src = String(reader.result)
            this.coverFileString = String(reader.result)
            this.newCoverUpload.hidden = false
            setTimeout(() => {
              this.newCoverUpload.hidden = true
            }, 2000)
          } else {
            this.addNotification(imageError)
          }
        },
        false
      )
      reader.readAsDataURL(this.coverFile)
    } else {
      this.addNotification(imageError)
    }
  }

  @Watch("workFile")
  public getWorkAsString() {
    const fileError = {
      content: "Not a valid .docx file.",
      color: "error",
    }
    if (this.workFile && /\.(docx)$/i.test(this.workFile.name)) {
      const reader = new FileReader()
      reader.addEventListener(
        "load",
        (): void => {
          if (
            reader.result &&
            String(reader.result).includes(
              "application/vnd.openxmlformats-officedocument.wordprocessingml.document"
            )
          ) {
            this.workFileString = String(reader.result)
            this.newWorkUpload.hidden = false
            setTimeout(() => {
              this.newWorkUpload.hidden = true
            }, 2000)
          } else {
            this.addNotification(fileError)
          }
        },
        false
      )
      reader.readAsDataURL(this.workFile)
    } else {
      this.addNotification(fileError)
    }
  }

  public determineDragAndDropCapable() {
    // Complete guide to drag and drop files
    // https://serversideup.net/drag-and-drop-file-uploads-with-vuejs-and-axios/
    const div = document.createElement("div")
    return (
      ("draggable" in div || ("ondragstart" in div && "ondrop" in div)) &&
      "FormData" in window &&
      "FileReader" in window
    )
  }

  async mounted() {
    // Prepare the listeners ...
    this.dragAndDropCapable = this.determineDragAndDropCapable()
    if (this.dragAndDropCapable) {
      ;["dragover", "drop"].forEach((dragEvent) => {
        this.coverForm.addEventListener(
          dragEvent,
          function (event) {
            event.preventDefault()
            event.stopPropagation()
          },
          false
        )
        this.workForm.addEventListener(
          dragEvent,
          function (event) {
            event.preventDefault()
            event.stopPropagation()
          },
          false
        )
      })
      // Add an event listener for drop to the form
      this.coverForm.addEventListener("drop", (event) => {
        // Only grab the first file
        if (event.dataTransfer && event.dataTransfer.files.length) {
          this.coverFile = event.dataTransfer.files[0]
        }
      })
      this.workForm.addEventListener("drop", (event) => {
        if (event.dataTransfer && event.dataTransfer.files.length) {
          this.workFile = event.dataTransfer.files[0]
        }
      })
    }
    // Get any stored blobs and show them
    const workCover: string = (await idb.getPayload(
      "cover",
      this.conversionKey
    )) as string
    if (workCover) {
      this.coverFileString = workCover
      this.coverPreview.src = workCover
    }
    const workText = await idb.getPayload("docx", this.conversionKey)
    if (workText) {
      this.workFileString = workText as string
    }
  }

  async asyncData({ store, redirect }) {
    const hasConversion = await store.getters["conversions/conversionKey"]
    if (!hasConversion) {
      await store.commit("main/addNotification", {
        content: "You haven't described your work yet.",
        color: "error",
      })
      redirect("/convert/description")
    }
    await store.commit("conversions/setCurrentStep", "upload")
  }
}
</script>

<template>
  <div>
    <div
      class="card card-compact rounded-md bg-base-100 shadow-sm lg:mx-10 mb-4 -mt-4"
    >
      <div class="card-body">
        <div class="flex">
          <div>
            <p class="text-sm pb-1">
              There is no standard for cover size, dimensions or resolution
              required for an EPUB. We recommend an image (<span
                class="italic font-semibold"
                >.jpeg, .jpg or .png</span
              >) of 1,600 by 2,400 pixels, and less than 5Mb in size. Create
              your cover (or have someone create it for you) exactly as you wish
              it to appear. Nothing will be added, removed, or changed.
            </p>
            <p class="text-sm pb-3 font-semibold">
              Ensure you have appropriate rights to use your cover image, and
              acknowledge the creator as a contributor.
            </p>
            <nuxt-link
              class="flex flex-row text-woad-500 hover:text-woad-800 text-sm"
              to="/get-started"
            >
              <SvgIcon
                terms="h-5 w-5 inline-flex mr-1"
                icon="svgInformationCircle"
              />
              <p class="text-sm">Read the Guide to learn more.</p>
            </nuxt-link>
          </div>
          <SvgIcon
            terms="hidden px-2 sm:inline-flex sm:w-24 sm:h-36"
            icon="svgCoverAspectRatio"
          />
        </div>
      </div>
    </div>
    <ValidationObserver v-slot="{ invalid }">
      <div class="mx-auto lg:grid lg:grid-cols-3 lg:gap-2">
        <div class="relative lg:row-start-1 lg:col-start-3 lg:mt-6">
          <form ref="cover-form" @submit.prevent="submit">
            <div
              class="mx-auto relative flex flex-col justify-center m-1 w-60 h-96 bg-ochre-400 hover:bg-ochre-700 text-ochre-50 rounded-md filter drop-shadow-lg shadow transition ease-in duration-200"
            >
              <img
                v-show="coverFileString"
                ref="preview-cover"
                class="rounded-md object-cover object-center min-h-full min-w-full animate-fade-in"
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
            <!-- Call to action -->
            <div class="mt-8 max-w-2xl mx-auto flex justify-center">
              <button
                type="submit"
                :class="`btn-woad-extended ${invalid ? 'opacity-50' : ''}`"
                :disabled="invalid"
              >
                Next &#10230;
              </button>
            </div>
          </form>
        </div>
        <div class="lg:col-span-2">
          <form>
            <div class="grid grid-cols-1 gap-4 w-full">
              <!-- Contributor -->
              <label
                v-for="(contributor, i) in contributorList"
                :key="`contributor-${i}`"
                class="flex-auto block"
              >
                <span v-if="i == 0" class="text-ochre-600 text-xs ml-3"
                  >Contributor</span
                >
                <div class="flex flex-col">
                  <!-- Contributor Name -->
                  <div class="inpt-span">
                    <input
                      :id="`contributor-name-${i}`"
                      v-model="contributor.name"
                      type="text"
                      autocomplete="name"
                      class="inpt-text rounded-l-full"
                      placeholder="Artist, editor or translator who played a role in the creation of the work."
                    />
                  </div>
                  <div class="flex flex-row justify-between">
                    <!-- Contributor Role -->
                    <label class="flex-auto block mr-2 w-1/2 mt-1">
                      <span class="inpt-span">
                        <select
                          v-model="contributor.role"
                          class="inpt-text rounded-l-full"
                        >
                          <option disabled value="">Contributor role...</option>
                          <option
                            v-for="role in contributorRoleList"
                            :key="`contributor-${i}-${role.value}`"
                            :value="role.value"
                          >
                            {{ role.text }}
                          </option>
                        </select>
                      </span>
                    </label>
                    <!-- Contributor Year -->
                    <label class="flex-auto block ml-2 w-1/2 mt-1">
                      <span class="inpt-span">
                        <input
                          v-model="contributor.year"
                          type="text"
                          class="inpt-text rounded-l-full"
                          placeholder="Year of publication of work."
                      /></span>
                    </label>
                  </div>
                  <!-- Contributor Terms -->
                  <div class="flex mt-1">
                    <span class="inpt-span">
                      <input
                        :id="`contributor-${i}`"
                        v-model="contributor.terms"
                        type="text"
                        class="inpt-text rounded-l-full"
                        placeholder="Information about copyright held by the rights-holder and their terms-of-use."
                    /></span>
                    <button
                      v-show="contributorList.length > 1"
                      class="btn-sinopia-sm mt-3 ml-2"
                      @click.prevent="removeContributor(i)"
                    >
                      <SvgIcon terms="w-6 h-6 pr-1 pb-1" icon="svgMinus" />
                    </button>
                    <button
                      v-show="i === contributorList.length - 1"
                      class="btn-ochre-sm mt-3 ml-2"
                      @click.prevent="addContributor"
                    >
                      <SvgIcon terms="w-6 h-6 pr-1 pb-1" icon="svgPlus" />
                    </button>
                  </div>
                </div>
              </label>
              <div class="flex justify-between">
                <!-- Publisher -->
                <label class="flex-auto block mr-2">
                  <span class="text-ochre-600 text-xs ml-3">Publisher</span>
                  <span class="inpt-span">
                    <input
                      id="publisher"
                      v-model="work.publisher"
                      name="publisher"
                      type="text"
                      class="inpt-text rounded-l-full"
                      placeholder="Publisher of the creative work."
                  /></span>
                </label>
                <!-- Publisher URI -->
                <ValidationProvider v-slot="{ failedRules }" rules="url">
                  <label class="flex-auto block mr-2">
                    <span class="text-ochre-600 text-xs ml-3"
                      >Publisher website</span
                    >
                    <span class="inpt-span">
                      <SvgIcon
                        :terms="`inpt-icon ${
                          failedRules.url ? 'text-red-500' : 'text-ochre-400'
                        }`"
                        icon="svgLink" />
                      <input
                        id="publisher_uri"
                        v-model="work.publisher_uri"
                        name="publisher_uri"
                        type="url"
                        autocomplete="url"
                        class="inpt-text"
                        placeholder="Publisher's website."
                    /></span>
                  </label>
                </ValidationProvider>
              </div>
            </div>
          </form>
        </div>
      </div>
    </ValidationObserver>
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
import { IWorkMetadata, IContributorMetadata, IConversion } from "@/interfaces"
import { idb } from "@/api"

@Component({
  middleware: "refresh-authentication",
})
export default class UploadWork extends Vue {
  @Getter("conversions/conversionKey") conversionKey
  @Action("collections/storePayload") storePayload
  @Action("collections/storeCollectionPayload") storeConversionPayload
  @Action("conversions/updateConversionState") updateConversionState
  @Mutation("main/addNotification") addNotification
  @Ref("cover-form") readonly coverForm!: HTMLFormElement
  @Ref("preview-cover") readonly coverPreview!: HTMLImageElement
  @Ref("new-cover-uploaded") readonly newCoverUpload!: HTMLSpanElement
  public dragAndDropCapable: boolean = false
  public coverFile: File | null = null
  public coverFileString: string = ""
  public work: IWorkMetadata = {} as IWorkMetadata
  public conversion: IConversion = {} as IConversion
  public contributorList: IContributorMetadata[] = []
  public contributor_roles: string[] = ["artist", "editor", "translator"]
  public contributorRoleList: object[] = [
    {
      text: "Artist",
      value: "artist",
    },
    {
      text: "Editor",
      value: "editor",
    },
    {
      text: "Translator",
      value: "translator",
    },
  ]

  public addContributor(): void {
    const new_contributor: IContributorMetadata = {
      role: "artist",
      name: "",
      terms: "",
      year: "",
    }
    this.contributorList.push(new_contributor)
  }

  public removeContributor(contributor): void {
    if (this.contributorList.length > 1) {
      this.contributorList.splice(contributor, 1)
    }
  }

  public async submit(): Promise<void> {
    if (this.coverFileString) {
      // https://davidwalsh.name/javascript-clone-array
      if (this.contributorList.length) {
        // https://stackoverflow.com/a/46694321/295606
        this.work.contributor = this.contributorList.slice(0)
        // https://stackoverflow.com/a/18652793/295606
        this.work.contributor = this.work.contributor.filter(
          (contributor) => contributor.name !== ""
        )
      }
      // Update the conversion
      this.conversion.metadata = this.work
      // And can now save the conversion
      await this.storeConversionPayload({
        collection: "conversion",
        payload: this.conversion,
        key: this.work.identifier,
      })
      // Store coverFileString
      await this.storePayload({
        collection: "cover",
        payload: this.coverFileString,
        key: this.conversionKey,
      })
      // Update the conversion state
      await this.updateConversionState({
        conversionKey: this.conversionKey,
        conversionStep: "attribute",
      })
      if (
        this.$route.query &&
        Object.keys(this.$route.query).length !== 0 &&
        this.$route.query.constructor === Object
      ) {
        const query = Object.keys(this.$route.query)
          .map((key) => key + "=" + this.$route.query[key])
          .join("&")
        this.$router.push(`/write/convert?${query}`)
      } else this.$router.push("/write/convert")
    } else {
      this.addNotification({
        content: "Please upload a cover.",
        color: "error",
      })
    }
  }

  public coverFileUpload(event): void {
    if (event.target && event.target.files.length) {
      this.coverFile = event.target.files[0]
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
    // Saved exists
    // https://stackoverflow.com/a/53813384/295606
    this.conversion = (await idb.getPayload(
      "conversion",
      this.conversionKey
    )) as unknown as IConversion
    this.work = this.conversion.metadata
    // Ensure at least one contributor exists
    if (this.work.contributor && this.work.contributor.length) {
      this.work.contributor.forEach((c: IContributorMetadata) => {
        return this.contributorList.push({ ...c })
      })
    } else {
      this.addContributor()
    }
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
      })
      // Add an event listener for drop to the form
      this.coverForm.addEventListener("drop", (event) => {
        // Only grab the first file
        if (event.dataTransfer && event.dataTransfer.files.length) {
          this.coverFile = event.dataTransfer.files[0]
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
  }

  async asyncData({ store, redirect }) {
    const hasConversion = await store.getters["conversions/conversionKey"]
    if (!hasConversion) {
      await store.commit("main/addNotification", {
        content: "You haven't described your work yet.",
        color: "error",
      })
      redirect("/write/describe")
    }
    await store.commit("conversions/setCurrentStep", "attribute")
  }
}
</script>

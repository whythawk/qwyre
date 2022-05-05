<template>
  <div>
    <div
      class="card card-compact rounded-md bg-base-100 shadow-sm lg:mx-10 mb-4 -mt-4"
    >
      <div class="card-body">
        <div>
          <p v-if="isUpdate" class="text-sm pb-1">
            <span class="font-semibold">Update</span> your existing work either
            by importing a new <span class="italic font-semibold">.epub</span>
            or through the step-by-step epub creator.
          </p>
          <p class="text-sm pb-1">
            Your <span class="font-semibold">Word</span>
            <span class="italic font-semibold">.docx</span> text must be
            formatted with a header at the top of each chapter you want included
            in the table of contents.
          </p>
          <p class="text-sm pb-1">
            Don't include other structural formatting (such as page numbers,
            covers, copyright, or contents) as these will be created from the
            descriptive terms you provide below.
          </p>
        </div>
        <div class="flex justify-between">
          <nuxt-link
            class="flex flex-row text-woad-500 hover:text-woad-800 text-sm self-center"
            to="/get-started"
          >
            <SvgIcon
              terms="h-5 w-5 inline-flex mr-1"
              icon="svgInformationCircle"
            />
            <p class="text-sm">Read the Guide to learn more.</p>
          </nuxt-link>
          <div v-if="!isLoggedIn">
            <NuxtLink
              class="flex flex-row text-ochre-600 hover:text-ochre-800 text-sm"
              to="/login?next=convert"
            >
              <SvgIcon
                terms="h-5 w-5 inline-flex mr-1 flex-row"
                icon="svgUpload"
              />
              <p>
                <span class="font-semibold">Login </span>to import an existing
                <span class="italic">.epub</span> to publish on Qwyre.
              </p>
            </NuxtLink>
          </div>
          <div v-else class="ml-4 flex flex-row">
            <p class="text-sm text-ochre-600 mr-2 my-auto">
              If you have an existing <span class="italic">.epub</span> you want
              to publish on Qwyre
            </p>
            <CollectionsImportWork :work-id="workID" />
          </div>
        </div>
      </div>
    </div>
    <ValidationObserver v-slot="{ invalid }">
      <div class="lg:grid lg:grid-cols-3 lg:gap-2">
        <div class="relative lg:row-start-1 lg:col-start-3 lg:mt-6">
          <form ref="work-form" @submit.prevent="submit">
            <div
              class="mx-auto relative flex flex-col justify-center m-1 w-60 h-96 bg-woad-400 hover:bg-woad-700 text-ochre-50 rounded-md filter drop-shadow-lg shadow transition ease-in duration-200"
            >
              <img
                v-show="workFileString"
                class="rounded-md object-cover object-center min-h-full min-w-full animate-fade-in"
                src="/never-talk-to-strangers.jpg"
                alt=""
              />
              <label
                for="clickWorkUpload"
                class="absolute text-center text-lg bg-woad-600 bg-opacity-70 hover:bg-opacity-90 transition ease-in duration-200"
              >
                <span
                  ref="new-work-uploaded"
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
            <div class="mx-auto">
              <div class="grid grid-cols-1 gap-4 w-full">
                <!-- Title -->
                <ValidationProvider
                  v-slot="{ errors }"
                  immediate
                  rules="required"
                >
                  <label class="block">
                    <span class="text-ochre-600 text-xs ml-3">Title</span>
                    <span class="inpt-span">
                      <SvgIcon
                        :terms="`inpt-icon ${
                          errors[0] ? 'text-red-500' : 'text-ochre-400'
                        }`"
                        icon="svgExclamationCircle" />
                      <input
                        id="title"
                        v-model="work.title"
                        name="title"
                        type="text"
                        class="inpt-text"
                        placeholder="Title given to the creative work."
                    /></span>
                  </label>
                </ValidationProvider>
                <!-- Description -->
                <label class="block">
                  <span class="text-ochre-600 text-xs ml-3"
                    >Short description</span
                  >
                  <span class="inpt-span-area">
                    <!-- Block LastPass on TextArea https://github.com/mui-org/material-ui/issues/14860 -->
                    <textarea
                      id="description"
                      v-model="work.description"
                      name="description"
                      type="text"
                      class="inpt-textarea"
                      rows="1"
                      placeholder="A short, single-sentence summary of the creative work."
                      @change.stop
                    ></textarea>
                  </span>
                </label>
                <!-- Long description -->
                <label class="block">
                  <span class="text-ochre-600 text-xs ml-3"
                    >Long description</span
                  >
                  <span class="inpt-span-area">
                    <textarea
                      id="long_description"
                      v-model="work.long_description"
                      name="long_description"
                      type="text"
                      class="inpt-textarea"
                      rows="4"
                      placeholder="The pitch, or jacket-cover, description of the creative work."
                      @change.stop
                    ></textarea>
                  </span>
                </label>
                <!-- Creator -->
                <ValidationProvider
                  v-slot="{ errors }"
                  immediate
                  rules="required"
                >
                  <label
                    v-for="(creator, i) in creatorList"
                    :key="`creator-${i}`"
                    class="block"
                  >
                    <span v-if="i == 0" class="text-ochre-600 text-xs ml-3"
                      >Creator</span
                    >
                    <span class="flex mb-2">
                      <span class="inpt-span">
                        <SvgIcon
                          v-show="i == 0"
                          :terms="`inpt-icon ${
                            errors[0] ? 'text-red-500' : 'text-ochre-400'
                          }`"
                          icon="svgExclamationCircle" />
                        <input
                          :id="`creator-${i}`"
                          :key="`creator-${i}`"
                          v-model="creator.value"
                          type="text"
                          autocomplete="name"
                          :class="`inpt-text ${i > 0 ? 'rounded-l-full' : ''}`"
                          placeholder="The name of the work creator"
                      /></span>
                      <button
                        v-show="creatorList.length > 1"
                        class="btn-sinopia-sm mt-3 ml-2"
                        @click.prevent="removeCreator(i)"
                      >
                        <SvgIcon terms="w-6 h-6 pr-1 pb-1" icon="svgMinus" />
                      </button>
                      <button
                        v-show="i === creatorList.length - 1"
                        class="btn-ochre-sm mt-3 ml-2"
                        @click.prevent="addCreator"
                      >
                        <SvgIcon terms="w-6 h-6 pr-1 pb-1" icon="svgPlus" />
                      </button>
                    </span>
                  </label>
                </ValidationProvider>
                <!-- Subject -->
                <label class="block mt-2">
                  <span class="text-ochre-600 text-xs ml-3">Subject</span>
                  <div class="inpt-span-area bg-ochre-50">
                    <SvgIcon
                      terms="w-4 h-4 text-ochre-600 ml-2 mr-1 flex-none"
                      icon="svgTag"
                    />
                    <!-- button must be type button https://stackoverflow.com/a/44681697/295606 -->
                    <span class="flex flex-wrap">
                      <button
                        v-for="(sbjct, i) in subjectList"
                        :key="`subject-${i}`"
                        type="button"
                        class="sbjct-tag flex flex-row whitespace-nowrap"
                      >
                        <span>{{ sbjct }}</span>
                        <div @click.prevent="removeSubject(i)">
                          <SvgIcon terms="w-3 h-3 ml-2 mt-1" icon="svgX" />
                        </div>
                      </button>
                    </span>
                    <input
                      id="subject"
                      name="subject"
                      type="text"
                      class="inpt-textarea"
                      placeholder="Subjects, or tags, for the creative work. Comma or return separated."
                      @keydown.188="addSubject"
                      @keydown.enter="addSubject"
                      @keydown.delete="removeLastSubject"
                    />
                  </div>
                </label>
                <!-- Rights -->
                <label class="block">
                  <span class="text-ochre-600 text-xs ml-3">Rights</span>
                  <span class="inpt-span">
                    <input
                      id="rights"
                      v-model="work.rights"
                      name="rights"
                      type="text"
                      class="inpt-text rounded-l-full"
                      placeholder="A statement of copyright terms for the creative work, e.g. 'All rights reserved.'"
                  /></span>
                </label>
                <!-- Long rights -->
                <!-- <label class="block">
                <span class="text-ochre-600 text-xs ml-3">Long rights</span>
                <span class="inpt-span-area">
                  <textarea
                    id="long_rights"
                    v-model="work.long_rights"
                    name="long_rights"
                    type="text"
                    class="inpt-textarea"
                    rows="4"
                    placeholder="Information about copyright held in and over the creative work. Formatted as you wish it to appear."
                    @change.stop
                  ></textarea>
                </span>
              </label> -->
                <div class="flex justify-between">
                  <!-- Identifier/ISBN -->
                  <label class="flex-auto block mr-2">
                    <span class="text-ochre-600 text-xs ml-3">Identifier</span>
                    <span class="inpt-span">
                      <input
                        id="identifier"
                        v-model="work.identifier"
                        name="identifier"
                        type="text"
                        class="inpt-text rounded-l-full"
                        placeholder="UUID, DOI or ISBN of the creative work."
                    /></span>
                  </label>
                  <!-- Work URI -->
                  <ValidationProvider v-slot="{ failedRules }" rules="url">
                    <label class="flex-auto block mr-2">
                      <span class="text-ochre-600 text-xs ml-3"
                        >Work website</span
                      >
                      <span class="inpt-span">
                        <SvgIcon
                          :terms="`inpt-icon ${
                            failedRules.url ? 'text-red-500' : 'text-ochre-400'
                          }`"
                          icon="svgLink" />
                        <input
                          id="work_uri"
                          v-model="work.work_uri"
                          name="work_uri"
                          type="url"
                          autocomplete="url"
                          class="inpt-text"
                          placeholder="Website for the creative work."
                      /></span>
                    </label>
                  </ValidationProvider>
                </div>
                <div class="flex justify-between">
                  <!-- Date -->
                  <label class="flex-auto block mr-2 w-6/12">
                    <span class="text-ochre-600 text-xs ml-3"
                      >Date published</span
                    >
                    <span class="inpt-span">
                      <input
                        v-model="work.isodate"
                        type="date"
                        class="inpt-text rounded-l-full"
                    /></span>
                  </label>
                  <!-- Language -->
                  <label class="flex-auto block w-7/12">
                    <span class="text-ochre-600 text-xs ml-3">Language</span>
                    <span class="inpt-span">
                      <select
                        v-model="work.language"
                        class="inpt-text rounded-l-full"
                      >
                        <option disabled value="">Work language...</option>
                        <option
                          v-for="language in languageList"
                          :key="language.value"
                          :value="language.value"
                        >
                          {{ language.text }}
                        </option>
                      </select>
                    </span>
                  </label>
                </div>
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
  Action,
  Getter,
  Mutation,
  Watch,
  Ref,
} from "nuxt-property-decorator"
import { IWorkMetadata, IContributorMetadata, IConversion } from "@/interfaces"
import { generateUUID } from "@/utilities"
import { idb } from "@/api"
const getLanguages = (): Promise<
  {
    /* eslint-disable camelcase */
    text: string
    /* eslint-disable camelcase */
    value: string
  }[]
> => import("@/assets/json/iso639-1.json")

@Component({
  middleware: "refresh-authentication",
})
export default class CreateDescription extends Vue {
  @Getter("main/isLoggedIn") isLoggedIn
  @Getter("conversions/conversionKey") conversionKey
  @Mutation("conversions/setConversionKey") setConversionKey
  @Action("collections/replaceCollectionKey") replaceConversionKey
  @Action("collections/storeCollectionPayload") storeConversionPayload
  @Action("collections/storePayload") storePayload
  @Action("conversions/updateConversionState") updateConversionState
  @Mutation("main/addNotification") addNotification
  @Ref("work-form") readonly workForm!: HTMLFormElement
  @Ref("new-work-uploaded") readonly newWorkUpload!: HTMLSpanElement
  public workID: string = ""
  public isUpdate: boolean = false
  public dragAndDropCapable: boolean = false
  public workFile: File | null = null
  public workFileString: string = ""
  public work: IWorkMetadata = {
    title: "",
    creator: [],
  }

  public conversion: IConversion = {
    key: "",
    date_created: new Date(),
    metadata: this.work,
    dedication: "",
    conversionState: [],
  }

  public languageList: object[] = []
  public subjectList: string[] = []
  public creatorList: { value: string }[] = [{ value: "" }]

  public addCreator(): void {
    this.creatorList.push({ value: "" })
  }

  public removeCreator(creator): void {
    if (this.creatorList.length > 1) {
      this.creatorList.splice(creator, 1)
    }
  }

  public addSubject(event): void {
    // https://learnvue.co/2020/01/build-a-custom-vuejs-tag-input-in-under-10-minutes/
    event.preventDefault()
    const distinctSubject: string = event.target.value.trim()
    if (distinctSubject.length > 0) {
      this.subjectList.push(distinctSubject)
      // https://stackoverflow.com/a/1374131/295606
      this.subjectList = [...new Set(this.subjectList)]
      event.target.value = ""
    }
  }

  public removeSubject(subject): void {
    if (this.subjectList.length) {
      this.subjectList.splice(subject, 1)
    }
  }

  public removeLastSubject(subject): void {
    if (subject.target.value.length === 0 && this.subjectList.length) {
      this.removeSubject(this.subjectList.length - 1)
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

  public workFileUpload(event): void {
    if (event.target && event.target.files.length) {
      this.workFile = event.target.files[0]
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

  public async submit(): Promise<void> {
    this.work.subject = this.subjectList.slice(0)
    // validate
    if (
      this.creatorList.length &&
      this.creatorList[0].value !== "" &&
      this.work.title &&
      this.workFileString
    ) {
      if (this.creatorList.length) {
        // https://stackoverflow.com/a/46694321/295606
        this.work.creator = this.creatorList.map(({ value }) => value)
      }
      // Update the conversion
      this.conversion.metadata = this.work
      if (this.conversion.key !== this.work.identifier) {
        const checkKey: number = await idb.hasKey(
          "conversion",
          this.conversion.key
        )
        if (checkKey === 1)
          // First replace the key, then continue
          await this.replaceConversionKey({
            collection: "conversion",
            keyOld: this.conversion.key,
            keyNew: this.work.identifier,
          })
        this.conversion.key = this.work.identifier as string
      }
      // And can now save the conversion
      await this.storeConversionPayload({
        collection: "conversion",
        payload: this.conversion,
        key: this.work.identifier,
      })
      this.setConversionKey(this.conversion.key)
      // Store workFileString
      await this.storePayload({
        collection: "docx",
        payload: this.workFileString,
        key: this.conversionKey,
      })
      // Update the conversion state
      await this.updateConversionState({
        conversionKey: this.conversionKey,
        conversionStep: "describe",
      })
      if (
        this.$route.query &&
        Object.keys(this.$route.query).length !== 0 &&
        this.$route.query.constructor === Object
      ) {
        const query = Object.keys(this.$route.query)
          .map((key) => key + "=" + this.$route.query[key])
          .join("&")
        this.$router.push(`/write/attribute?${query}`)
      } else this.$router.push("/write/attribute")
    } else {
      this.addNotification({
        content: "Please complete all required fields.",
        color: "error",
      })
    }
  }

  public mountListeners() {
    // Prepare the listeners ...
    this.dragAndDropCapable = this.determineDragAndDropCapable()
    if (this.dragAndDropCapable) {
      ;["dragover", "drop"].forEach((dragEvent) => {
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
      this.workForm.addEventListener("drop", (event) => {
        if (event.dataTransfer && event.dataTransfer.files.length) {
          this.workFile = event.dataTransfer.files[0]
        }
      })
    }
  }

  public initialiseMetadata() {
    // Set work language
    // https://stackoverflow.com/a/26889118/295606
    if (!this.work.language) {
      if (process.browser) {
        this.work.language = window.navigator.languages
          ? window.navigator.languages[0].substring(0, 2)
          : this.$i18n.locale
      } else {
        this.work.language = this.$i18n.locale
      }
    }
    if (!this.work.identifier) {
      this.work.identifier = generateUUID()
    }
    // Set subjectList
    if (this.work.subject && this.work.subject.length) {
      this.subjectList = this.work.subject.slice(0)
    }
    // Set creators
    if (this.work.creator && this.work.creator.length) {
      this.creatorList = []
      this.work.creator.forEach((c: string) =>
        this.creatorList.push({ value: c })
      )
    }
  }

  public async initialiseSaved() {
    // Saved exists
    // https://stackoverflow.com/a/53813384/295606
    this.conversion = (await idb.getPayload(
      "conversion",
      this.conversionKey
    )) as unknown as IConversion
    this.work = this.conversion.metadata
    // Initialise saved work
    const workText = await idb.getPayload("docx", this.conversionKey)
    if (workText) {
      this.workFileString = workText as string
    }
    this.initialiseMetadata()
  }

  public async mounted(): Promise<void> {
    if (process.client) {
      let checkKey = 0
      if (this.conversionKey)
        checkKey = await idb.hasKey("conversion", this.conversionKey)
      if (checkKey === 1) await this.initialiseSaved()
      this.initialiseMetadata()
      this.mountListeners()
      if (
        this.$route.query &&
        Object.keys(this.$route.query).length !== 0 &&
        this.$route.query.constructor === Object &&
        Object.prototype.hasOwnProperty.call(this.$route.query, "work")
      ) {
        this.workID = this.$route.query.work as string
        this.isUpdate = true
      }
    }
  }

  async fetch() {
    this.languageList = await getLanguages()
  }

  async asyncData({ store }) {
    await store.commit("conversions/setCurrentStep", "describe")
  }
}
</script>

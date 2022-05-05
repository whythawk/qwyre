<template>
  <div>
    <div
      class="card card-compact rounded-md bg-base-100 shadow-sm lg:mx-10 mb-4 -mt-4"
    >
      <div class="card-body">
        <p class="text-sm pb-3">
          Review the information below before conversion. You can also choose to
          save it online to <span v-if="workID">update</span
          ><span v-else>publish</span> on Qwyre.
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
    </div>
    <div class="flex flex-wrap overflow-hidden">
      <div class="my-1 px-1 w-2/3 text-ochre-800">
        <!-- Description -->
        <h1 class="text-4xl font-medium">{{ work.title }}</h1>
        <p class="text-sm py-3">{{ workCreator }}</p>
        <div
          v-show="workDedication && !editDedication"
          class="text-sm py-3 font-light text-center italic"
        >
          <p
            v-for="(dedict, i) in drawWorkLines(workDedication)"
            :key="`dedication-${i}`"
            class="py-1"
          >
            {{ dedict }}
          </p>
        </div>
        <div
          v-show="!workDedication && !editDedication"
          class="text-sm py-3 font-light text-center italic"
        >
          <p>Dedicate your work. Optional, but appreciated.</p>
        </div>
        <form>
          <div v-if="editDedication" class="max-w-2xl mx-auto">
            <div class="grid grid-cols-1 gap-4 w-full">
              <!-- Dedication -->
              <label class="block">
                <span class="text-ochre-600 text-xs ml-3">Dedication</span>
                <span class="inpt-span-area">
                  <!-- Block LastPass on TextArea https://github.com/mui-org/material-ui/issues/14860 -->
                  <textarea
                    id="dedication_text"
                    v-model="workDedication"
                    name="dedication_text"
                    type="text"
                    class="inpt-textarea"
                    rows="4"
                    placeholder="Dedicate your work. Optional, but appreciated."
                    @change.stop
                  ></textarea>
                </span>
              </label>
            </div>
          </div>
          <!-- Call to action -->
          <div v-if="editDedication" class="max-w-2xl flex mx-auto justify-end">
            <button
              class="btn-sinopia-sm mt-3 ml-2"
              @click.prevent="editDedication = !editDedication"
            >
              <SvgIcon terms="w-6 h-6 pr-1 pb-1" icon="svgMinus" />
            </button>
            <button
              class="btn-woad-sm mt-3 ml-2"
              @click.prevent="addDedication"
            >
              <SvgIcon terms="w-6 h-6 pr-1 pb-1" icon="svgPlus" />
            </button>
          </div>
          <div v-else class="max-w-2xl flex mx-auto justify-center">
            <button
              class="btn-ochre-sm mb-2"
              @click.prevent="editDedication = !editDedication"
            >
              <SvgIcon terms="w-6 h-6 pr-1 pb-1" icon="svgPencilAlt" />
            </button>
          </div>
        </form>
        <p v-show="work.description" class="text-sm py-2 font-bold">
          {{ work.description }}
        </p>
        <div v-show="work.long_description" class="py-1 space-y-1 text-sm">
          <p
            v-for="(descript, i) in drawWorkLines(work.long_description)"
            :key="`long-description-${i}`"
          >
            {{ descript }}
          </p>
        </div>
        <!-- General metadata table -->
        <table class="table-fixed text-sm w-full">
          <thead>
            <tr>
              <th class="w-1/3"></th>
              <th class="w-2/3"></th>
            </tr>
          </thead>
          <tbody>
            <tr v-show="work.isodate">
              <td class="font-semibold py-2">Published</td>
              <td class="text-right py-2">{{ work.isodate }}</td>
            </tr>
            <tr v-show="work.identifier">
              <td class="font-semibold py-2">Identifier (ISBN, UUID)</td>
              <td class="text-right py-2">
                {{ work.identifier }}
              </td>
            </tr>
            <tr v-show="work.language">
              <td class="font-semibold py-2">Language</td>
              <td class="text-right py-2">{{ work.language }}</td>
            </tr>
            <tr v-show="work.subject && work.subject.length">
              <td class="font-semibold py-2">Subject</td>
              <td class="text-right py-2">{{ workSubject }}</td>
            </tr>
            <tr v-show="work.publisher">
              <td class="font-semibold py-2">Publisher</td>
              <td v-if="work.publisher_url" class="text-right py-2">
                <a :href="work.publisher_url">{{ work.publisher }}</a>
              </td>
              <td v-else class="text-right py-2">
                {{ work.publisher }}
              </td>
            </tr>
          </tbody>
        </table>
        <!-- Publication Rights -->
        <p v-show="work.rights" class="text-xs py-2 italic">
          {{ work.rights }}
        </p>
        <div v-show="work.long_rights" class="py-1">
          <p
            v-for="(right, i) in drawWorkLines(work.long_rights)"
            :key="`long-rights-${i}`"
            class="text-xs py-1"
          >
            {{ right }}
          </p>
        </div>
        <!-- Contributors -->
        <div
          v-show="
            work.contributor &&
            work.contributor.length &&
            work.contributor[0].name
          "
        >
          <p class="text-lg font-semibold">Contributors</p>
          <table
            v-for="(contributor, i) in work.contributor"
            :key="`contributor-table-${i}`"
            class="table-fixed text-sm w-full mt-2"
          >
            <thead>
              <tr>
                <th class="w-1/3"></th>
                <th class="w-2/3"></th>
              </tr>
            </thead>
            <tbody>
              <tr v-show="contributor.name">
                <td class="font-semibold py-0">Name</td>
                <td class="text-right py-0">{{ contributor.name }}</td>
              </tr>
              <tr v-show="contributor.role">
                <td class="font-semibold py-0">Role</td>
                <td class="text-right py-0">{{ contributor.role }}</td>
              </tr>
              <tr v-show="contributor.year">
                <td class="font-semibold py-0">Year</td>
                <td class="text-right py-0">{{ contributor.year }}</td>
              </tr>
              <tr v-show="contributor.terms">
                <td class="font-semibold py-0">Terms</td>
                <td class="text-right py-0">{{ contributor.terms }}</td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
      <div class="my-1 px-1 w-1/3 flex flex-col">
        <!-- Cover -->
        <div
          class="relative mx-auto my-5 w-60 h-96 filter drop-shadow-lg shadow transition ease-in duration-200"
        >
          <img
            :src="workCover"
            class="object-cover object-center min-h-full min-w-full animate-fade-in rounded-lg"
          />
        </div>
        <!-- WorkDOCX -->
        <div
          class="mx-auto mb-5 text-xs p-2 bg-ochre-100 filter drop-shadow-lg shadow transition ease-in duration-200"
        >
          <a
            :href="workText"
            :download="workDOCX"
            type="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
          >
            <SvgIcon terms="w-6 h-4 inline-block" icon="logoDocx" />
            <span>{{ workDOCX }}</span>
          </a>
        </div>
        <!-- WorkEPUB -->
        <div
          v-if="convertState === 'complete'"
          class="mx-auto mb-5 text-xs p-2 bg-ochre-100 filter drop-shadow-lg shadow transition ease-in duration-200"
        >
          <a
            :href="convertEPUB"
            :download="workEPUB"
            type="application/epub+zip"
          >
            <SvgIcon
              terms="w-6 h-4 inline-block mr-1 text-malachite-400"
              icon="logoEPUB"
            />
            <span>{{ workEPUB }}</span>
          </a>
        </div>
        <!-- Call to action -->
        <div class="mt-8 flex mx-auto justify-center">
          <div
            v-if="isLoggedIn && convertState !== 'complete'"
            class="relative flex items-start"
          >
            <div class="flex items-center h-5">
              <input
                id="saveWork"
                v-model="saveWork"
                aria-describedby="store-description"
                name="saveWork"
                type="checkbox"
                class="focus:ring-woad-500 h-4 w-4 text-woad-600 border-gray-300 rounded"
              />
            </div>
            <div class="ml-3 text-sm">
              <label for="saveWork" class="font-medium text-gray-700"
                >Save online</label
              >
              <span id="store-description" class="text-gray-500"
                ><span class="sr-only">Save online </span>to
                <span v-if="workID">update</span><span v-else>publish</span> on
                Qwyre.</span
              >
            </div>
          </div>
          <div
            v-if="!isLoggedIn && convertState !== 'complete'"
            class="relative flex items-start"
          >
            <NuxtLink class="ml-3 text-sm" to="/login?next=convert">
              <span class="text-gray-500 hover:text-ochre-500"
                ><span class="font-semibold">Login </span>to
                <span v-if="workID">update</span><span v-else>publish</span> on
                Qwyre.</span
              >
            </NuxtLink>
          </div>
        </div>
        <div class="mt-2 max-w-2xl flex mx-auto justify-center">
          <button
            v-if="convertState === 'waiting'"
            type="submit"
            class="btn-woad-extended mt-4"
            @click.prevent="submit"
          >
            Convert &#10230;
          </button>
          <button
            v-if="convertState === 'converting'"
            type="submit"
            class="btn-woad-extended mt-4 opacity-50"
            disabled
          >
            <SvgIcon terms="w-8 h-8" icon="svgRingsSpinner" />
          </button>
          <button
            v-if="convertState === 'complete' && !saveWorkIdentifier"
            type="submit"
            class="btn-malachite-extended"
            disabled
          >
            <SvgIcon terms="w-5 h-4 inline-block mr-1" icon="logoEPUB" />
            <span>Complete</span>
          </button>
          <!-- Next to Review -->
          <button
            v-if="convertState === 'complete' && saveWorkIdentifier"
            type="submit"
            class="btn-woad-extended"
            @click.prevent="redirectReview"
          >
            Next &#10230;
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script lang="ts">
import {
  Component,
  mixins,
  Action,
  Getter,
  Mutation,
} from "nuxt-property-decorator"
import WebSocketAsPromised from "websocket-as-promised"
import { IConversion, IKeyable, IWorkMetadata } from "@/interfaces"
import { ISocketResponse } from "@/interfaces/utilities"
import { idb } from "@/api"
import importWorkData from "@/mixins/importWorkData"

@Component({
  middleware: "refresh-authentication",
})
export default class ConvertWork extends mixins(importWorkData) {
  @Getter("conversions/conversionKey") conversionKey
  @Action("collections/storePayload") storePayload
  @Action("collections/storeCollectionPayload") storeConversionPayload
  @Action("conversions/updateConversionState") updateConversionState
  @Mutation("main/addNotification") addNotification
  @Getter("main/isLoggedIn") isLoggedIn
  @Action("conversions/buildWorkMetadata") buildWorkMetadata
  public workID: string = ""
  public convertState: string = "waiting"
  public convertEPUB: string | null = null
  public conversion: IConversion = {} as IConversion
  public work: IWorkMetadata = {
    title: "",
    creator: [""],
  }

  public workCover: string = ""
  public workText: string = ""
  public workDedication: string = ""
  public editDedication: boolean = true
  public saveWork: boolean = false
  public saveWorkIdentifier: string = ""

  public async addDedication(): Promise<void> {
    ;(this.conversion as IConversion).dedication = this.workDedication
    await this.storeConversionPayload({
      collection: "conversion",
      payload: this.conversion,
      key: this.conversionKey,
    })
    this.editDedication = false
  }

  public wsp = new WebSocketAsPromised(
    `${process.env.apiWS}/api/v1/works/create`,
    {
      packMessage: (data) => JSON.stringify(data),
      unpackMessage: (data) => JSON.parse(data as string),
    }
  )

  async created(): Promise<void> {
    // Get the conversion
    // https://stackoverflow.com/a/53813384/295606
    this.conversion = (await idb.getPayload(
      "conversion",
      this.conversionKey
    )) as unknown as IConversion
    this.work = this.conversion.metadata
    this.workDedication = this.conversion.dedication
    if (this.workDedication) this.editDedication = false
    // Cover and Text
    this.workCover = (await idb.getPayload(
      "cover",
      this.conversionKey
    )) as string
    this.workText = (await idb.getPayload("docx", this.conversionKey)) as string
    if (
      this.$route.query &&
      Object.keys(this.$route.query).length !== 0 &&
      this.$route.query.constructor === Object &&
      Object.prototype.hasOwnProperty.call(this.$route.query, "work")
    ) {
      this.workID = this.$route.query.work as string
      this.saveWork = true
    }
    if (process.client) {
      this.wsp.open()
      this.wsp.onUnpackedMessage.addListener((data) =>
        this.convertSocketResponse(data)
      )
    }
  }

  public submit(): void {
    const token = (this as any).$cookies.get("token")
      ? (this as any).$cookies.get("token")
      : ""
    const jsonData: IKeyable = {
      metadata: {} as IKeyable,
      cover: "" as string,
      text: "" as string,
      dedication: null as string[] | null,
      token,
      save: false,
      workID: null,
    }
    jsonData.metadata = JSON.parse(JSON.stringify(this.work)) as IKeyable
    jsonData.cover = this.workCover
    jsonData.text = this.workText
    jsonData.dedication =
      this.workDedication === ""
        ? null
        : this.drawWorkLines(this.workDedication)
    if (token && this.saveWork) {
      jsonData.save = this.saveWork
    }
    if (this.workID && this.saveWork) {
      jsonData.workID = this.workID
    }
    this.wsp
      .open()
      .then(() => {
        this.wsp.sendPacked(jsonData)
        this.convertState = "converting"
        const sendingNotification = {
          content: "Uploading convert...",
          showProgress: true,
        }
        this.addNotification(sendingNotification)
      })
      .catch((e) => console.error(e))
  }

  public redirectReview() {
    if (this.saveWork && this.saveWorkIdentifier)
      this.$router.push(`/workshop/${this.saveWorkIdentifier}`)
  }

  public async convertSocketResponse(
    convertResponse: ISocketResponse
  ): Promise<void> {
    if (
      !this.work.identifier &&
      Object.prototype.hasOwnProperty.call(
        convertResponse.data,
        "identifier"
      ) &&
      (convertResponse.data as any).identifier
    ) {
      this.work.identifier = (convertResponse.data as any).identifier as string
      // await this.storeWorkMetadata(this.work)
    }
    if (convertResponse.state === "converting") {
      this.convertState = "converting"
      this.addNotification({
        content: `converting '${this.workEPUB}'...`,
        showProgress: true,
      })
    }
    if (convertResponse.state === "complete") {
      this.addNotification({
        content: "Conversion complete.",
        color: "success",
      })
      this.convertState = "complete"
      // Save epub and update conversion
      this.convertEPUB = (convertResponse.data as any).work as string
      const epubFile = await this.getFileFromBase64(
        this.convertEPUB,
        this.workEPUB,
        "application/epub+zip"
      )
      this.storeWork(epubFile)
      await this.storeConversionPayload({
        collection: "conversion",
        payload: this.conversion,
        key: this.conversionKey,
      })
      // Update the conversion state
      await this.updateConversionState({
        conversionKey: this.conversionKey,
        conversionStep: "convert",
      })
      // Get the redirect-to-review work identifier
      if (this.saveWork && (convertResponse.data as any).workIdentifier)
        this.saveWorkIdentifier = (convertResponse.data as any)
          .workIdentifier as string
      return this.download(
        this.convertEPUB,
        this.workEPUB,
        "application/epub+zip"
      )
    }
  }

  public download(content, fileName, contentType) {
    // https://stackoverflow.com/a/18197341/295606
    const a = document.createElement("a")
    a.href = content
    a.download = fileName
    a.type = contentType
    a.style.display = "none"
    document.body.appendChild(a)
    a.click()
    document.body.removeChild(a)
  }

  public get workName() {
    return this.work.title.toLowerCase().split(" ").join("-")
  }

  public get workEPUB() {
    return this.workName + ".epub"
  }

  public get workDOCX() {
    return this.workName + ".docx"
  }

  public get workCreator() {
    if (this.work.creator && this.work.creator.length > 1) {
      return [
        this.work.creator.slice(0, -1).join(", "),
        this.work.creator.slice(-1),
      ].join(" & ")
    } else {
      return this.work.creator[0]
    }
  }

  public get workSubject() {
    if (this.work.subject) return this.work.subject.join(", ")
    else return ""
  }

  public drawWorkMarkup(text: string) {
    return `<p>${this.drawWorkLines(text).join("</p><p>")}</p>`
  }

  public drawWorkLines(text: string) {
    if (text) {
      return text
        .replace(/\r/g, "")
        .split(/\n/)
        .filter((n) => n)
    } else {
      return [text]
    }
  }

  async asyncData({ store, redirect }): Promise<void> {
    const cKey = await store.getters["conversions/conversionKey"]
    let sameKeys = false
    if (cKey) {
      let [iKey, dKey] = [0, 0]
      if (cKey) iKey = await idb.hasKey("cover", cKey)
      if (cKey) dKey = await idb.hasKey("docx", cKey)
      sameKeys = [1, iKey, dKey].every((val, _i, arr) => val === arr[0])
    }
    if (!cKey) {
      await store.commit("main/addNotification", {
        content: "You haven't imported your work yet.",
        color: "error",
      })
      redirect("/write/describe")
    }
    if (!sameKeys) {
      await store.commit("main/addNotification", {
        content: "You haven't imported your cover yet.",
        color: "error",
      })
      redirect("/write/attribute")
    }
    await store.commit("conversions/setCurrentStep", "convert")
  }
}
</script>

<template>
  <div class="flex flex-wrap overflow-hidden">
    <div class="my-1 px-1 w-2/3 text-ochre-800">
      <!-- Description -->
      <h1 class="text-4xl font-medium">{{ work.title }}</h1>
      <p class="text-sm py-3">{{ workCreator }}</p>
      <div
        v-show="workDedication"
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
      <p v-show="work.description" class="text-sm py-2 font-bold">
        {{ work.description }}
      </p>
      <div v-show="work.long_description" class="py-1">
        <p
          v-for="(descript, i) in drawWorkLines(work.long_description)"
          :key="`long-description-${i}`"
          class="text-sm py-1"
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
        <a :href="convertEPUB" :download="workEPUB" type="application/epub+zip">
          <SvgIcon
            terms="w-6 h-4 inline-block mr-1 text-malachite-400"
            icon="logoEPUB"
          />
          <span>{{ workEPUB }}</span>
        </a>
      </div>
      <!-- Call to action -->
      <div class="mt-8 max-w-2xl flex mx-auto justify-center">
        <button
          v-if="convertState === 'waiting'"
          type="submit"
          class="btn-woad-extended mt-4"
          @click.prevent="submit"
        >
          <SvgIcon terms="w-5 h-4 inline-block mr-1" icon="svgReturn" />
          <span>convert your work</span>
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
          v-if="convertState === 'complete'"
          type="submit"
          class="btn-malachite-extended mt-4"
          disabled
        >
          <SvgIcon terms="w-5 h-4 inline-block mr-1" icon="logoEPUB" />
          <span>convert complete</span>
        </button>
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
import { IConversion, IWorkMetadata } from "@/interfaces"
import { SocketResponse } from "@/interfaces/utilities"
import { idb } from "@/api"
import importWorkData from "@/mixins/importWorkData"

@Component
export default class ConvertWork extends mixins(importWorkData) {
  @Getter("conversions/conversionKey") conversionKey
  @Action("collections/storePayload") storePayload
  @Action("collections/storeCollectionPayload") storeConversionPayload
  @Mutation("main/addNotification") addNotification

  @Action("conversions/buildWorkMetadata") buildWorkMetadata
  public conversion: string | IConversion = ""
  public convertState: string = "waiting"
  public convertEPUB: string | null = null
  public work: IWorkMetadata = {
    title: "",
    creator: [""],
  }

  public workCover: string = ""
  public workText: string = ""
  public workDedication: string = ""

  public wsp = new WebSocketAsPromised(
    `${process.env.apiWS}/api/v1/chapisha/build`,
    {
      packMessage: (data) => JSON.stringify(data),
      unpackMessage: (data) => JSON.parse(data as string),
    }
  )

  async created(): Promise<void> {
    // Get the conversion
    // https://stackoverflow.com/a/53813384/295606
    this.conversion = ((await idb.getPayload(
      "conversion",
      this.conversionKey
    )) as unknown) as IConversion
    this.work = this.conversion.metadata
    this.workDedication = this.conversion.dedication
    // Cover and Text
    this.workCover = (await idb.getPayload(
      "cover",
      this.conversionKey
    )) as string
    this.workText = (await idb.getPayload("docx", this.conversionKey)) as string
    if (process.client) {
      this.wsp.open()
      this.wsp.onUnpackedMessage.addListener((data) =>
        this.convertSocketResponse(data)
      )
    }
  }

  public submit(): void {
    // await this.buildWorkMetadata()
    const jsonData = {
      metadata: this.work,
      cover: this.workCover,
      text: this.workText,
      dedication: this.workDedication === "" ? null : this.workDedication,
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

  public async convertSocketResponse(
    convertResponse: SocketResponse
  ): Promise<void> {
    if (!this.work.identifier && convertResponse.data.identifier) {
      this.work.identifier = convertResponse.data.identifier as string
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
        content: "convert complete.",
        color: "success",
      })
      this.convertState = "complete"
      // Save epub and update conversion
      this.convertEPUB = convertResponse.data.work as string
      const epubFile = await this.getFileFromBase64(
        this.convertEPUB,
        this.workEPUB,
        "application/epub+zip"
      )
      this.storeWork(epubFile)
      // await this.storePayload({
      //  collection: "epub",
      //  payload: this.convertEPUB,
      //  key: this.conversionKey,
      // })
      ;(this.conversion as IConversion).conversionState.conversion = true
      await this.storeConversionPayload({
        collection: "conversion",
        payload: this.conversion,
        key: this.conversionKey,
      })
      return this.download(
        this.convertEPUB,
        this.workEPUB,
        "application/epub+zip"
      )
    }
  }

  public download(content, fileName, contentType) {
    const a = document.createElement("a")
    const file = new Blob([content], { type: contentType })
    a.href = URL.createObjectURL(file)
    a.download = fileName
    a.click()
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
    const creator = this.work.creator
    if (creator.length > 1) {
      return [creator.slice(0, -1).join(", "), creator.slice(-1)].join(" & ")
    } else {
      return creator[0]
    }
  }

  public get workSubject() {
    if (this.work.subject) return this.work.subject.join(", ")
    else return ""
  }

  public drawWorkLines(text: string) {
    if (text) {
      return text.replace(/\r/g, "").split(/\n/)
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
        content: "You haven't described your work yet.",
        color: "error",
      })
      redirect("/convert/description")
    }
    if (!sameKeys) {
      await store.commit("main/addNotification", {
        content: "You haven't uploaded your work yet.",
        color: "error",
      })
      redirect("/convert/upload")
    }
    await store.commit("conversions/setCurrentStep", "conversion")
  }
}
</script>

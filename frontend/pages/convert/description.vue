<template>
  <div class="flex-auto">
    <p class="pb-1">
      The terms you use to describe your work are called metadata and are
      defined by international convention. Dublin Core is a vocabulary of
      fifteen properties for use in resource description. In epubs, four of them
      - title, identifier, language and rights - are required.
    </p>
    <p class="py-1">
      Qwyre will automatically provide an identifier and default language and
      rights, but only you can know your title. Your name, as creator, is also
      enforced.
    </p>
    <p class="py-1">
      The more information you can include the better since these data are
      stored in your epub and used by the distribution platforms you are likely
      to release your work on to help readers search for something to read.
    </p>
    <nuxt-link
      class="flex flex-row text-woad-500 underline pt-1"
      to="/get-started"
    >
      <SvgIcon terms="h-6 w-6 inline-flex" icon="svgInformationCircle" />
      <p>Read the Guide for more details...</p>
    </nuxt-link>
    <ValidationObserver v-slot="{ invalid }">
      <form @submit.prevent="submit">
        <div class="mt-8 max-w-2xl mx-auto">
          <div class="grid grid-cols-1 gap-4 w-full">
            <!-- Title -->
            <ValidationProvider v-slot="{ errors }" immediate rules="required">
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
              <span class="text-ochre-600 text-xs ml-3">Short description</span>
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
              <span class="text-ochre-600 text-xs ml-3">Long description</span>
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
            <ValidationProvider v-slot="{ errors }" immediate rules="required">
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
                  placeholder="A short statement of copyright terms for the creative work, e.g. 'All rights reserved.'"
              /></span>
            </label>
            <!-- Long rights -->
            <label class="block">
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
            </label>
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
                  <span class="text-ochre-600 text-xs ml-3">Work website</span>
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
                <span class="text-ochre-600 text-xs ml-3">Date published</span>
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
            <!-- Contributor -->
            <label
              v-for="(contributor, i) in contributorList"
              :key="`contributor-${i}`"
              class="block"
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
          </div>
        </div>
        <!-- Call to action -->
        <div class="mt-8 max-w-2xl mx-auto flex justify-center">
          <button
            type="submit"
            :class="`btn-woad-extended ${invalid ? 'opacity-50' : ''}`"
            :disabled="invalid"
          >
            <SvgIcon terms="w-5 h-4 inline-block mr-1" icon="svgReturn" />
            <span>Store description</span>
          </button>
        </div>
      </form>
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

@Component
export default class CreateDescription extends Vue {
  @Getter("conversions/conversionKey") conversionKey
  @Mutation("conversions/setConversionKey") setConversionKey
  @Action("collections/replaceCollectionKey") replaceConversionKey
  @Action("collections/storeCollectionPayload") storeConversionPayload
  @Mutation("main/addNotification") addNotification
  public work: IWorkMetadata = {
    title: "",
    creator: [""],
  }

  public conversion: IConversion = {
    key: "",
    date_created: new Date(),
    metadata: this.work,
    dedication: "",
    conversionState: {
      description: false,
      upload: false,
      dedication: false,
      conversion: false,
    },
  }

  public languageList: object[] = []
  public subjectList: string[] = []
  public creatorList: { value: string }[] = []
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

  public addCreator(): void {
    this.creatorList.push({ value: "" })
  }

  public removeCreator(creator): void {
    if (this.creatorList.length > 1) {
      this.creatorList.splice(creator, 1)
    }
  }

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

  async created(): Promise<void> {
    let checkKey: number = 0
    if (this.conversionKey)
      checkKey = await idb.hasKey("conversion", this.conversionKey)
    // Set description to work
    if (checkKey === 1) {
      // https://stackoverflow.com/a/53813384/295606
      this.conversion = ((await idb.getPayload(
        "conversion",
        this.conversionKey
      )) as unknown) as IConversion
      this.work = this.conversion.metadata
    }
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
    // Ensure at least one contributor exists
    if (this.work.contributor && this.work.contributor.length) {
      this.work.contributor.forEach((c: IContributorMetadata) => {
        return this.contributorList.push({ ...c })
      })
    } else {
      this.addContributor()
    }
    // Ensure at least one creator exists
    if (this.work && this.work.creator.length) {
      this.work.creator.forEach((c: string) =>
        this.creatorList.push({ value: c })
      )
    } else {
      this.addCreator()
    }
  }

  public async submit(): Promise<void> {
    this.work.subject = this.subjectList.slice(0)
    // validate
    if (
      this.creatorList.length &&
      this.creatorList[0].value !== "" &&
      this.work.title
    ) {
      if (this.creatorList.length) {
        // https://stackoverflow.com/a/46694321/295606
        this.work.creator = this.creatorList.map(({ value }) => value)
      }
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
      this.conversion.conversionState.description = true
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
      this.$router.push("/convert/upload")
    } else {
      this.addNotification({
        content: "Please complete all required fields.",
        color: "error",
      })
    }
  }

  async fetch() {
    this.languageList = await getLanguages()
  }

  async asyncData({ store }) {
    await store.commit("conversions/setCurrentStep", "description")
  }
}
</script>

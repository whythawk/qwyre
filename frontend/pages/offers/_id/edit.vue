<template>
  <div class="container min-h-screen mx-auto flex flex-col">
    <TitleBar title="Edit Offer" />
    <div class="max-w-2xl mx-auto flex justify-between p-3 space-x-3">
      <div class="flex-1 line-clamp-5">
        <h3 class="mt-1 text-gray-900 text-sm font-semibold truncate">
          {{ workEdit.metadata.title }}
        </h3>
        <p class="mt-1 text-gray-500 text-sm italic">
          {{ creatorName }}
        </p>
        <p class="mt-1 text-gray-500 text-sm line-clamp-5">
          {{ workEdit.metadata.description }}
        </p>
        <NuxtLink
          :to="`/workshop/${workEdit.metadata.identifier}`"
          class="
            relative
            flex-1
            inline-flex
            items-center
            justify-center
            pt-4
            text-sm text-gray-700
            font-medium
            border border-transparent
            rounded-br-lg
            hover:text-gray-500
          "
        >
          <SvgIcon terms="w-5 h-5 text-gray-400" icon="svgPencilAlt" />
          <span class="ml-3">Return to review</span>
        </NuxtLink>
      </div>
      <SourcesCoverImage :src="cover.data" />
    </div>
    <div v-if="canMakeCreativeOffers">
      <form @submit.prevent="submit">
        <div class="mt-8 max-w-2xl mx-auto">
          <div class="grid grid-cols-1 gap-4 w-full">
            <!-- Description -->
            <label class="block">
              <span class="text-ochre-600 text-xs ml-3">Offer description</span>
              <span class="inpt-span-area">
                <!-- Block LastPass on TextArea https://github.com/mui-org/material-ui/issues/14860 -->
                <textarea
                  id="description"
                  v-model="contractUpdate.description"
                  name="description"
                  type="text"
                  class="inpt-textarea"
                  rows="5"
                  placeholder="Describe your offer, and make a pitch as for why someone should edit your work."
                  @change.stop
                ></textarea>
              </span>
            </label>
            <div class="grid grid-cols-2 gap-4 w-full">
              <!-- Creator Proportion -->
              <span class="text-ochre-600 font-semibold ml-3 my-auto"
                >Creator [<NuxtLink
                  :to="`/creator/${creatorProfile.identifier}`"
                  class="underline"
                  >{{ creatorName }}</NuxtLink
                >]</span
              >
              <label class="flex-auto block mr-2">
                <span class="text-ochre-600 text-xs ml-3"
                  >Creator proportion</span
                >
                <span class="inpt-span">
                  <SvgIcon
                    :terms="`inpt-icon ${
                      validateProportions
                        ? 'text-ochre-500'
                        : 'text-sinopia-400'
                    }`"
                    icon="svgExclamationCircle" />
                  <input
                    id="creator-proportion"
                    v-model="creatorProportion"
                    name="creator-proportion"
                    type="text"
                    class="inpt-text"
                    placeholder="Revenue share. Must add up to 100."
                /></span>
              </label>
              <!-- Parties -->
              <span
                v-if="editorLink"
                class="text-ochre-600 font-semibold ml-3 my-auto"
                >Editor [<NuxtLink
                  :to="`/creator/${editorLink}`"
                  class="underline"
                  >{{ creatorName }}</NuxtLink
                >]</span
              >
              <span v-else class="text-ochre-600 font-semibold ml-3 my-auto"
                >Editor</span
              >
              <label class="flex-auto block mr-2">
                <span class="text-ochre-600 text-xs ml-3"
                  >Editor proportion</span
                >
                <span class="inpt-span">
                  <input
                    id="editor-proportion"
                    v-model="editorProportion"
                    name="editor-proportion"
                    type="text"
                    class="inpt-text rounded-l-full"
                    placeholder="Revenue share. Must add up to 100."
                /></span>
              </label>
            </div>
          </div>
        </div>
        <!-- Call to action -->
        <div class="mt-8 max-w-2xl mx-auto flex justify-center">
          <button
            type="submit"
            class="btn-woad-extended flex items-center"
            @click.prevent="submit"
          >
            <SvgIcon terms="w-5 h-4 inline-block mr-1" icon="svgReturn" />
            <span>Save</span>
          </button>
        </div>
      </form>
    </div>
    <div v-else>
      <p>
        Before you can offer your work, you'll need to complete a few tasks:
      </p>
      <p v-if="!userProfile.email_validated">
        Validate your email, or - if you prefer to use a different email address
        - update your profile.
      </p>
      <CreatorValidateEmailButton />
      <p v-if="creatorProfile.isPrivate">
        You are welcome to remain anonymous, but you'll need to publish your
        profile before others can see your offers.
      </p>
    </div>
  </div>
</template>

<script lang="ts">
import { Component, Action, Getter, Vue } from "nuxt-property-decorator"
import { api } from "@/api"
import {
  IContractCreate,
  IContractUpdate,
  IPartyCreate,
  IPartyUpdate,
  IDataSource,
} from "@/interfaces"

@Component({
  layout: "working",
  middleware: "authenticated",
})
export default class EditOffer extends Vue {
  @Action("conversions/getWorkToEdit") getWorkToEdit
  @Action("conversions/getContractToEdit") getContractToEdit
  @Action("conversions/createWorkContract") createWorkContract
  @Action("conversions/updateWorkContract") updateWorkContract
  @Getter("conversions/workEdit") workEdit
  @Getter("conversions/contractEdit") contractEdit
  @Getter("main/creatorProfile") creatorProfile
  @Getter("main/userProfile") userProfile
  @Getter("main/canMakeCreativeOffers") canMakeCreativeOffers
  public toUpdate: boolean = false
  public cover: IDataSource = {} as IDataSource
  public creatorProportion: string = "95"
  public editorProportion: string = "5"
  public editorLink: string = ""
  public contractUpdate: IContractCreate | IContractUpdate = {} as
    | IContractCreate
    | IContractUpdate

  public async getCoverImage(sourceID: string): Promise<IDataSource> {
    let coverImage = {} as IDataSource
    try {
      const response = await api.getCoverAuthenticated(
        (this as any).$cookies.get("token"),
        sourceID,
        "thumbnail"
      )
      if (response.data) {
        coverImage = response.data
      }
    } catch (error) {}
    return coverImage
  }

  public get creatorName() {
    if (this.creatorProfile.creator) return this.creatorProfile.creator
    else return "Anonymous"
  }

  public get editor(): IPartyUpdate | IPartyCreate | null {
    if (this.contractEdit && Object.keys(this.contractEdit).length > 0) {
      return (this.contractUpdate.parties as any).find(
        (x) => !x.creator || x.creator !== this.creatorProfile.identifier
      )
    } else {
      return null
    }
  }

  public get creator(): IPartyUpdate {
    return (this.contractUpdate.parties as any).find(
      (x) => x.creator && x.creator === this.creatorProfile.identifier
    )
  }

  public get validateProportions(): boolean {
    const parties = [
      { proportion: parseInt(this.creatorProportion) },
      { proportion: parseInt(this.editorProportion) },
    ]
    const result = parties.every((p) => {
      return p.proportion >= 1 && p.proportion <= 100
    })
    if (!result) return false
    const total = parties.reduce((prev, next) => ({
      proportion: prev.proportion + next.proportion,
    }))
    return total.proportion === 100
  }

  public reset() {
    if (this.contractEdit && Object.keys(this.contractEdit).length > 0) {
      this.toUpdate = true
      this.contractUpdate = {
        identifier: this.contractEdit.identifier,
        description: this.contractEdit.description,
        work: this.$route.params.id,
        parties: [],
      }
      for (const party of this.contractEdit.parties) {
        this.contractUpdate.parties.push({
          identifier: party.identifier,
          proportion: party.proportion,
          creator: party.creator ? party.creator.identifier : null,
        })
      }
      this.creatorProportion = String(this.creator.proportion)
      if (this.editor) this.editorProportion = String(this.editor.proportion)
      else this.editorProportion = String(100 - this.creator.proportion)
    } else {
      this.contractUpdate = {
        description: "",
        work: this.$route.params.id,
        parties: [],
      }
      this.creatorProportion = "95"
      this.editorProportion = "5"
      if (
        this.editor &&
        Object.prototype.hasOwnProperty.call(this.editor, "identifier")
      )
        this.editorLink = (this.editor as IPartyUpdate).identifier
    }
  }

  public updateParties() {
    let editor = this.editor
    if (!editor)
      editor = {
        proportion: parseInt(this.editorProportion),
      }
    else editor.proportion = parseInt(this.editorProportion)
    let creator: IPartyCreate | IPartyUpdate = this.creator
    if (!creator)
      creator = {
        creator: this.creatorProfile.identifier,
        proportion: parseInt(this.creatorProportion),
      }
    else creator.proportion = parseInt(this.creatorProportion)
    return [creator, editor]
  }

  public submit() {
    if (
      this.canMakeCreativeOffers &&
      this.contractUpdate.description &&
      this.validateProportions
    ) {
      this.contractUpdate.parties = this.updateParties() as
        | IPartyCreate[]
        | IPartyUpdate[]
      let payload
      if (this.toUpdate) {
        payload = {
          data: this.contractUpdate,
          contractID: (this.contractUpdate as IContractUpdate).identifier,
        }
        this.updateWorkContract(payload)
      } else {
        payload = {
          data: this.contractUpdate,
          workID: this.workEdit.identifier,
        }
        this.createWorkContract(payload)
      }
    }
  }

  public async created() {
    if (this.canMakeCreativeOffers)
      await this.getContractToEdit(this.$route.params.id)
    if (this.contractEdit && Object.keys(this.contractEdit).length)
      await this.getWorkToEdit(this.contractEdit.work.metadata.identifier)
    else await this.getWorkToEdit(this.$route.params.id)
    if (this.workEdit && this.workEdit.identifier)
      this.cover = await this.getCoverImage(this.workEdit.identifier)
    this.reset()
  }

  async asyncData({ store, redirect }) {
    const creator = await store.getters["main/creatorProfile"]
    if (!creator || creator.isBanned) {
      redirect("/creator")
    }
    await store.dispatch("main/getUserProfile")
  }
}
</script>

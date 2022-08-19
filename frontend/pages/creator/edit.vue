<template>
  <div class="container min-h-screen mx-auto flex flex-col">
    <TitleBar title="Edit" />
    <div
      v-if="!canMakeCreativeOffers"
      class="card card-compact rounded-md bg-base-100 shadow-sm lg:mx-10 mb-4"
    >
      <div class="card-body">
        <p>
          Before you can offer your work, or edit the work of others, you'll
          need to ensure your profile is public, that you've verified your email
          address, and that you have a payout wallet saved.
        </p>
        <nuxt-link
          class="flex flex-row text-woad-500 hover:text-woad-800 text-sm"
          to="/get-paid"
        >
          <SvgIcon
            terms="h-5 w-5 inline-flex mr-1"
            icon="svgInformationCircle"
          />
          <p class="text-sm">Read the Guide to getting paid to learn more.</p>
        </nuxt-link>
      </div>
    </div>
    <div class="container max-w-2xl mx-auto">
      <div class="flex items-start">
        <!-- Enabled: "bg-woad-600", Not Enabled: "bg-gray-200" -->
        <button
          type="button"
          :class="`
        ${payload.isPrivate ? 'bg-gray-200' : 'bg-woad-600'}
          relative
          inline-flex
          flex-shrink-0
          h-6
          w-11
          border-2 border-transparent
          rounded-full
          cursor-pointer
          transition-colors
          ease-in-out
          duration-200
          focus:outline-none
          focus:ring-2
          focus:ring-offset-2
          focus:ring-woad-500
        `"
          role="switch"
          :aria-checked="!payload.isPrivate"
          aria-labelledby="is-public"
          @click.prevent="togglePrivacy"
        >
          <!-- Enabled: "translate-x-5", Not Enabled: "translate-x-0" -->
          <span
            aria-hidden="true"
            :class="`
          ${payload.isPrivate ? 'translate-x-0' : 'translate-x-5'}
            pointer-events-none
            inline-block
            h-5
            w-5
            rounded-full
            bg-white
            shadow
            transform
            ring-0
            transition
            ease-in-out
            duration-200
          `"
          ></span>
        </button>
        <span id="is-public" class="ml-3">
          <span class="text-sm text-ochre-500">Profile is </span>
          <span
            v-if="payload.isPrivate"
            class="text-sm font-medium text-ochre-700"
            >Private</span
          >
          <span v-else class="text-sm font-medium text-ochre-700">Public</span>
        </span>
      </div>
    </div>
    <form @submit.prevent="submit">
      <div class="mt-8 max-w-2xl mx-auto">
        <div class="grid grid-cols-1 gap-4 w-full">
          <!-- Creator -->
          <label class="block">
            <span class="text-ochre-600 text-xs ml-3"
              >Creator name - leave blank to be 'Anonymous'</span
            >
            <span class="inpt-span">
              <input
                id="creator"
                v-model="payload.creator"
                name="creator"
                type="text"
                class="inpt-text rounded-l-full"
                placeholder="How do you wish to be known?"
            /></span>
          </label>
          <!-- Description -->
          <label class="block">
            <span class="text-ochre-600 text-xs ml-3">Short description</span>
            <span class="inpt-span-area">
              <!-- Block LastPass on TextArea https://github.com/mui-org/material-ui/issues/14860 -->
              <textarea
                id="description"
                v-model="payload.description"
                name="description"
                type="text"
                class="inpt-textarea"
                rows="1"
                placeholder="Describe yourself and your approach to creation."
                @change.stop
              ></textarea>
            </span>
          </label>
          <div class="flex justify-between">
            <!-- Website -->
            <ValidationProvider v-slot="{ failedRules }" rules="url">
              <label class="flex-auto block mr-2">
                <span class="text-ochre-600 text-xs ml-3">Website</span>
                <span class="inpt-span">
                  <SvgIcon
                    :terms="`inpt-icon ${
                      failedRules.url ? 'text-red-500' : 'text-ochre-400'
                    }`"
                    icon="svgLink" />
                  <input
                    id="website"
                    v-model="payload.website"
                    name="website"
                    type="url"
                    autocomplete="url"
                    class="inpt-text"
                    placeholder="Your personal website."
                /></span>
              </label>
            </ValidationProvider>
            <!-- Wallet -->
            <label class="flex-auto block mr-2">
              <span class="text-ochre-600 text-xs ml-3">Payout wallet</span>
              <span class="inpt-span">
                <input
                  id="wallet"
                  v-model="payload.wallet"
                  name="wallet"
                  type="text"
                  class="inpt-text rounded-l-full"
                  placeholder="Your web monetization wallet."
              /></span>
            </label>
          </div>
        </div>
      </div>
      <!-- Call to action -->
      <div class="mt-8 max-w-2xl mx-auto flex justify-center">
        <button type="submit" class="btn-woad-extended">
          <SvgIcon terms="w-5 h-4 inline-block mr-1" icon="svgReturn" />
          <span>Update</span>
        </button>
      </div>
    </form>
  </div>
</template>

<script lang="ts">
import { Component, Vue, Action, Getter } from "nuxt-property-decorator"
import { ICreatorSummary } from "@/interfaces"

@Component({
  layout: "working",
  middleware: "authenticated",
})
export default class CreatorEditProfile extends Vue {
  @Getter("main/canMakeCreativeOffers") canMakeCreativeOffers
  @Action("main/refreshLoggedProfile") refreshLoggedProfile
  @Action("main/updateCreatorProfile") updateCreatorProfile
  @Action("main/toggleCreatorPrivacy") toggleCreatorPrivacy
  @Getter("main/creatorProfile") creatorProfile
  @Getter("main/userProfile") userProfile
  public payload: ICreatorSummary = {} as ICreatorSummary

  public reset() {
    this.payload = JSON.parse(JSON.stringify(this.creatorProfile))
  }

  public async togglePrivacy() {
    this.payload.isPrivate = !this.payload.isPrivate
    await this.toggleCreatorPrivacy()
  }

  public async submit() {
    await this.updateCreatorProfile(this.payload)
    this.$router.push("/creator")
  }

  async created() {
    if (this.$nuxt.isOffline)
      return this.$nuxt.error({
        statusCode: 404,
      })
    await this.refreshLoggedProfile()
    this.reset()
  }
}
</script>

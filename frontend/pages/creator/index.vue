<template>
  <div class="container min-h-screen mx-auto flex flex-col">
    <TitleBar v-if="creatorProfile.creator" :title="creatorProfile.creator" />
    <TitleBar v-else title="Anonymous" />
    <div class="max-w-screen-md mx-auto">
      <div class="grid grid-cols-3 gap-2">
        <div class="mx-auto flex">
          <NuxtLink
            to="/creator/edit"
            class="btn-woad-extended-sm items-center h-8"
          >
            <SvgIcon terms="w-5 h-4 inline-block mr-1" icon="svgDocumentText" />
            <span class="text-sm">Edit profile</span>
          </NuxtLink>
        </div>
        <div class="mx-auto flex">
          <NuxtLink
            to="/creator/security"
            class="btn-sinopia-extended-sm items-center h-8"
          >
            <SvgIcon terms="w-5 h-4 inline-block mr-1" icon="svgLockClosed" />
            <span class="text-sm">Security &amp; mail</span>
          </NuxtLink>
        </div>
        <div class="mx-auto flex">
          <button class="btn-ochre-extended-sm h-8" @click.prevent="logout">
            <SvgIcon terms="w-5 h-4 inline-block mr-1" icon="svgUser" />
            <span class="text-sm">Logout</span>
          </button>
        </div>
      </div>
    </div>
    <div
      v-if="!canMakeCreativeOffers"
      class="card card-compact rounded-md bg-base-100 shadow-sm lg:mx-10 mt-4"
    >
      <div class="card-body">
        <p>
          Before you can offer your work, or edit the work of others, you'll
          need to complete a few tasks:
        </p>
        <div v-if="!userProfile.email_validated" class="flex items-start">
          <div class="flex-shrink-0">
            <SvgIcon terms="h-6 w-6 text-ochre-600" icon="svgAtSymbol" />
          </div>
          <div class="ml-3 w-0 flex-1 pt-0.5">
            <p class="mb-2">
              Validate your email, or - if you prefer to use a different email
              address - update your profile.
            </p>
            <CreatorValidateEmailButton />
          </div>
        </div>
        <div
          v-if="creatorProfile.isPrivate || !creatorProfile.wallet"
          class="flex items-start"
        >
          <div class="flex-shrink-0">
            <SvgIcon terms="h-6 w-6 text-ochre-600" icon="svgUser" />
          </div>
          <div class="ml-3 w-0 flex-1 pt-0.5">
            <p v-if="creatorProfile.isPrivate" class="mb-2">
              You are welcome to remain anonymous, but you will need to publish
              your profile before others can see your offers.
            </p>
            <p v-if="!creatorProfile.wallet" class="mb-2">
              Add your wallet payment pointer to your profile so you can be
              paid.
            </p>
            <div class="flex">
              <NuxtLink
                to="/creator/edit"
                class="btn-woad-extended-sm items-center h-8"
              >
                <SvgIcon
                  terms="w-5 h-4 inline-block mr-1 mt-1"
                  icon="svgDocumentText"
                />
                <span>Edit profile</span>
              </NuxtLink>
            </div>
          </div>
        </div>
      </div>
    </div>
    <div class="container max-w-screen-sm mx-auto flex-auto">
      <h3 class="text-lg py-4 mt-4 text-left">Profile</h3>
      <p v-if="creatorProfile.description" class="text-sm py-2">
        {{ creatorProfile.description }}
      </p>
      <p v-else class="text-sm py-2 italic">
        The blank page can be the scariest place in the world.
      </p>
      <div class="m-1 space-x-1">
        <span
          v-for="subject in creatorProfile.subject"
          :key="`subject-${subject.identifier}`"
          class="flex-shrink-0 inline-block px-2 py-0.5 text-woad-800 text-xs font-medium bg-woad-100 rounded-full"
          >{{ subject.term }}</span
        >
      </div>
    </div>
  </div>
</template>

<script lang="ts">
import {
  Component,
  Vue,
  Mutation,
  Action,
  Getter,
} from "nuxt-property-decorator"
import { api } from "@/api"

@Component({
  layout: "working",
  middleware: "authenticated",
})
export default class Creator extends Vue {
  @Action("main/logOut") userLogOut
  @Getter("main/creatorProfile") creatorProfile
  @Getter("main/userProfile") userProfile
  @Getter("main/canMakeCreativeOffers") canMakeCreativeOffers
  @Mutation("main/addNotification") addNotification

  public async logout() {
    await this.userLogOut()
    this.$router.push("/")
  }

  async created() {
    if (
      (this as any).$cookies.get("token") &&
      this.$route.query &&
      Object.keys(this.$route.query).length !== 0 &&
      this.$route.query.constructor === Object &&
      this.$route.query.token
    ) {
      const validation = this.$route.query.token as string
      try {
        const response = await api.validateEmail(
          (this as any).$cookies.get("token"),
          validation
        )
        if (response.data) {
          this.addNotification({
            content: "Your email has been validated.",
            color: "success",
          })
        }
      } catch (error) {
        this.addNotification({
          content: "Invalid token. Check your email and resend validation.",
          color: "error",
        })
      }
    }
  }

  async asyncData({ store, redirect }) {
    await store.dispatch("main/getUserProfile")
    const creator = await store.getters["main/creatorProfile"]
    if (!creator || creator.isBanned) {
      redirect("/")
    }
  }
}
</script>

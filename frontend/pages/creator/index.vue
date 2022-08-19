<template>
  <div class="container min-h-screen mx-auto flex flex-col">
    <div
      class="lg:flex lg:items-center lg:justify-between text-center pt-10 pb-8 sm:pt-16 sm:pb-14 px-4 sm:px-6 lg:px-8 mt-16"
    >
      <div class="flex-1 min-w-0">
        <h1 class="text-4xl font-extrabold tracking-tight text-gray-900">
          <span v-if="creatorProfile.creator">{{ creatorProfile.creator }}</span
          ><span v-else>Anonymous</span>
        </h1>
      </div>
      <div class="mt-5 flex justify-center space-x-2 lg:mt-0 lg:ml-4">
        <NuxtLink
          v-for="(t, i) in tabs"
          :key="`tab-action-${i}`"
          :to="t.to"
          class="btn-ochre-sm inline-flex items-center h-7 w-7"
          :aria-label="t.text"
        >
          <SvgIcon terms="w-5 h-5 mx-auto my-auto" :icon="t.icon" />
        </NuxtLink>
        <button
          class="btn-sinopia-sm inline-flex items-center h-7 w-7"
          aria-label="Logout"
          @click.prevent="logout"
        >
          <SvgIcon terms="w-5 h-5 mx-auto my-auto" icon="svgLogout" />
        </button>
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
                  icon="svgPencil"
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
import { IKeyable } from "@/interfaces"

@Component({
  layout: "working",
  middleware: "authenticated",
})
export default class Creator extends Vue {
  @Action("main/refreshLoggedProfile") refreshLoggedProfile
  @Action("main/logOut") userLogOut
  @Getter("main/creatorProfile") creatorProfile
  @Getter("main/userProfile") userProfile
  @Getter("main/canMakeCreativeOffers") canMakeCreativeOffers
  @Mutation("main/addNotification") addNotification
  public tabs: IKeyable[] = [
    {
      to: "/creator/edit",
      icon: "svgPencil",
      text: "Edit profile",
    },
    {
      to: "/creator/security",
      icon: "svgLockClosed",
      text: "Edit security and email",
    },
  ]

  public async logout() {
    await this.userLogOut()
    this.$router.push("/")
  }

  async emailValidation() {
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

  async created() {
    if (this.$nuxt.isOffline)
      return this.$nuxt.error({
        statusCode: 404,
      })
    await this.refreshLoggedProfile()
    if (!this.creatorProfile || this.creatorProfile.isBanned) {
      this.$router.push("/")
    }
    await this.emailValidation()
  }
}
</script>

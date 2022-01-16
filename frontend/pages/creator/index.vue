<template>
  <div class="container min-h-screen mx-auto flex flex-col">
    <TitleBar v-if="creatorProfile.creator" :title="creatorProfile.creator" />
    <TitleBar v-else title="Anonymous" />
    <div class="max-w-screen-md mx-auto">
      <div class="flex space-x-4 w-full justify-center">
        <NuxtLink to="/creator/edit" class="btn-woad-extended-sm h-8">
          <SvgIcon terms="w-5 h-4 inline-block mr-1" icon="svgDocumentText" />
          <span class="text-sm">Edit profile</span>
        </NuxtLink>
        <NuxtLink to="/creator/security" class="btn-sinopia-extended-sm h-8">
          <SvgIcon terms="w-5 h-4 inline-block mr-1" icon="svgLockClosed" />
          <span class="text-sm">Security &amp; mail</span>
        </NuxtLink>
        <div v-show="!userProfile.email_validated">
          <CreatorValidateEmailButton />
        </div>
        <button class="btn-ochre-extended-sm h-8" @click.prevent="logout">
          <SvgIcon terms="w-5 h-4 inline-block mr-1" icon="svgUser" />
          <span class="text-sm">Logout</span>
        </button>
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
          class="
            flex-shrink-0
            inline-block
            px-2
            py-0.5
            text-woad-800 text-xs
            font-medium
            bg-woad-100
            rounded-full
          "
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
  @Mutation("main/addNotification") addNotification
  @Getter("main/token") token

  public async logout() {
    await this.userLogOut()
    this.$router.push("/")
  }

  async created() {
    if (
      this.$route.query &&
      Object.keys(this.$route.query).length !== 0 &&
      this.$route.query.constructor === Object &&
      this.$route.query.token
    ) {
      const validation = this.$route.query.token as string
      try {
        const response = await api.validateEmail(this.token, validation)
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

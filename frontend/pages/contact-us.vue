<template>
  <div class="container min-h-screen max-w-7xl mt-12 mx-auto">
    <div
      class="
        relative
        mx-auto
        py-6
        sm:py-8
        flex flex-col
        items-center
        text-center
      "
    >
      <div class="max-w-4xl w-full space-y-10">
        <h2 class="text-center text-3xl font-extrabold text-gray-900">
          We'd love to hear from you
        </h2>
        <p class="text-xl mt-3 text-ochre-800">
          We are committed to
          <NuxtLink
            to="/privacy-rights"
            class="font-semibold hover:text-ochre-600"
            >personal privacy</NuxtLink
          >. None of the information you provide will be used other than to
          reply to you, and it will only be seen by those entrusted with
          responding to you.
        </p>
      </div>
      <div class="max-w-md w-full space-y-8">
        <ValidationObserver v-slot="{ invalid }">
          <form class="mt-8 space-y-4" @submit.prevent="submit">
            <ValidationProvider v-slot="{ errors }" rules="required">
              <label for="email-address" class="block">
                <span class="inpt-span">
                  <SvgIcon
                    :terms="`inpt-icon ${
                      errors[0] ? 'text-red-500' : 'text-ochre-400'
                    }`"
                    icon="svgAtSymbol"
                  />
                  <input
                    id="email-address"
                    v-model="email"
                    name="email-email"
                    type="email"
                    autocomplete="email"
                    required
                    class="inpt-text"
                    placeholder="Email address"
                  /> </span
              ></label>
            </ValidationProvider>
            <label for="email-subject" class="block">
              <span class="inpt-span">
                <input
                  id="email-subject"
                  v-model="emailSubject"
                  name="email-subject"
                  type="text"
                  autocomplete="text"
                  required
                  class="inpt-text rounded-l-full"
                  placeholder="Your message subject."
              /></span>
            </label>
            <label for="email-body" class="block">
              <span class="inpt-span-area">
                <textarea
                  id="email-body"
                  v-model="emailBody"
                  name="email-body"
                  type="text"
                  autocomplete="text"
                  class="inpt-textarea"
                  rows="4"
                  placeholder="Let us know how feel about our app, or any suggestions or concerns."
                  @change.stop
                ></textarea>
              </span>
            </label>
            <div class="flex w-full justify-center">
              <button
                type="submit"
                :class="`btn-woad-extended ${invalid ? 'opacity-50' : ''}`"
                :disabled="invalid"
              >
                <span>Send</span>
              </button>
            </div>
          </form>
        </ValidationObserver>
      </div>
    </div>
  </div>
</template>

<script lang="ts">
import { Action, Mutation, Component, Vue } from "nuxt-property-decorator"
import { ISendEmail } from "@/interfaces"
import { api } from "@/api"

@Component({
  middleware: "refresh-authentication",
  layout: "working",
})
export default class Login extends Vue {
  @Mutation("main/addNotification") addNotification
  @Action("main/sendMail") sendMail
  public email: string = ""
  public emailSubject: string = ""
  public emailBody: string = ""

  public async submit() {
    if (this.email && this.emailSubject && this.emailBody) {
      const data: ISendEmail = {
        email: this.email,
        subject: this.emailSubject,
        content: this.emailBody,
      }
      try {
        await api.postEmailContact(data)
        this.addNotification({
          content: "Thanks so much for contacting us.",
          color: "success",
        })
        this.$router.push("/")
      } catch (error) {
        this.addNotification({
          content: "Something went wrong with your email.",
          color: "error",
        })
      }
    }
  }
}
</script>

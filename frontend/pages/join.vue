<template>
  <div>
    <div class="min-h-screen flex justify-center px-4 sm:px-6 lg:px-8">
      <div class="max-w-md w-full space-y-8">
        <div>
          <h2 class="text-center text-3xl font-extrabold text-gray-900">
            Create your account
          </h2>
        </div>
        <ValidationObserver v-slot="{ invalid }">
          <form class="mt-8" @submit.prevent="submit">
            <ValidationProvider v-slot="{ failedRules }" rules="email">
              <label for="email-address" class="block">
                <span class="inpt-span">
                  <SvgIcon
                    :terms="`inpt-icon ${
                      failedRules.email ? 'text-red-700' : 'text-ochre-700'
                    }`"
                    icon="svgAtSymbol"
                  />
                  <input
                    id="email-address"
                    v-model="email"
                    name="email"
                    type="email"
                    autocomplete="email"
                    required
                    class="inpt-text"
                    placeholder="Email address"
                  />
                </span>
              </label>
            </ValidationProvider>
            <label for="full-name" class="mt-6 block">
              <span class="inpt-span">
                <SvgIcon terms="inpt-icon text-ochre-700" icon="svgUser" />
                <input
                  id="full-name"
                  v-model="fullName"
                  name="fullName"
                  type="text"
                  autocomplete="name"
                  class="inpt-text"
                  placeholder="Full name"
              /></span>
            </label>

            <ValidationProvider
              v-slot="{ failedRules }"
              name="password1"
              vid="password1"
              rules="confirmed:password2"
            >
              <label for="password1" class="block mt-6">
                <span class="inpt-span">
                  <SvgIcon
                    :terms="`inpt-icon ${
                      failedRules.confirmed ? 'text-red-700' : 'text-ochre-700'
                    }`"
                    icon="svgLockClosed"
                  />
                  <input
                    id="password1"
                    v-model="password1"
                    name="password1"
                    type="password"
                    autocomplete="new-password"
                    placeholder="Create password"
                    required
                    class="inpt-text"
                  />
                </span>
              </label>
            </ValidationProvider>
            <ValidationProvider
              v-slot="{ failedRules }"
              name="password2"
              vid="password2"
            >
              <label for="password2" class="block mt-1">
                <span class="inpt-span">
                  <svg
                    :class="`inpt-icon ${
                      failedRules.confirmed ? 'text-red-700' : 'text-ochre-700'
                    }`"
                    xmlns="http://www.w3.org/2000/svg"
                    fill="none"
                    viewBox="0 0 24 24"
                    stroke="currentColor"
                  >
                    <path
                      stroke-linecap="round"
                      stroke-linejoin="round"
                      stroke-width="2"
                      d=""
                    />
                  </svg>
                  <input
                    id="password2"
                    v-model="password2"
                    name="password2"
                    type="password"
                    autocomplete="new-password"
                    placeholder="Confirm password"
                    required
                    class="inpt-text"
                  />
                </span>
              </label>
            </ValidationProvider>

            <div class="flex w-full justify-center mt-8">
              <button
                type="submit"
                :class="`btn-woad-extended ${invalid ? 'opacity-50' : ''}`"
                :disabled="invalid"
              >
                <SvgIcon
                  terms="w-5 h-3 inline-block mr-1 mb-1"
                  icon="svgLockClosed"
                />
                <span>Join</span>
              </button>
            </div>
          </form>
        </ValidationObserver>
      </div>
    </div>
  </div>
</template>

<script lang="ts">
import { Action, Component, Vue } from "nuxt-property-decorator"
import { IUserOpenProfileCreate } from "@/interfaces"

@Component({
  middleware: "anonymous",
  layout: "working",
})
export default class Join extends Vue {
  @Action("main/createUserProfile") createMe
  public fullName: string = ""
  public email: string = ""
  public password1 = ""
  public password2 = ""

  public async submit() {
    const createdProfile: IUserOpenProfileCreate = {
      email: this.email,
      password: this.password1,
    }
    if (this.fullName) {
      createdProfile.full_name = this.fullName
    }
    await this.createMe(createdProfile)
    this.$router.push("/login")
  }

  public cancel() {
    this.$router.back()
  }
}
</script>

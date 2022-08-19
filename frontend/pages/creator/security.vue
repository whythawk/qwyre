<template>
  <div class="container min-h-screen mx-auto flex flex-col">
    <TitleBar title="Security settings" />
    <div class="mx-auto w-full space-y-8">
      <!-- UPDATE PASSWORD -->
      <div
        class="card card-compact w-full md:w-3/4 bg-ochre-50 rounded-lg shadow-xl mx-auto"
      >
        <div class="card-body">
          <div class="mx-auto space-y-8">
            <div>
              <h2 class="text-center text-3xl font-extrabold text-gray-900">
                Update your password
              </h2>
            </div>
            <ValidationObserver v-slot="{ invalid }">
              <form class="mt-8" @submit.prevent="changePassword">
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
                          failedRules.confirmed
                            ? 'text-red-700'
                            : 'text-ochre-700'
                        }`"
                        icon="svgLockClosed"
                      />
                      <input
                        id="password1"
                        v-model="password1"
                        name="password1"
                        type="password"
                        autocomplete="new-password"
                        placeholder="New password"
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
                          failedRules.confirmed
                            ? 'text-red-700'
                            : 'text-ochre-700'
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
                    <span>Update Password</span>
                  </button>
                </div>
              </form>
            </ValidationObserver>
          </div>
        </div>
      </div>
      <!-- CHANGE EMAIL -->
      <div
        class="card card-compact w-full md:w-3/4 bg-ochre-100 rounded-lg shadow-xl mx-auto"
      >
        <div class="card-body">
          <div class="mx-auto space-y-8">
            <h2 class="text-center text-3xl font-extrabold text-gray-900">
              Change your email
            </h2>
          </div>
          <ValidationObserver v-slot="{ invalid }">
            <form class="mt-8" @submit.prevent="changeEmail">
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
              <div class="flex w-full justify-center mt-8">
                <button
                  type="submit"
                  :class="`btn-woad-extended ${invalid ? 'opacity-50' : ''}`"
                  :disabled="invalid"
                >
                  <SvgIcon
                    terms="w-5 h-3 inline-block mr-1 mb-1"
                    icon="svgAtSymbol"
                  />
                  <span>Change email</span>
                </button>
              </div>
            </form>
          </ValidationObserver>
        </div>
      </div>
    </div>
  </div>
</template>

<script lang="ts">
import { Component, Action, Vue } from "nuxt-property-decorator"
import { IUserProfileUpdate } from "@/interfaces"

@Component({
  layout: "working",
  middleware: "authenticated",
})
export default class CreatorEditSecurity extends Vue {
  @Action("main/refreshLoggedProfile") refreshLoggedProfile
  @Action("main/updateUserProfile") updateUserProfile
  public email: string = ""
  public password1 = ""
  public password2 = ""

  public async changePassword() {
    const updatedProfile: IUserProfileUpdate = {}
    updatedProfile.password = this.password1
    await this.updateUserProfile(updatedProfile)
    this.$router.push("/creator")
  }

  public async changeEmail() {
    const updatedProfile: IUserProfileUpdate = {}
    if (this.email) {
      updatedProfile.email = this.email
      await this.updateUserProfile(updatedProfile)
      this.$router.push("/creator")
    }
  }

  async created() {
    if (this.$nuxt.isOffline)
      return this.$nuxt.error({
        statusCode: 404,
      })
    await this.refreshLoggedProfile()
  }
}
</script>

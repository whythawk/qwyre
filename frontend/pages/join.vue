<template>
  <div class="container min-h-screen mx-auto flex flex-col">
    <TitleBar title="Go on - create something wonderful" />
    <div class="flex space-x-8 w-full justify-center">
      <!-- JOIN -->
      <div class="max-w-md w-full bg-ochre-50 rounded-lg shadow-xl">
        <div class="w-3/4 mx-auto my-8 space-y-8">
          <div>
            <h2 class="text-center text-3xl font-extrabold text-gray-900">
              Create your account
            </h2>
          </div>
          <ValidationObserver v-slot="{ invalid }">
            <form class="mt-8 space-y-4" @submit.prevent="join">
              <ValidationProvider v-slot="{ failedRules }" rules="email">
                <label for="join-email-address" class="block">
                  <span class="inpt-span">
                    <SvgIcon
                      :terms="`inpt-icon ${
                        failedRules.email
                          ? 'text-sinopia-700'
                          : 'text-ochre-700'
                      }`"
                      icon="svgAtSymbol"
                    />
                    <input
                      id="join-email-address"
                      v-model="joinEmail"
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
                    placeholder="Creator name"
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
                        failedRules.confirmed
                          ? 'text-sinopia-700'
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
                        failedRules.confirmed
                          ? 'text-sinopia-700'
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

              <div class="flex justify-between">
                <div class="text-sm">
                  <NuxtLink
                    :to="loginRoute"
                    class="font-medium text-ochre-600 hover:text-ochre-400"
                  >
                    Login to your account
                  </NuxtLink>
                </div>
                <div class="text-sm">
                  <NuxtLink
                    :to="recoverRoute"
                    class="font-medium text-ochre-600 hover:text-ochre-400"
                  >
                    Forgot your password?
                  </NuxtLink>
                </div>
              </div>

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
  </div>
</template>

<script lang="ts">
import { Action, Component, Vue } from "nuxt-property-decorator"
import { IUserOpenProfileCreate, IKeyable } from "@/interfaces"

@Component({
  middleware: "anonymous",
  layout: "working",
})
export default class Join extends Vue {
  @Action("main/logIn") logIn
  @Action("main/createUserProfile") createMe
  public fullName: string = ""
  public email: string = ""
  public joinEmail: string = ""
  public password1 = ""
  public password2 = ""
  public password: string = ""
  public loginRoute: string = "/login"
  public recoverRoute: string = "/recover-password"
  public subscriptionRoute: string = "/pricing"
  public redirectRoute: IKeyable = {
    path: "/",
  }

  public redirectRoutes: IKeyable = {
    convert: "/write/convert",
  }

  public async join() {
    const createdProfile: IUserOpenProfileCreate = {
      email: this.joinEmail,
      password: this.password1,
    }
    if (this.fullName) {
      createdProfile.full_name = this.fullName
    }
    await this.createMe(createdProfile)
    this.email = this.joinEmail
    this.password = this.password1
    await this.login()
  }

  public async login() {
    await this.logIn({
      username: this.email,
      password: this.password,
    })
    this.$router.push(this.redirectRoute)
  }

  public created() {
    try {
      if (
        this.$route.query &&
        this.$route.query.next &&
        Object.keys(this.redirectRoutes).includes(
          this.$route.query.next as string
        )
      ) {
        this.redirectRoute.path =
          this.redirectRoutes[this.$route.query.next as string]
      }
    } catch {}
    if (
      this.$route.query &&
      Object.keys(this.$route.query).length !== 0 &&
      this.$route.query.constructor === Object
    ) {
      const query = Object.keys(this.$route.query)
        .map((key) => key + "=" + this.$route.query[key])
        .join("&")
      this.loginRoute = `/login?${query}`
      this.recoverRoute = `/recover-password?${query}`
      this.redirectRoute.query = this.$route.query
    }
  }
}
</script>

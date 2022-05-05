<template>
  <div class="container min-h-screen mx-auto flex flex-col">
    <TitleBar title="Go on - create something wonderful" />
    <div class="flex space-x-8 w-full justify-center">
      <!-- LOGIN -->
      <div class="max-w-md w-full bg-ochre-100 rounded-lg shadow-xl">
        <div class="w-3/4 mx-auto my-8 space-y-8">
          <div>
            <h2 class="text-center text-3xl font-extrabold text-gray-900">
              Sign in to your account
            </h2>
          </div>
          <ValidationObserver v-slot="{ invalid }">
            <form class="mt-8 space-y-4" @submit.prevent="login">
              <ValidationProvider v-slot="{ errors }" rules="required">
                <label for="email-address" class="block">
                  <span class="inpt-span">
                    <SvgIcon
                      :terms="`inpt-icon ${
                        errors[0] ? 'text-sinopia-700' : 'text-ochre-700'
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
                      @keyup.enter="login"
                    /> </span
                ></label>
              </ValidationProvider>
              <ValidationProvider v-slot="{ errors }" rules="required">
                <label for="password" class="block">
                  <span class="inpt-span mt-2">
                    <SvgIcon
                      :terms="`inpt-icon ${
                        errors[0] ? 'text-sinopia-700' : 'text-ochre-700'
                      }`"
                      icon="svgLockClosed"
                    />
                    <input
                      id="password"
                      v-model="password"
                      name="password"
                      type="password"
                      autocomplete="current-password"
                      required
                      class="inpt-text"
                      placeholder="Password"
                      @keyup.enter="login"
                    /> </span
                ></label>
              </ValidationProvider>

              <div class="flex justify-between">
                <div class="text-sm">
                  <NuxtLink
                    :to="joinRoute"
                    class="font-medium text-ochre-600 hover:text-ochre-400"
                  >
                    Create an account
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

              <div class="flex w-full justify-center">
                <button
                  type="submit"
                  :class="`btn-woad-extended ${invalid ? 'opacity-50' : ''}`"
                  :disabled="invalid"
                >
                  <SvgIcon
                    terms="w-5 h-3 inline-block mr-1 mb-1"
                    icon="svgLockClosed"
                  />
                  <span>Sign in</span>
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
import { IKeyable } from "@/interfaces"

@Component({
  middleware: "anonymous",
  layout: "working",
})
export default class Login extends Vue {
  @Action("main/logIn") logIn
  public email: string = ""
  public password: string = ""
  public joinRoute: string = "/join"
  public recoverRoute: string = "/recover-password"
  public subscriptionRoute: string = "/pricing"
  public redirectRoute: IKeyable = {
    path: "/",
  }

  public redirectRoutes: IKeyable = {
    convert: "/write/convert",
  }

  public async login() {
    await this.logIn({
      username: this.email,
      password: this.password,
    })
    this.$router.push(this.redirectRoute)
  }

  public created() {
    if (
      this.$route.query &&
      Object.keys(this.$route.query).length !== 0 &&
      this.$route.query.constructor === Object
    ) {
      const query = Object.keys(this.$route.query)
        .map((key) => key + "=" + this.$route.query[key])
        .join("&")
      this.joinRoute = `/join?${query}`
      this.recoverRoute = `/recover-password?${query}`
      this.redirectRoute.query = this.$route.query
    }
    try {
      if (
        this.$route.query &&
        this.$route.query.next &&
        Object.keys(this.redirectRoutes).includes(
          this.$route.query.next as string
        )
      ) {
        this.redirectRoute = {
          path: this.redirectRoutes[this.$route.query.next as string],
        }
      }
    } catch {}
  }
}
</script>

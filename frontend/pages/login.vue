<template>
  <div>
    <div class="min-h-screen flex justify-center px-4 sm:px-6 lg:px-8">
      <div class="max-w-md w-full space-y-8">
        <div>
          <h2 class="text-center text-3xl font-extrabold text-gray-900">
            Sign in to your account
          </h2>
        </div>
        <ValidationObserver v-slot="{ invalid }">
          <form class="mt-8 space-y-4" @submit.prevent="submit">
            <ValidationProvider v-slot="{ errors }" rules="required">
              <label for="email-address" class="block">
                <span class="inpt-span">
                  <SvgIcon
                    :terms="`inpt-icon ${
                      !errors[0] ? 'text-red-500' : 'text-ochre-400'
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
                    @keyup.enter="submit"
                  /> </span
              ></label>
            </ValidationProvider>
            <ValidationProvider v-slot="{ errors }" rules="required">
              <label for="password" class="block">
                <span class="inpt-span mt-2">
                  <SvgIcon
                    :terms="`inpt-icon ${
                      !errors[0] ? 'text-red-500' : 'text-ochre-400'
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
                    @keyup.enter="submit"
                  /> </span
              ></label>
            </ValidationProvider>

            <div class="flex justify-between">
              <div class="text-sm">
                <NuxtLink
                  to="/join"
                  class="font-medium text-ochre-600 hover:text-ochre-400"
                >
                  Create an account
                </NuxtLink>
              </div>
              <div class="text-sm">
                <NuxtLink
                  to="/recover-password"
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
</template>

<script lang="ts">
import { Action, Component, Vue } from "nuxt-property-decorator"

@Component({
  middleware: "anonymous",
  layout: "working",
})
export default class Login extends Vue {
  @Action("main/logIn") logIn
  public email: string = ""
  public password: string = ""

  public async submit() {
    await this.logIn({
      username: this.email,
      password: this.password,
    })
    this.$router.push("/main/dashboard")
  }
}
</script>

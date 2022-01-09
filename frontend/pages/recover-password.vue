<template>
  <div class="container min-h-screen mx-auto flex flex-col">
    <TitleBar title="Recover your account" />
    <div class="max-w-md w-full mx-auto space-y-8">
      <form class="mt-8 space-y-4">
        <label for="email-address" class="block">
          <span class="inpt-span">
            <input
              id="email-address"
              v-model="username"
              name="email"
              type="email"
              autocomplete="email"
              required
              class="inpt-text rounded-l-full"
              placeholder="Email address"
              @keyup.enter="submit"
            /> </span
        ></label>
        <div class="flex w-full justify-center">
          <button
            type="submit"
            class="btn-woad-extended"
            @click.prevent="submit"
          >
            <SvgIcon
              terms="w-5 h-3 inline-block mr-1 mb-1"
              icon="svgLockClosed"
            />
            <span>Recover</span>
          </button>
        </div>
      </form>
    </div>
  </div>
</template>

<script lang="ts">
import { Action, Component, Vue } from "nuxt-property-decorator"

@Component({
  middleware: "anonymous",
  layout: "working",
})
export default class RecoverPassword extends Vue {
  @Action("main/passwordRecovery") passwordRecovery
  public username: string = ""

  public submit() {
    this.passwordRecovery({ username: this.username })
  }
}
</script>

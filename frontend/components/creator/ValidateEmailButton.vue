<template>
  <button
    type="submit"
    class="btn-malachite-extended flex items-center h-8"
    @click.prevent="submit"
  >
    <SvgIcon terms="w-5 h-4 inline-block mr-1 mb-1" icon="svgAtSymbol" />
    <span class="text-sm">Validate email</span>
  </button>
</template>

<script lang="ts">
import { Component, Vue, Mutation } from "nuxt-property-decorator"
import { api } from "@/api"

@Component
export default class CreatorValidateEmailButton extends Vue {
  @Mutation("main/addNotification") addNotification

  public async submit() {
    if ((this as any).$cookies.get("token")) {
      try {
        const response = await api.requestValidationEmail(
          (this as any).$cookies.get("token")
        )
        if (response.data) {
          this.addNotification({
            content: "Validation sent. Check your email and respond.",
            color: "success",
          })
        }
      } catch (error) {
        this.addNotification({
          content: "Please check your email and try again.",
          color: "error",
        })
      }
    }
  }
}
</script>

<template>
  <button
    type="submit"
    class="btn-woad-extended flex items-center h-8"
    @click.prevent="submit"
  >
    <SvgIcon terms="w-5 h-4 inline-block mr-1 mb-1" icon="svgBookmark" />
    <span class="text-sm">Express interest</span>
  </button>
</template>

<script lang="ts">
import {
  Component,
  Vue,
  Mutation,
  Getter,
  Prop,
  Action,
} from "nuxt-property-decorator"
import { api } from "@/api"

@Component
export default class CreatorExpressOfferInterestButton extends Vue {
  @Prop(String) readonly contractId!: string
  @Mutation("main/addNotification") addNotification
  @Action("main/addErrorNotification") addErrorNotification

  public async submit() {
    if ((this as any).$cookies.get("token")) {
      try {
        const response = await api.expressContractInterest(
          (this as any).$cookies.get("token"),
          this.contractId
        )
        if (response.data) {
          this.addNotification({
            content:
              "We have expressed your interest. Check your email for further details.",
            color: "success",
          })
        }
      } catch (error) {
        this.addErrorNotification(error)
      }
    }
  }
}
</script>

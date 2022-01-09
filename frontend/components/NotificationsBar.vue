<template>
  <div class="fixed z-50 bottom-0 mx-auto w-full">
    <div
      v-show="showNotification"
      class="grid grid-cols-1 gap-2 justify-center items-center"
    >
      <div
        :class="`flex items-center text-ochre-10 max-w-sm w-full ${fadeState} ${currentNotificationColor} shadow-md rounded-lg overflow-hidden mx-auto`"
      >
        <div class="w-10 border-r px-2">
          <div class="flex space-x-3">
            <div v-if="!showProgress">
              <SvgIcon
                v-show="colorMatch === 'info'"
                terms="h-6 w-6"
                icon="svgInformationCircle"
              />
              <SvgIcon
                v-show="colorMatch === 'error'"
                terms="h-6 w-6"
                icon="svgExclamationCircle"
              />
              <SvgIcon
                v-show="colorMatch === 'success'"
                terms="h-6 w-6"
                icon="svgCheckCircle"
              />
            </div>
            <div v-else>
              <SvgIcon terms="animate-spin h-6 w-6" icon="svgCog" />
            </div>
          </div>
        </div>
        <div class="flex items-center px-2 py-3">
          <div class="mx-3">
            <p>{{ currentNotificationContent }}</p>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script lang="ts">
import {
  Action,
  Component,
  Mutation,
  Getter,
  Watch,
  Vue,
  Ref,
} from "nuxt-property-decorator"
import { AppNotification } from "@/store/main/state"

@Component
export default class RecoverPassword extends Vue {
  @Getter("main/firstNotification") firstNotification
  @Mutation("main/removeNotification") mutateNotification
  @Action("main/removeNotification") removeNotification
  @Ref("new-cover-uploaded") readonly newCoverUpload!: HTMLSpanElement
  public showNotification: boolean = false
  public fadeState: string = "animate-fade-down-out"
  public showProgress: boolean = false
  public currentNotification: AppNotification | false = false
  public timeoutHandle: any | false = false

  public close() {
    this.fadeState = "animate-fade-out-down duration-500"
    setTimeout(() => {
      this.currentNotification = false
      this.showNotification = false
      this.mutateNotification(this.currentNotification)
    }, 500)
  }

  public setNotification(notification: AppNotification | false) {
    if (notification) {
      this.currentNotification = notification
      this.showProgress = notification.showProgress || false
      this.fadeState = "animate-fade-in-up"
      this.showNotification = true
    } else {
      this.close()
    }
  }

  @Watch("firstNotification", { immediate: true })
  public async onNotificationChange(newNotification: AppNotification | false) {
    if (newNotification !== this.currentNotification) {
      this.setNotification(newNotification)
      if (newNotification) {
        await this.removeNotification({
          notification: newNotification,
          timeout: 2000,
        })
      }
    }
  }

  public get currentNotificationContent() {
    return (this.currentNotification && this.currentNotification.content) || ""
  }

  public get colorMatch() {
    return (
      (this.currentNotification && this.currentNotification.color) || "info"
    )
  }

  public get currentNotificationColor() {
    const colormatch = {
      info: "bg-woad-500",
      error: "bg-sinopia-500",
      success: "bg-malachite-500",
    }
    return colormatch[this.colorMatch]
  }
}
</script>

<template>
  <transition
    enter-active-class="duration-400 sm:duration-500"
    leave-active-class="duration-400 sm:duration-500"
  >
    <div
      v-show="showOptions"
      ref="options-panel-view"
      class="z-40 fixed inset-0"
    >
      <transition
        enter-active-class="ease-in-out duration-400 sm:duration-500"
        enter-from-class="opacity-0"
        enter-to-class="opacity-100"
        leave-active-class="ease-in-out duration-400 sm:duration-500"
        leave-from-class="opacity-100"
        leave-to-class="opacity-0"
      >
        <div v-show="showOptions" class="absolute inset-0">
          <!-- Background overlay, show/hide based on showOptions state. -->
          <div
            class="absolute inset-0 bg-ochre-700 bg-opacity-30 transition-opacity"
            aria-hidden="true"
          ></div>
          <!-- top options panel: user experience -->
          <transition
            enter-active-class="transform transition ease-in-out duration-400 sm:duration-500 opacity-100"
            enter-from-class="-translate-y-full"
            enter-to-class="translate-y-0"
            leave-active-class="transform transition ease-in-out duration-400 sm:duration-500 opacity-100"
            leave-from-class="translate-y-0"
            leave-to-class="-translate-y-full"
          >
            <div
              v-show="showOptions"
              class="z-40 fixed inset-x-0 top-0 w-screen flex"
            >
              <div class="w-screen">
                <div
                  class="relative flex flex-col py-4 bg-ochre-900 opacity-90 shadow-xl"
                >
                  <div class="relative flex-1 px-4 sm:px-6">
                    <NavigationReaderMenu />
                  </div>
                </div>
              </div>
            </div>
          </transition>
          <!-- bottom options panel: navigation -->
          <transition
            enter-active-class="transform transition ease-in-out duration-400 sm:duration-500 opacity-100"
            enter-from-class="translate-y-full"
            enter-to-class="translate-y-0"
            leave-active-class="transform transition ease-in-out duration-400 sm:duration-500 opacity-100"
            leave-from-class="translate-y-0"
            leave-to-class="translate-y-full"
          >
            <div
              v-show="showOptions"
              class="z-40 fixed inset-x-0 bottom-0 w-screen flex"
            >
              <div class="w-screen">
                <div
                  class="relative flex flex-col py-4 bg-ochre-900 opacity-90 shadow-xl"
                >
                  <div class="relative flex-1 px-4 sm:px-6">
                    <NavigationReaderOptions :completion="completion" />
                  </div>
                </div>
              </div>
            </div>
          </transition>
        </div>
      </transition>
    </div>
  </transition>
</template>

<script lang="ts">
import {
  Component,
  Vue,
  Getter,
  Ref,
  Mutation,
  Prop,
} from "nuxt-property-decorator"
import { clickYListener } from "@/mixins/readerListeners"

@Component
export default class OverlaysReaderOptions extends Vue {
  @Prop(String) readonly completion!: string
  @Ref("options-panel-view") readonly optionsView!: HTMLElement
  @Getter("main/showOptions") showOptions
  @Mutation("main/setShowOptions") setShowOptions

  public listenerResponse(event: string) {
    if (this.showOptions && ["close", "menu"].includes(event)) {
      this.setShowOptions(false)
    } else if (!this.showOptions && ["open", "menu"].includes(event)) {
      this.setShowOptions(true)
    }
  }

  mounted() {
    clickYListener(this.optionsView, this.listenerResponse)
  }
}
</script>

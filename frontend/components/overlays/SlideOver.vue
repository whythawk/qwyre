<template>
  <div
    :class="`z-40 fixed inset-0 overflow-hidden ${
      !showOptions ? 'hidden' : ''
    }`"
    aria-labelledby="slide-over-title"
    role="dialog"
    aria-modal="true"
  >
    <div class="absolute inset-0 overflow-hidden">
      <!-- Background overlay, show/hide based on slide-over state. -->
      <div class="absolute inset-0" aria-hidden="true"></div>

      <div v-show="showOptions" class="fixed inset-x-0 top-0 w-screen flex">
        <transition
          enter-active-class="transform transition ease-in-out duration-500 sm:duration-700"
          enter-from-class="translate-x-full"
          enter-to-class="translate-x-0"
          leave-active-class="transform transition ease-in-out duration-500 sm:duration-700"
          leave-from-class="translate-x-0"
          leave-to-class="translate-x-full"
        >
          <div class="w-screen">
            <div
              class="h-40 flex flex-col py-6 bg-white shadow-xl overflow-y-scroll"
            >
              <div class="px-4 sm:px-6">
                <div class="flex items-start justify-between">
                  <h2
                    id="slide-over-title"
                    class="text-lg font-medium text-gray-900"
                  >
                    Panel title
                  </h2>
                  <div class="ml-3 h-12 flex items-center">
                    <button
                      class="bg-white rounded-md text-gray-400 hover:text-gray-500 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500"
                    >
                      <span class="sr-only">Close panel</span>
                      <!-- Heroicon name: outline/x -->
                      <SvgIcon terms="h-6 w-6" icon="svgX" />
                    </button>
                  </div>
                </div>
              </div>
              <div class="mt-6 relative flex-1 px-4 sm:px-6">
                <!-- Replace with your content -->
                <div class="absolute inset-0 px-4 sm:px-6">
                  <div
                    class="h-full border-2 border-dashed border-gray-200"
                    aria-hidden="true"
                  >
                    {{ showOptions }}
                  </div>
                </div>
                <!-- /End replace -->
              </div>
            </div>
          </div>
        </transition>
      </div>
    </div>
  </div>
</template>

<script lang="ts">
import { Component, Vue, Getter } from "nuxt-property-decorator"

@Component
export default class SlideOver extends Vue {
  @Getter("anthology/showOptions") showOptions
}
</script>

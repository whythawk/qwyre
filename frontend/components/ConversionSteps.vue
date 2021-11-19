<template>
  <!-- https://tailwindcomponents.com/component/steps-bar -->
  <div v-show="currentStep" class="w-3/4 mx-auto py-10">
    <div class="flex">
      <div v-for="step in steps" :key="`step-${step.key}`" class="w-1/4">
        <div class="relative mb-2">
          <div
            v-show="step.key != 'description'"
            class="absolute flex align-center items-center align-middle content-center"
            style="
              width: calc(100% - 2.5rem - 1rem);
              top: 50%;
              transform: translate(-50%, -50%);
            "
          >
            <div
              class="w-full bg-ochre-100 bg-opacity-70 rounded items-center align-middle align-center flex-1"
            >
              <div
                :class="`${step.linewidth} bg-malachite-200 py-1 rounded`"
              ></div>
            </div>
          </div>
          <div
            :class="`w-10 h-10 mx-auto ${step.color} rounded-full text-lg text-ochre-50 flex items-center`"
          >
            <span class="text-center text-ochre-50 w-full">
              <SvgIcon
                terms="w-6 h-6 mx-auto my-auto"
                :icon="svgIcons[step.key]"
              />
            </span>
          </div>
        </div>
        <div
          v-if="liveSteps[step.key]"
          class="text-xs font-sans text-center md:text-sm"
        >
          <NuxtLink
            :to="`${
              step.key === 'conversion' ? '/convert' : `/convert/${step.key}`
            }`"
            >{{ step.value }}</NuxtLink
          >
        </div>
        <div v-else class="text-xs font-sans text-center md:text-sm">
          {{ step.value }}
        </div>
      </div>
    </div>
  </div>
</template>

<script lang="ts">
import { Component, Vue, Getter, Watch } from "nuxt-property-decorator"
import { idb } from "@/api"
import { IConversion } from "@/interfaces"

@Component
export default class ConversionSteps extends Vue {
  @Getter("conversions/conversionKey") conversionKey
  @Getter("conversions/currentStep") currentStep

  public steps: { [key: string]: string }[] = [
    { key: "description", value: "Describe" },
    { key: "upload", value: "Upload" },
    { key: "dedication", value: "Dedicate" },
    { key: "conversion", value: "Convert" },
  ]

  public svgIcons: { [key: string]: string } = {
    description: "svgAnnotation",
    upload: "svgUpload",
    dedication: "svgFire",
    conversion: "svgCog",
  }

  public liveSteps: { [key: string]: boolean } = {
    description: false,
    upload: false,
    dedication: false,
    conversion: false,
  }

  @Watch("currentStep")
  public async setSteps() {
    let hasKey = 0
    if (this.conversionKey)
      hasKey = await idb.hasKey("conversion", this.conversionKey)
    if (hasKey === 1) {
      const conversion = (await idb.getPayload(
        "conversion",
        this.conversionKey
      )) as IConversion
      this.liveSteps = { ...conversion.conversionState }
    }
    this.liveSteps[this.currentStep] = true
    this.steps.forEach((element) => {
      // element is current page ? blue : element is complete ? green : ochre
      element.color =
        element.key === this.currentStep
          ? "bg-woad-200"
          : this.liveSteps[element.key]
          ? "bg-malachite-200"
          : "bg-ochre-200 bg-opacity-70"
      // element is complete ? full : element is current page ? 2/5 : 0
      element.linewidth = this.liveSteps[element.key] ? "w-full" : "w-0"
    })
  }

  created() {
    this.setSteps()
  }
}
</script>

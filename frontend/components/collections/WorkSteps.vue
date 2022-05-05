<template>
  <nav
    v-show="currentStep"
    class="flex items-center justify-center py-10 pt-28"
    aria-label="Publishing process"
  >
    <p class="text-ochre-600 text-sm font-medium">{{ currentDescription }}</p>
    <ol role="list" class="ml-8 flex items-center space-x-5">
      <li v-for="step in steps" :key="`step-${step.key}`">
        <NuxtLink
          tag="button"
          :to="step.to"
          :class="`${
            currentStep === step.key
              ? 'relative flex items-center justify-center'
              : step.complete
              ? 'block w-2.5 h-2.5 rounded-full bg-malachite-200 hover:bg-malachite-400'
              : 'block w-2.5 h-2.5 rounded-full bg-ochre-50 hover:bg-ochre-200'
          }`"
          :disabled="!step.complete"
        >
          <span
            v-if="currentStep === step.key"
            class="absolute w-5 h-5 p-px flex"
            aria-hidden="true"
          >
            <span class="w-full h-full rounded-full bg-malachite-100"></span>
          </span>
          <span
            v-if="currentStep === step.key"
            class="relative block w-2.5 h-2.5 bg-malachite-400 rounded-full"
            aria-hidden="true"
          ></span>
          <span class="sr-only">Step {{ step.step }}: {{ step.value }}</span>
        </NuxtLink>
      </li>
    </ol>
  </nav>
</template>

<script lang="ts">
import { Component, Vue, Getter, Watch } from "nuxt-property-decorator"
import { idb } from "@/api"
import { IConversion } from "@/interfaces"

@Component
export default class CollectionsWorkSteps extends Vue {
  @Getter("conversions/conversionKey") conversionKey
  @Getter("conversions/currentStep") currentStep
  public currentDescription: string = "Step 1 of 4: Describe your work"

  public steps: { [key: string]: string | boolean }[] = [
    {
      key: "describe",
      value: "Describe your work",
      step: "1",
      to: "/write/describe",
      complete: false,
    },
    {
      key: "attribute",
      value: "Attribute artist & contributors",
      step: "2",
      to: "/write/attribute",
      complete: false,
    },
    {
      key: "convert",
      value: "Build your epub",
      step: "3",
      to: "/write/convert",
      complete: false,
    },
    {
      key: "submit",
      value: "Submit your work for editing",
      step: "4",
      to: "/write/convert",
      complete: false,
    },
  ]

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
      this.steps.forEach((element) => {
        // element is current page ? blue : element is complete ? green : ochre
        element.complete = conversion.conversionState.includes(
          element.key as string
        )
        if (element.key === this.currentStep)
          this.currentDescription = `Step ${element.step} of ${this.steps.length}: ${element.value}`
      })
    }
    console.log("-------------------------------------------------------------")
    console.log(this.conversionKey)
    console.log("-------------------------------------------------------------")
  }

  created() {
    this.setSteps()
  }
}
</script>

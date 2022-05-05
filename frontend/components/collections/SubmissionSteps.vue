<template>
  <nav
    v-show="effectiveState"
    class="flex justify-center"
    aria-label="Publishing process"
  >
    <ol role="list" class="space-y-3">
      <li v-for="step in steps" :key="`step-${step.key}`">
        <div class="group">
          <span class="flex items-start">
            <span
              v-if="step.complete && step.key !== effectiveState"
              class="flex-shrink-0 relative h-5 w-5 flex items-center justify-center"
            >
              <svg
                class="h-full w-full text-malachite-400"
                xmlns="http://www.w3.org/2000/svg"
                viewBox="0 0 20 20"
                fill="currentColor"
                aria-hidden="true"
              >
                <path
                  fill-rule="evenodd"
                  d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z"
                  clip-rule="evenodd"
                />
              </svg>
            </span>
            <div
              v-else
              class="flex-shrink-0 h-5 w-5 relative flex items-center justify-center"
              aria-hidden="true"
            >
              <span
                v-if="step.key === effectiveState"
                class="absolute h-4 w-4 rounded-full bg-malachite-200"
              ></span>
              <span
                :class="`relative block w-2 h-2 rounded-full ${
                  step.key === effectiveState
                    ? 'bg-malachite-400'
                    : 'bg-ochre-200'
                }`"
              ></span>
            </div>
            <span class="ml-3 text-sm font-medium text-gray-600">{{
              step.value
            }}</span>
          </span>
        </div>
      </li>
    </ol>
  </nav>
</template>

<script lang="ts">
import { Component, Vue, Prop } from "nuxt-property-decorator"

@Component
export default class CollectionsSubmissionSteps extends Vue {
  @Prop(String) readonly workState!: string
  @Prop(Boolean) readonly contractState!: boolean
  public effectiveState: string = "offered"

  public steps: { [key: string]: string | boolean }[] = [
    {
      key: "submitted",
      value: "Submitted",
      step: "1",
      complete: false,
    },
    {
      key: "offered",
      value: "Offered for editing",
      step: "2",
      complete: false,
    },
    {
      key: "contracted",
      value: "Contracted an editor",
      step: "3",
      complete: false,
    },
    {
      key: "edited",
      value: "Completed editing",
      step: "4",
      complete: false,
    },
    {
      key: "published",
      value: "Published",
      step: "4",
      complete: false,
    },
  ]

  public created() {
    this.effectiveState = this.workState
    if (this.effectiveState === "updated" && this.contractState)
      this.effectiveState = "offered"
    if (this.effectiveState === "updated" && !this.contractState)
      this.effectiveState = "submitted"
    for (const s of this.steps) {
      s.complete = true
      if (s.key === this.effectiveState) break
    }
  }
}
</script>

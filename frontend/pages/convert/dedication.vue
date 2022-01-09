<template>
  <div class="flex-auto">
    <div>
      <p class="pb-1">A dedication is not required, but is appreciated ;p</p>
      <nuxt-link
        class="flex flex-row text-woad-500 underline pt-1"
        to="/get-started"
      >
        <SvgIcon terms="h-6 w-6 inline-flex" icon="svgInformationCircle" />
        <p>Read the Guide for more details...</p>
      </nuxt-link>
    </div>
    <form>
      <div class="mt-8 max-w-2xl mx-auto">
        <div class="grid grid-cols-1 gap-4 w-full">
          <!-- Dedication -->
          <label class="block">
            <span class="text-ochre-600 text-xs ml-3">Dedication</span>
            <span class="inpt-span-area">
              <!-- Block LastPass on TextArea https://github.com/mui-org/material-ui/issues/14860 -->
              <textarea
                id="dedication_text"
                v-model="dedication"
                name="dedication_text"
                type="text"
                class="inpt-textarea"
                rows="4"
                placeholder="Dedicate your work. Optional, but appreciated."
                @change.stop
              ></textarea>
            </span>
          </label>
        </div>
      </div>
      <!-- Call to action -->
      <div class="mt-8 max-w-2xl flex mx-auto justify-center">
        <div class="mt-3 sm:mt-0 sm:ml-3">
          <button
            type="submit"
            class="btn-woad-extended"
            @click.prevent="submit"
          >
            <SvgIcon terms="w-5 h-4 inline-block mr-1" icon="svgReturn" />
            <span>Store dedication</span>
          </button>
        </div>
        <div class="mt-3 sm:mt-0 sm:ml-3">
          <button
            type="submit"
            class="btn-ochre-extended"
            @click.prevent="skip"
          >
            <span>Skip</span>
          </button>
        </div>
      </div>
    </form>
  </div>
</template>

<script lang="ts">
import { Component, Vue, Action, Getter } from "nuxt-property-decorator"
import { idb } from "@/api"
import { IConversion } from "@/interfaces"

@Component({
  middleware: "refresh-authentication",
})
export default class CreateDedication extends Vue {
  @Getter("conversions/conversionKey") conversionKey
  @Action("collections/storeCollectionPayload") storeConversionPayload

  public conversion: string | IConversion = ""
  public dedication: string = ""

  async created(): Promise<void> {
    // Set description to work
    if (this.conversionKey) {
      // https://stackoverflow.com/a/53813384/295606
      this.conversion = (await idb.getPayload(
        "conversion",
        this.conversionKey
      )) as unknown as IConversion
      this.dedication = this.conversion.dedication
    }
  }

  async updateState(): Promise<void> {
    ;(this.conversion as IConversion).conversionState.dedication = true
    await this.storeConversionPayload({
      collection: "conversion",
      payload: this.conversion,
      key: this.conversionKey,
    })
    this.$router.push("/convert")
  }

  public async submit(): Promise<void> {
    ;(this.conversion as IConversion).dedication = this.dedication
    await this.updateState()
  }

  public async skip(): Promise<void> {
    await this.updateState()
  }

  async asyncData({ store, redirect }): Promise<void> {
    const cKey = await store.getters["conversions/conversionKey"]
    let sameKeys = false
    if (cKey) {
      let [iKey, dKey] = [0, 0]
      if (cKey) iKey = await idb.hasKey("cover", cKey)
      if (cKey) dKey = await idb.hasKey("docx", cKey)
      sameKeys = [1, iKey, dKey].every((val, _i, arr) => val === arr[0])
    }
    if (!cKey) {
      await store.commit("main/addNotification", {
        content: "You haven't described your work yet.",
        color: "error",
      })
      redirect("/convert/description")
    }
    if (!sameKeys) {
      await store.commit("main/addNotification", {
        content: "You haven't uploaded your work yet.",
        color: "error",
      })
      redirect("/convert/upload")
    }
    await store.commit("conversions/setCurrentStep", "dedication")
  }
}
</script>

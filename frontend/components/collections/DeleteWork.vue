<template>
  <div
    v-if="['submitted', 'updated', 'offered'].includes(status)"
    class="flex space-x-4"
  >
    <button
      type="submit"
      class="
        relative
        flex-1
        inline-flex
        items-center
        justify-center
        border border-transparent
        hover:text-gray-500
        focus:outline-none
      "
      @click.prevent="submit"
    >
      <SvgIcon terms="w-5 h-6 text-sinopia-700" icon="svgTrash" /><label
        for="confirmDelete"
        :class="`ml-1 text-sm font-semibold ${
          confirmDelete ? 'text-sinopia-600' : 'text-gray-700'
        } cursor-pointer`"
        >Delete work</label
      >
    </button>
    <input
      id="confirmDelete"
      v-model="confirmDelete"
      aria-describedby="store-description"
      name="confirmDelete"
      type="checkbox"
      class="
        relative
        inline-flex
        items-center
        justify-center
        my-auto
        focus:ring-sinopia-500
        h-4
        w-4
        text-sinopia-600
        border-gray-300
        rounded
      "
    />
  </div>
</template>

<script lang="ts">
import { Component, Action, Prop, Vue } from "nuxt-property-decorator"

@Component
export default class CollectionsDeleteWork extends Vue {
  @Prop(String) readonly workKey!: string
  @Prop(String) readonly status!: string
  @Action("conversions/deleteWork") deleteWork
  public confirmDelete: boolean = false

  async submit() {
    if (
      ["submitted", "updated", "offered"].includes(this.status) &&
      this.confirmDelete
    ) {
      await this.deleteWork(this.workKey)
      this.$router.push("/workshop")
    }
  }
}
</script>

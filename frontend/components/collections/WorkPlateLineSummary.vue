<template>
  <div class="flex flex-col text-center">
    <div class="w-full flex justify-between p-3 space-x-3">
      <div class="flex-1 line-clamp-4">
        <h3 class="mt-1 text-gray-900 text-sm font-semibold truncate">
          {{ summary.work.metadata.title }}
        </h3>
        <p class="mt-1 text-gray-500 text-sm line-clamp-3 md:line-clamp-5">
          {{ summary.work.metadata.description }}
        </p>
      </div>
      <SourcesCoverImage :src="summary.cover.data" />
    </div>
    <div class="m-1 space-x-1 line-clamp-2">
      <span
        v-for="subject in summary.work.metadata.subject"
        :key="`subject-${summary.work.identifier}-${subject.identifier}`"
        class="flex-shrink-0 inline-block px-2 py-0.5 text-woad-800 text-xs font-medium bg-woad-100 rounded-full"
        >{{ subject.term }}</span
      >
    </div>
    <div class="divider -my-1"></div>
    <div class="flex justify-between text-gray-500 text-xs mx-10 md:mx-20">
      <span>Status</span>
      <span class="font-semibold capitalize">{{ summary.work.state }}</span>
    </div>
    <div class="divider -my-1"></div>
    <div class="">
      <div class="-mt-px flex">
        <div class="w-0 flex-1 flex">
          <button
            v-show="summary.work.metadata.uid"
            class="relative -mr-px w-0 flex-1 inline-flex items-center justify-center py-4 text-sm text-gray-700 font-medium border border-transparent rounded-bl-lg hover:text-gray-500"
            @click.prevent="read"
          >
            <SvgIcon terms="w-5 h-5 text-gray-400" icon="svgBookOpen" />
            <span class="ml-3">Read</span>
          </button>
        </div>
        <div class="-ml-px w-0 flex-1 flex">
          <NuxtLink
            :to="`/workshop/${summary.work.metadata.identifier}`"
            class="relative w-0 flex-1 inline-flex items-center justify-center py-4 text-sm text-gray-700 font-medium border border-transparent rounded-br-lg hover:text-gray-500"
          >
            <SvgIcon terms="w-5 h-5 text-gray-400" icon="svgPencilAlt" />
            <span class="ml-3">Review</span>
          </NuxtLink>
        </div>
      </div>
    </div>
  </div>
</template>

<script lang="ts">
import { Component, Prop, Mutation, Vue } from "nuxt-property-decorator"
import { IWorkLineSummary, IDataSource } from "@/interfaces"

@Component
export default class CollectionsWorkPlateLineSummary extends Vue {
  @Mutation("collections/setCollection") setCollection
  @Prop(Object) readonly summary!: {
    work: IWorkLineSummary
    cover: IDataSource
  }

  async read() {
    if (this.summary.work.metadata.uid) {
      await this.setCollection({
        collection: "work",
        key: this.summary.work.metadata.uid,
      })
      await this.setCollection({
        collection: "library",
        key: this.summary.work.metadata.uid,
      })
    }
    this.$router.push("/read")
  }
}
</script>

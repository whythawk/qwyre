<template>
  <div
    class="
      aspect-h-12
      sm:aspect-h-11
      md:aspect-h-14
      lg:aspect-h-16
      xl:aspect-h-11
      aspect-w-10
    "
  >
    <NuxtLink
      :to="`/stream/${result.work}`"
      class="col-span-1 flex flex-col text-center bg-white rounded-lg shadow"
    >
      <div class="w-full flex justify-between p-3 space-x-3">
        <div class="flex-1 line-clamp-5">
          <h3
            class="
              mt-1
              text-ochre-900 text-xs
              sm:text-sm
              font-semibold
              line-clamp-2
            "
          >
            {{ result.title }}
          </h3>
          <p
            class="
              mt-1
              text-ochre-700 text-xs
              sm:text-sm
              italic
              line-clamp-1
              sm:line-clamp-2
            "
          >
            {{ parseStringList(result.creator) }}
          </p>
          <p
            class="
              mt-1
              text-ochre-700 text-xs
              sm:text-sm
              line-clamp-4
              sm:line-clamp-5
            "
          >
            {{ result.description }}
          </p>
        </div>
        <SourcesCoverImage :src="cover.data" />
      </div>
      <div class="m-1 space-x-1 text-ochre-700 text-xs tracking-wide">
        <span v-if="result.isodate">{{ parseISOString(result.isodate) }}</span>
        <span v-if="result.isodate && result.word_count">&</span>
        <span v-if="result.word_count"
          >{{ result.word_count.toLocaleString() }} words</span
        >
      </div>
      <div
        class="
          m-1
          space-x-1
          line-clamp-1
          sm:line-clamp-2
          md:line-clamp-3
          lg:line-clamp-4
        "
      >
        <span
          v-for="(subject, i) in result.subject"
          :key="`subject-${result.work.identifier}-${i}`"
          class="
            flex-shrink-0
            inline-block
            px-2
            py-0.5
            text-woad-800 text-xs
            font-medium
            bg-woad-100
            rounded-full
          "
          >{{ subject }}</span
        >
      </div>
    </NuxtLink>
  </div>
</template>

<script lang="ts">
import { Component, Prop, Watch, Vue } from "nuxt-property-decorator"
import { IDataSource, IWorkSearchSummary } from "@/interfaces"
import { api } from "@/api"

@Component
export default class CollectionsSearchPlateSummary extends Vue {
  @Prop(Object) readonly result!: IWorkSearchSummary
  public cover: IDataSource = {} as IDataSource

  public parseISOString(isodate: string): string {
    // https://stackoverflow.com/a/27013409/295606
    const b = isodate.split(/\D+/).map((x) => +x)
    const d = new Date(Date.UTC(b[0], --b[1], b[2]))
    return `${d.getUTCDate()} ${d.toLocaleString("default", {
      month: "short",
    })} ${d.getUTCFullYear()}`
  }

  public parseStringList(stringList: string[]): string {
    switch (stringList.length) {
      case 0:
        return ""
      case 1:
        return stringList[0]
      case 2:
        return stringList.join(" & ")
      default:
        return `${stringList.slice(0, -1).join(", ")} & ${
          stringList.slice(-1)[0]
        }`
    }
  }

  @Watch("result")
  public async getCoverImage() {
    try {
      const response = await api.getCoverPublic(this.result.work, "thumbnail")
      if (response.data) {
        this.cover = response.data
      }
    } catch (error) {}
  }

  async created() {
    await this.getCoverImage()
  }
}
</script>

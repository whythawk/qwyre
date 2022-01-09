<template>
  <div v-if="work && work.metadata">
    <div class="my-2" v-html="work.metadata.long_description"></div>
    <!-- General metadata table -->
    <table class="table-fixed text-sm w-full">
      <thead>
        <tr>
          <th class="w-1/3"></th>
          <th class="w-2/3"></th>
        </tr>
      </thead>
      <tbody>
        <tr v-show="work.metadata.isodate">
          <td class="font-semibold py-2">Published</td>
          <td class="text-right py-2">
            {{ getReadableDate(work.metadata.isodate) }}
          </td>
        </tr>
        <tr v-show="work.metadata.uid">
          <td class="font-semibold py-2">Identifier (ISBN, UUID)</td>
          <td class="text-right py-2">
            {{ work.metadata.uid }}
          </td>
        </tr>
        <tr v-show="work.metadata.language">
          <td class="font-semibold py-2">Language</td>
          <td class="text-right py-2">{{ work.metadata.language }}</td>
        </tr>
        <tr v-show="work.metadata.subject && work.metadata.subject.length">
          <td class="font-semibold py-2">Subject</td>
          <td class="text-right py-2 space-x-1 space-y-1">
            <span
              v-for="subject in work.metadata.subject"
              :key="`subject-${work.identifier}-${subject.identifier}`"
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
              >{{ subject.term }}</span
            >
          </td>
        </tr>
        <tr v-show="work.metadata.publisher">
          <td class="font-semibold py-2">Publisher</td>
          <td v-if="work.metadata.publisher_uri" class="text-right py-2">
            <a :href="work.metadata.publisher_uri" class="underline">{{
              work.metadata.publisher
            }}</a>
          </td>
          <td v-else class="text-right py-2">
            {{ work.metadata.publisher }}
          </td>
        </tr>
        <tr v-if="work.metadata.word_count">
          <td class="font-semibold py-2">Word count</td>
          <td class="text-right py-2">
            {{ work.metadata.word_count.toLocaleString() }}
          </td>
        </tr>
      </tbody>
    </table>
    <!-- Publication Rights -->
    <p v-show="work.metadata.rights" class="text-xs py-2 italic">
      {{ work.metadata.rights }}
    </p>
    <!-- Contributors -->
    <div v-show="work.metadata.contributor && work.metadata.contributor.length">
      <p class="text-lg font-semibold">Contributors</p>
      <table
        v-for="(contributor, i) in work.metadata.contributor"
        :key="`contributor-table-${i}`"
        class="table-fixed text-sm w-full mt-2"
      >
        <thead>
          <tr>
            <th class="w-1/3"></th>
            <th class="w-2/3"></th>
          </tr>
        </thead>
        <tbody>
          <tr v-if="contributor.name">
            <td class="font-semibold py-0">Name</td>
            <td class="text-right py-0">{{ contributor.name }}</td>
          </tr>
          <tr v-else>
            <td class="font-semibold py-0">Name</td>
            <td class="text-right py-0">
              <a href="" class="underline"
                ><span
                  v-if="contributor.creator && contributor.creator.creator"
                  >{{ contributor.creator.creator }}</span
                >
                <span v-else>Anonymous</span></a
              >
            </td>
          </tr>
          <tr v-show="contributor.role">
            <td class="font-semibold py-0">Role</td>
            <td class="text-right py-0 capitalize">{{ contributor.role }}</td>
          </tr>
          <tr v-show="contributor.terms">
            <td class="font-semibold py-0">Terms</td>
            <td class="text-right py-0">{{ contributor.terms }}</td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
</template>

<script lang="ts">
import { Component, Prop, Vue } from "nuxt-property-decorator"
import { IWorkSummary } from "@/interfaces"
import { readableDate } from "@/utilities"

@Component
export default class CollectionsWorkSummaryMetadataTab extends Vue {
  @Prop(Object) readonly work!: IWorkSummary

  public getReadableDate(dataString: string): string {
    return readableDate(dataString)
  }
}
</script>

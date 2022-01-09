<template>
  <div class="container min-h-screen mx-auto">
    <div class="py-16 mt-16 mx-2 md:mx-0">
      <SearchBar />
    </div>
    <!-- Search results grid -->
    <section
      aria-labelledby="search-results"
      class="max-w-7xl mx-auto overflow-hidden sm:px-6 lg:px-8"
    >
      <h2 id="search-results" class="sr-only">Search Results</h2>
      <div class="grid grid-cols-2 sm:mx-0 md:grid-cols-3 lg:grid-cols-4 gap-2">
        <div
          v-for="result in pagedSearch"
          :key="`search-result-${result.identifier}`"
        >
          <div class="transition ease-in duration-200">
            <CollectionsSearchPlateSummary :result="result" />
          </div>
        </div>
      </div>
    </section>
    <!-- Pagination -->
    <nav
      v-show="totalPages > 1"
      aria-label="Pagination"
      class="
        max-w-7xl
        mx-auto
        px-4
        mt-6
        flex
        justify-between
        text-sm
        font-medium
        text-gray-700
        sm:px-6
        lg:px-8
      "
    >
      <div class="min-w-0 flex-1">
        <a
          disabled="currentPage < 1"
          class="
            inline-flex
            items-center
            px-4
            h-10
            cursor-pointer
            btn-ochre-extended-sm
          "
          @click="currentPage > 1 ? (currentPage -= 1) : (currentPage = 1)"
        >
          Previous
        </a>
      </div>
      <div
        v-for="p in getPageNavigationList"
        :key="`page-item-${p}`"
        class="hidden sm:flex"
      >
        <a
          :class="`inline-flex items-center mx-1 px-2 sm:px-3 h-10 cursor-pointer ${
            p === '...'
              ? 'border-transparent font-semibold text-ochre-500'
              : currentPage === p
              ? 'btn-woad-extended-sm'
              : 'btn-ochre-extended-sm'
          }`"
          @click="p !== '...' ? (currentPage = p) : ''"
        >
          {{ p }}
        </a>
      </div>
      <div class="min-w-0 flex-1 flex justify-end">
        <a
          disabled="currentPage === totalPages"
          class="
            inline-flex
            items-center
            px-4
            h-10
            cursor-pointer
            btn-ochre-extended-sm
          "
          @click="
            currentPage < totalPages
              ? (currentPage += 1)
              : (currentPage = totalPages)
          "
        >
          Next
        </a>
      </div>
    </nav>
  </div>
</template>

<script lang="ts">
import { Component, Getter, Action, Watch, Vue } from "nuxt-property-decorator"
import { getPageNumberNavigation } from "@/utilities"
import { IWorkSearchSummary } from "@/interfaces"

@Component({
  layout: "working",
  middleware: "refresh-authentication",
})
export default class Search extends Vue {
  @Getter("collections/search") searchResults
  @Action("collections/getSearch") getSearch
  public paginationLimit = 8
  public currentPage: number = 1
  public completeSearch: IWorkSearchSummary[] = []
  public pagedSearch: IWorkSearchSummary[] = []

  public get totalPages(): number {
    return Math.ceil((this.searchResults.length + 1) / this.paginationLimit)
  }

  public get getPageNavigationList(): (string | number)[] {
    return getPageNumberNavigation(this.totalPages, this.currentPage)
  }

  @Watch("searchResults")
  public refreshSearchList() {
    this.completeSearch = [...this.searchResults]
  }

  @Watch("currentPage")
  public pageSearchResults() {
    this.getSearchList()
  }

  @Watch("completeSearch")
  public getSearchList() {
    this.pagedSearch = this.completeSearch.slice(
      this.paginationLimit * (this.currentPage - 1),
      this.paginationLimit * this.currentPage
    )
  }

  public async created() {
    if (
      this.$route.query &&
      Object.keys(this.$route.query).length !== 0 &&
      this.$route.query.constructor === Object &&
      this.$route.query.q
    ) {
      await this.getSearch(decodeURIComponent(this.$route.query.q as string))
    } else {
      await this.getSearch("")
    }
  }
}
</script>

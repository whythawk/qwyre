<template>
  <div class="mx-auto">
    <!-- Filters -->
    <section
      aria-labelledby="filter-heading"
      class="relative z-10 grid items-center"
    >
      <h2 id="filter-heading" class="sr-only">Filters</h2>
      <div class="relative col-start-1 row-start-1 py-4">
        <div class="flex max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div class="w-0 flex-1 flex">
            <NuxtLink
              to="/get-streaming"
              class="group inline-flex justify-center text-sm font-medium focus:outline-none text-malachite-600 hover:text-malachite-800"
            >
              <SvgIcon terms="w-5 h-5" icon="svgInformationCircle" />
              <span class="h-5 w-5 ml-1 my-auto">Guide</span>
            </NuxtLink>
          </div>
        </div>
      </div>
      <div class="col-start-1 row-start-1 py-4">
        <div class="flex justify-end max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div class="relative inline-block">
            <div class="flex">
              <button
                id="menu-button"
                type="button"
                class="group inline-flex justify-center text-sm font-medium focus:outline-none text-ochre-600 hover:text-ochre-800"
                aria-expanded="false"
                aria-haspopup="true"
                @click="isFilterOpen = !isFilterOpen"
              >
                Sort
                <SvgIcon
                  terms="h-4 w-4 my-auto text-ochre-600 group-hover:text-ochre-800"
                  icon="svgChevronDown"
                />
              </button>
            </div>
            <transition
              enter-active-class="transition ease-out duration-100"
              enter-class="transform opacity-0 scale-95"
              enter-to-class="transform opacity-100 scale-100"
              leave-active-class="transition ease-in duration-75"
              leave-class="transform opacity-100 scale-100"
              leave-to-class="transform opacity-0 scale-95"
            >
              <div
                v-show="isFilterOpen"
                class="origin-top-right absolute right-0 mt-2 w-40 rounded-md shadow-2xl bg-white ring-1 ring-black ring-opacity-5 focus:outline-none"
                role="menu"
                aria-orientation="vertical"
                aria-labelledby="menu-button"
                tabindex="-1"
              >
                <div
                  v-for="(s, i) in sortOptions"
                  :key="`sort-option-${i}`"
                  class="py-1"
                  role="none"
                >
                  <a
                    id="`sort-option-${i}`"
                    :class="`${
                      s.key === currentSort
                        ? 'font-medium text-ochre-800'
                        : 'text-ochre-500'
                    } block px-4 py-2 text-sm cursor-pointer`"
                    role="menuitem"
                    tabindex="-1"
                    @click.prevent="sortCompleteCollection(s.key)"
                  >
                    {{ s.value }}
                  </a>
                </div>
              </div>
            </transition>
          </div>
        </div>
      </div>
    </section>

    <!-- Works grid -->
    <section
      aria-labelledby="works-heading"
      class="max-w-7xl mx-auto overflow-hidden sm:px-6 lg:px-8"
    >
      <h2 id="works-heading" class="sr-only">Workshop collection</h2>

      <ul class="grid grid-cols-1 sm:mx-0 md:grid-cols-2 gap-2">
        <li
          v-for="summary in pagedCollection"
          :key="`work-summary-${summary.work.identifier}`"
          class="card card-compact bg-base-100 rounded-md shadow-sm h-full"
        >
          <div class="transition ease-in duration-200">
            <CollectionsWorkPlateLineSummary :summary="summary" />
          </div>
        </li>
      </ul>
    </section>

    <!-- Pagination -->
    <nav
      v-show="totalPages > 1"
      aria-label="Pagination"
      class="max-w-7xl mx-auto px-4 mt-6 flex justify-between text-sm font-medium text-gray-700 sm:px-6 lg:px-8"
    >
      <div class="min-w-0 flex-1">
        <a
          disabled="currentPage < 1"
          class="inline-flex items-center px-4 h-10 cursor-pointer btn-ochre-extended-sm"
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
          class="inline-flex items-center px-4 h-10 cursor-pointer btn-ochre-extended-sm"
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
import { Component, Prop, Watch, Getter, Vue } from "nuxt-property-decorator"
import { getPageNumberNavigation } from "@/utilities"
import { IWorkLineSummary, IDataSource } from "@/interfaces"

@Component
export default class CollectionsWorkshopFilteredGrid extends Vue {
  @Prop(Array) readonly workList!: {
    work: IWorkLineSummary
    cover: IDataSource
  }[]

  public isFilterOpen: boolean = false
  public showDelete: boolean = false
  public paginationLimit = 8
  public currentPage: number = 1
  public currentSort: string = "latest"

  public completeCollection: {
    work: IWorkLineSummary
    cover: IDataSource
  }[] = []

  public pagedCollection: {
    work: IWorkLineSummary
    cover: IDataSource
  }[] = []

  public sortOptions = [
    {
      key: "latest",
      value: "Latest",
    },
    {
      key: "title",
      value: "Title",
    },
    {
      key: "status",
      value: "Status",
    },
  ]

  public get totalPages(): number {
    return Math.ceil((this.workList.length + 1) / this.paginationLimit)
  }

  public get getPageNavigationList(): (string | number)[] {
    return getPageNumberNavigation(this.totalPages, this.currentPage)
  }

  public sortCompleteCollection(sortBy: string) {
    this.currentSort = sortBy
    switch (sortBy) {
      case "latest":
        this.completeCollection = this.completeCollection.sort(
          (a, b) =>
            new Date(b.work.created).getTime() -
            new Date(a.work.created).getTime()
        )
        break
      case "title":
        this.completeCollection = this.completeCollection.sort((a, b) =>
          a.work.metadata.title.localeCompare(b.work.metadata.title)
        )
        break
      case "status":
        // https://stackoverflow.com/a/45544166/295606
        this.completeCollection = this.completeCollection.sort((a, b) =>
          a.work.state.localeCompare(b.work.state)
        )
        break
    }
  }

  @Watch("workList")
  public refreshCollectionList() {
    this.getCollectionList()
    this.completeCollection = [...this.workList]
  }

  @Watch("currentPage")
  public pageCollectionList() {
    this.getCollectionList()
  }

  @Watch("completeCollection")
  public getCollectionList() {
    this.pagedCollection = this.completeCollection.slice(
      this.paginationLimit * (this.currentPage - 1),
      this.paginationLimit * this.currentPage
    )
  }

  async mounted() {
    await this.refreshCollectionList()
  }
}
</script>

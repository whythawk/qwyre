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
          <div>
            <button
              type="button"
              :class="`group inline-flex justify-center text-sm font-medium focus:outline-none ${
                showDelete
                  ? 'text-sinopia-700 hover:text-sinopia-900'
                  : 'text-ochre-600 hover:text-ochre-800'
              }`"
              @click="showDelete = !showDelete"
            >
              <SvgIcon terms="h-4 w-4 mr-1 my-auto" icon="svgTrash" />
              Toggle delete
            </button>
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
                class="
                  group
                  inline-flex
                  justify-center
                  text-sm
                  font-medium
                  focus:outline-none
                  text-ochre-600
                  hover:text-ochre-800
                "
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
                class="
                  origin-top-right
                  absolute
                  right-0
                  mt-2
                  w-40
                  rounded-md
                  shadow-2xl
                  bg-white
                  ring-1 ring-black ring-opacity-5
                  focus:outline-none
                "
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
      <h2 id="works-heading" class="sr-only">Reading collection</h2>

      <div class="grid grid-cols-2 sm:mx-0 md:grid-cols-3 lg:grid-cols-4">
        <div v-for="(c, i) in pagedCollection" :key="`library-${c.key}`">
          <div class="transition ease-in duration-200">
            <div v-if="i === 0">
              <CollectionsWorkPlateSummary
                collection="work"
                :collection-key="c.key"
                :show-new="true"
              />
            </div>
            <div v-else>
              <CollectionsWorkPlateSummary
                :collection="c.collection"
                :collection-key="c.key"
                :show-delete="showDelete"
              />
            </div>
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
import { Component, Watch, Getter, Vue } from "nuxt-property-decorator"
import { idb } from "@/api"
import {
  IWork,
  IStream,
  ILibrary,
  IKeyable,
  ICreatorSummary,
} from "@/interfaces"

@Component
export default class CollectionsLibrary extends Vue {
  @Getter("collections/collectionWatcher") collectionWatcher
  public collection: string = "library"
  public isFilterOpen: boolean = false
  public showDelete: boolean = false
  public forceRefresh: boolean = false
  public paginationLimit = 7
  public totalPages: number = 1
  public currentPage: number = 1
  public currentSort: string = "latest"
  public libraryCollection: ILibrary[] = []
  public completeCollection: IKeyable[] = []

  public pagedCollection: IKeyable[] = []

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
      key: "author",
      value: "Author",
    },
    {
      key: "published",
      value: "Published",
    },
  ]

  public disardable: any = {
    key: "disardable_first",
    name: "disardable_first",
    date_created: new Date(),
  }

  public sortCompleteCollection(sortBy: string) {
    this.currentSort = sortBy
    switch (sortBy) {
      case "latest":
        this.completeCollection = this.completeCollection.sort(
          (a, b) => b.created - a.created
        )
        break
      case "published":
        // https://stackoverflow.com/a/45544166/295606
        this.completeCollection = this.completeCollection.sort((a, b) =>
          a.published.localeCompare(b.published)
        )
        break
      case "title":
        this.completeCollection = this.completeCollection.sort((a, b) =>
          a.title.localeCompare(b.title)
        )
        break
      case "author":
        this.completeCollection = this.completeCollection.sort((a, b) =>
          a.author.localeCompare(b.author)
        )
        break
    }
  }

  public get getPageNavigationList() {
    // format: 1 - 1 2 3 ... 8 9 10
    if (this.totalPages === 1) return []
    let navArray: (number | string)[] = []
    if (this.totalPages <= 6) {
      navArray = [...Array(this.totalPages + 1).keys()]
      navArray.shift()
      return navArray
    }
    if (this.currentPage <= 3)
      return [
        1,
        2,
        3,
        "...",
        this.totalPages - 2,
        this.totalPages - 1,
        this.totalPages,
      ]
    if (this.currentPage > 3 && this.currentPage < this.totalPages - 2) {
      navArray = [
        1,
        "...",
        this.currentPage - 1,
        this.currentPage,
        this.currentPage + 1,
        "...",
        this.totalPages,
      ]
      return navArray
    }
    return [1, "...", this.totalPages - 2, this.totalPages - 1, this.totalPages]
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
    // eslint-disable-next-line
    this.pagedCollection.unshift(this.disardable)
  }

  public checkBy(name: string | null): string {
    if (!name) return "Anonymous"
    return name
  }

  public makeAuthorString(authors: ICreatorSummary[]): string {
    if (authors.length === 1) {
      return this.checkBy(authors[0].creator)
    }
    if (authors.length >= 2) {
      const authorList: string[] = []
      for (const author of authors.slice(0, -1))
        authorList.push(this.checkBy(author.creator))
      return `${authorList.join(", ")} &amp; ${this.checkBy(
        authors.slice(-1)[0].creator
      )}`
    }
    return "Anonymous"
  }

  public async refreshCompleteCollection() {
    const completeCollection: IKeyable[] = []
    for (const book of this.libraryCollection) {
      const member = (await idb.getPayload(book.collection, book.key)) as
        | IWork
        | IStream
      member.date_created = book.date_created
      const newMember: IKeyable = {
        key: book.key,
        created: book.date_created,
        collection: book.collection,
        title: member.metadata.title,
        author:
          book.collection === "work"
            ? member.metadata.creator
            : this.makeAuthorString(
                member.metadata.creator as ICreatorSummary[]
              ),
        published: member.metadata.isodate
          ? member.metadata.isodate
          : (member.metadata as any).pubdate,
      }
      completeCollection.push(newMember)
    }
    this.completeCollection = completeCollection
  }

  @Watch("collectionWatcher")
  public async refreshCollection() {
    if (
      this.forceRefresh ||
      (this.collectionWatcher &&
        this.collectionWatcher.split("-")[0] === this.collection)
    ) {
      this.forceRefresh = false
      this.libraryCollection = (await idb.getAllPayloads(
        this.collection
      )) as ILibrary[]
      await this.refreshCompleteCollection()
      this.sortCompleteCollection(this.currentSort)
      this.totalPages = Math.ceil(
        (this.completeCollection.length + 1) / this.paginationLimit
      )
    }
  }

  async mounted() {
    this.forceRefresh = true
    await this.refreshCollection()
  }
}
</script>

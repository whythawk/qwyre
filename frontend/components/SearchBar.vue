<template>
  <div class="container max-w-3xl mx-auto z-40">
    <div class="relative">
      <div class="container max-w-3xl mx-auto">
        <label class="block">
          <span class="flex">
            <span class="inpt-span">
              <SvgIcon terms="inpt-icon text-ochre-400" icon="svgSearch" />
              <input
                id="search-bar"
                v-model="term"
                type="text"
                autocomplete="off"
                class="inpt-text"
                placeholder="Search, or paste a link to an eBook to import it."
                @keyup.prevent="readPress"
                @keyup.enter="submit"
            /></span>
            <button
              type="submit"
              class="btn-woad-extended ml-2 h-10 mt-1"
              @click.prevent="submit"
            >
              <span v-if="workURL">Import</span><span v-else>Search</span>
            </button>
            <button
              class="btn-ochre ml-2 h-10 mt-1"
              @click.prevent="importBook"
            >
              <SvgIcon terms="w-6 h-6 mx-auto my-auto" icon="svgPlus" />
            </button>
          </span>
        </label>
      </div>
      <div
        v-if="showSuggestions && suggestions.length"
        :class="`
          origin-top-left
          z-40
          absolute
          left-12
          mt-2
          w-2/3
          rounded-md
          bg-ochre-50
          ring-ochre-600
          border-ochre-10 border-2
          focus:shadow-lg
          shadow
          animate-fade-in
          focus:outline-none
        `"
        role="list"
        aria-orientation="vertical"
        aria-labelledby="search-bar"
        tabindex="-1"
      >
        <div class="py-1" role="none">
          <div
            v-for="(suggestion, i) in suggestions"
            :key="`suggestion-item-${i}`"
            :class="`
              ${
                highlighted === i
                  ? 'bg-ochre-100 text-ochre-900'
                  : 'text-ochre-700'
              }
              cursor-default
              block
              px-4
              py-2
              text-sm text-left
            `"
            role="listitem"
            tabindex="-1"
            @mouseover="highlighted = i"
            @click="acceptSuggestion(suggestion)"
          >
            {{ suggestion }}
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script lang="ts">
import {
  Component,
  Watch,
  Action,
  Getter,
  mixins,
} from "nuxt-property-decorator"
import importWorkData from "@/mixins/importWorkData"
import { isValidHttpUrl } from "@/utilities"
import { api } from "@/api"

@Component
export default class CollectionsImportLibrary extends mixins(importWorkData) {
  @Action("collections/getSearch") getSearch
  @Getter("main/changeWatcher") changeWatcher
  public term: string = ""
  public suggestions: string[] = []
  public showSuggestions: boolean = false
  public highlighted: number = 0

  public async acceptSuggestion(suggestion: string) {
    this.term = suggestion
    this.suggestions = []
    this.showSuggestions = false
    await this.submit()
  }

  public readPress(press: KeyboardEvent) {
    if (!press.code) return
    if (press.code === "Escape" || this.term === "") {
      this.term = ""
      this.suggestions = []
      this.showSuggestions = false
      this.highlighted = 0
    }
    if (
      press.code.startsWith("Key") ||
      press.code.startsWith("Digit") ||
      ["Backspace", "Delete"].includes(press.code)
    ) {
      this.showSuggestions = true
      this.highlighted = 0
    }
    if (
      this.showSuggestions &&
      press.code === "ArrowDown" &&
      this.highlighted < this.suggestions.length
    )
      this.highlighted += 1
    if (
      this.showSuggestions &&
      press.code === "ArrowUp" &&
      this.highlighted > 0
    )
      this.highlighted -= 1
    if (this.showSuggestions && ["ArrowUp", "ArrowDown"].includes(press.code))
      this.term = this.suggestions[this.highlighted]
  }

  public storeBook() {
    try {
      if (this.blob) {
        this.storeWork(this.blob)
        this.addNotification({
          content: "Successfully imported your epub.",
          color: "success",
        })
      }
    } catch (e) {
      this.addNotification({
        content: "Please import a valid epub.",
        color: "error",
      })
    }
  }

  public async importBook() {
    await this.importWorkFromClick()
    this.storeBook()
  }

  public async importLink() {
    await this.importWorkFromURL()
    this.storeBook()
    this.term = ""
    this.workURL = ""
    history.pushState({}, "", `${this.$route.path}`)
  }

  public async searchResponse() {
    await this.getSearch(this.term)
    this.suggestions = []
    const newRoute: string = `?q=${encodeURIComponent(this.term)}`
    if (this.$route.path === "/") {
      this.$router.push(`/search${newRoute}`)
    } else {
      history.pushState({}, "", `${this.$route.path}${newRoute}`)
    }
  }

  @Watch("term")
  public async termResponse() {
    if (isValidHttpUrl(this.term)) {
      this.workURL = this.term
    } else {
      try {
        if (this.term.length >= 2 && !this.suggestions.includes(this.term)) {
          const response = await api.getSearchSuggestions(this.term)
          if (response.data) {
            this.suggestions = response.data
          }
        }
      } catch (error) {
        this.suggestions = []
      }
    }
  }

  public async submit(): Promise<void> {
    if (this.workURL) {
      await this.importLink()
    } else {
      await this.searchResponse()
    }
  }

  @Watch("changeWatcher")
  public async readMe() {
    if (this.changeWatcher.split("-")[0] === "readme") {
      const term = this.changeWatcher.split("-").slice(1).join("-")
      if (term && isValidHttpUrl(decodeURIComponent(term as string))) {
        this.workURL = decodeURIComponent(term as string)
        await this.importLink()
      }
    }
  }

  async created() {
    if (
      this.$route.query &&
      Object.keys(this.$route.query).length !== 0 &&
      this.$route.query.constructor === Object
    ) {
      if (
        this.$route.query.import &&
        isValidHttpUrl(decodeURIComponent(this.$route.query.import as string))
      ) {
        this.workURL = decodeURIComponent(this.$route.query.import as string)
        await this.importLink()
      } else if (this.$route.query.q) {
        this.term = decodeURIComponent(this.$route.query.q as string)
      }
    }
  }
}
</script>

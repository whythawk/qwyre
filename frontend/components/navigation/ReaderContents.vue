<template>
  <div class="relative max-w-xs sm:max-w-screen-sm mx-auto my-4">
    <div class="overflow-y-auto max-h-40 w-96 min-w-max sm:max-h-56">
      <ul class="-mb-1">
        <li v-for="(content, i) in contents" :key="`content-item-${i}`">
          <div class="relative pb-1 mx-2">
            <span
              class="absolute left-1 -ml-px h-full w-0.5 bg-gray-200"
              aria-hidden="true"
            ></span>
            <button
              class="
                relative
                flex
                items-center
                space-x-3
                pt-1
                focus:outline-none
              "
              @click="
                bookmark.collection === 'work'
                  ? updateCurrentCFI(content.href)
                  : updateStreamPage(i)
              "
            >
              <div>
                <span
                  class="
                    h-2
                    w-2
                    rounded-full
                    bg-ochre-400
                    flex
                    items-center
                    justify-center
                    ring-2 ring-ochre-100
                  "
                >
                </span>
              </div>
              <div>
                <p
                  class="
                    text-xs
                    sm:text-sm
                    text-left
                    max-w-xs
                    sm:max-w-sm
                    pr-10
                    sm:pr-0
                    truncate
                    text-ochre-100
                    hover:text-ochre-400
                  "
                >
                  <span v-if="bookmark.collection === 'work'">{{
                    content.title
                  }}</span>
                  <span v-else>{{ content }}</span>
                </p>
              </div>
            </button>
          </div>
        </li>
      </ul>
    </div>
  </div>
</template>

<script lang="ts">
import {
  Component,
  Vue,
  Getter,
  Action,
  Watch,
  Mutation,
} from "nuxt-property-decorator"
import { IWork, IWorkContents, ILibrary, IStream } from "@/interfaces"
import { idb } from "@/api"
import { generateUUID } from "@/utilities"

@Component
export default class NavigationReaderContents extends Vue {
  @Mutation("main/setWatchReaderCFI") setWatchReaderCFI
  @Action("collections/storeCollectionPayload") storeCollectionPayload
  @Getter("collections/firstCollection") firstCollection
  @Getter("main/changeWatcher") changeWatcher
  public bookmark: ILibrary = {} as ILibrary
  public contents: IWorkContents[] | string[] = []
  public work: IWork = {} as IWork
  public stream: IStream = {} as IStream

  async initialise() {
    const key = await this.firstCollection("library")
    if (key) this.bookmark = (await idb.getPayload("library", key)) as ILibrary
    if (this.bookmark && this.bookmark.collection === "work") {
      this.work = (await idb.getPayload("work", key)) as IWork
      if (this.work.contents && this.work.contents.length)
        this.contents = this.work.contents
    }
    if (this.bookmark && this.bookmark.collection === "stream") {
      this.stream = (await idb.getPayload("stream", key)) as IStream
      if (this.stream.spine && this.stream.spine.length)
        this.contents = this.stream.spine.slice(0, this.stream.stream.length)
    }
  }

  public async updateCurrentCFI(href: string) {
    this.work.currentCFI = href
    await this.storeCollectionPayload({
      collection: "work",
      payload: this.work,
      key: this.work.key,
    })
    await this.setWatchReaderCFI(`contents-${generateUUID()}`)
  }

  public async updateStreamPage(page: number) {
    await this.setWatchReaderCFI(`contents-${page}-${generateUUID()}`)
  }

  @Watch("changeWatcher")
  public async updateStreamContents() {
    const watchResponse = this.changeWatcher.split("-")
    if (watchResponse[0] === "newstream") await this.initialise()
  }
}
</script>

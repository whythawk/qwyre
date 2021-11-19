<template>
  <div class="relative w-full mx-1 lg:w-11/12 lg:mx-auto z-auto">
    <div
      :class="`hidden lg:flex swiper-button-prev swiper-button-prev-${collection} btn-woad -left-3 lg:-left-4 xl:-left-8`"
    >
      <SvgIcon terms="w-6 h-6" icon="svgChevronLeft" />
    </div>
    <div
      :class="`hidden lg:flex swiper-button-next swiper-button-next-${collection} btn-woad -right-3 lg:-right-4 xl:-right-8`"
    >
      <SvgIcon terms="w-6 h-6" icon="svgChevronRight" />
    </div>
    <div :class="`swiper-container swiper-container-${collection}`">
      <div class="swiper-wrapper">
        <div
          v-for="c in collectionList"
          :key="`collection-${collection}-${c.regenKey}`"
          class="swiper-slide block items-center justify-center py-5"
        >
          <div class="transition ease-in duration-200">
            <div v-if="!c.key">
              <div v-if="collection === 'work'" class="aspect-h-16 aspect-w-10">
                <CollectionsImportWork />
              </div>
              <div v-else class="aspect-h-16 aspect-w-10">
                <CollectionsCreate :collection="collection" />
              </div>
            </div>
            <div v-else>
              <CollectionsCover
                :collection="collection"
                :collection-key="c.key"
              />
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script lang="ts">
import {
  Action,
  Component,
  Getter,
  Prop,
  Vue,
  Watch,
} from "nuxt-property-decorator"
import SwiperCore, { Navigation, A11y } from "swiper/core"
import { Swiper } from "swiper/swiper.d"
import { generateUUID } from "@/utilities"
SwiperCore.use([Navigation, A11y])

@Component
export default class CollectionsSwipeLatest extends Vue {
  @Prop(String) readonly collection!: string
  @Action("collections/restoreCollection") restoreCollection
  @Getter("collections/latestCollections") latestCollections
  @Getter("collections/collectionWatcher") collectionWatcher
  public forceRefresh: boolean = false
  public collectionList: { [key: string]: string | null }[] = []

  public swiper: Swiper = {} as Swiper

  @Watch("collectionWatcher")
  public async refreshCollection() {
    if (
      this.forceRefresh ||
      (this.collectionWatcher &&
        this.collectionWatcher.split("-")[0] === this.collection)
    ) {
      this.forceRefresh = false
      // Initialise swiper.js
      this.swiper = new SwiperCore(`.swiper-container-${this.collection}`, {
        slidesPerView: 2.5,
        slidesPerGroup: 1.5,
        slidesOffsetAfter: 5,
        spaceBetween: 4,
        freeMode: true,
        navigation: {
          nextEl: `.swiper-button-next-${this.collection}`,
          prevEl: `.swiper-button-prev-${this.collection}`,
        },
        breakpoints: {
          640: {
            slidesPerView: 3.5,
          },
          768: {
            slidesPerView: 4.5,
          },
          1024: {
            slidesPerView: 5.5,
          },
          1280: {
            slidesPerView: 6.5,
          },
          1536: {
            slidesPerView: 7.5,
          },
        },
      })
      // Initialise the collection
      this.collectionList = this.collectionList.slice(0, 1)
      if (!this.collectionList.length)
        this.collectionList.push({
          key: null,
          regenKey: generateUUID(),
        })
      // Check IDB if nothing in the Vuex store
      if (!this.latestCollections(this.collection).length) {
        await this.restoreCollection({ collection: this.collection })
      }
      for (const key of this.latestCollections(this.collection))
        this.collectionList.push({
          key,
          regenKey: generateUUID(),
        })
      setTimeout(() => {
        this.swiper.update()
      }, 1)
    }
  }

  async mounted() {
    this.forceRefresh = true
    await this.refreshCollection()
  }
}
</script>

<style>
/* @import "~/swiper/swiper.min.css"; */
/** * Swiper 6.8.0 * Most modern mobile touch slider and framework with hardware accelerated transitions * https://swiperjs.com * * Copyright 2014-2021 Vladimir Kharlampidi * * Released under the MIT License * * Released on: July 22, 2021 */
:root {
  --swiper-theme-color: #007aff;
}
.swiper-container {
  margin-left: auto;
  margin-right: auto;
  position: relative;
  overflow: hidden;
  list-style: none;
  padding: 0;
  z-index: 1;
}
.swiper-wrapper {
  position: relative;
  width: 100%;
  height: 100%;
  z-index: 1;
  display: flex;
  transition-property: transform;
  box-sizing: content-box;
}
.swiper-container-android .swiper-slide,
.swiper-wrapper {
  transform: translate3d(0px, 0, 0);
}
.swiper-container-free-mode > .swiper-wrapper {
  transition-timing-function: ease-out;
  margin: 0 auto;
}
.swiper-container-pointer-events {
  touch-action: pan-y;
}
.swiper-container-pointer-events.swiper-container-vertical {
  touch-action: pan-x;
}
.swiper-slide {
  flex-shrink: 0;
  width: 100%;
  height: 100%;
  position: relative;
  transition-property: transform;
}
.swiper-slide-invisible-blank {
  visibility: hidden;
}
.swiper-container-autoheight,
.swiper-container-autoheight .swiper-slide {
  height: auto;
}
.swiper-container-autoheight .swiper-wrapper {
  align-items: flex-start;
  transition-property: transform, height;
}
.swiper-container-css-mode > .swiper-wrapper {
  overflow: auto;
  scrollbar-width: none;
  -ms-overflow-style: none;
}
.swiper-container-css-mode > .swiper-wrapper::-webkit-scrollbar {
  display: none;
}
.swiper-container-css-mode > .swiper-wrapper > .swiper-slide {
  scroll-snap-align: start start;
}
.swiper-container-horizontal.swiper-container-css-mode > .swiper-wrapper {
  scroll-snap-type: x mandatory;
}
.swiper-container-vertical.swiper-container-css-mode > .swiper-wrapper {
  scroll-snap-type: y mandatory;
}
/* @import "~/swiper/components/navigation/navigation.min.css";
 */
:root {
  --swiper-navigation-size: 44px;
}
.swiper-button-next,
.swiper-button-prev {
  position: absolute;
  top: 50%;
  margin-top: calc(0px - (var(--swiper-navigation-size) / 2));
  z-index: 10;
  cursor: pointer;
  align-items: center;
  justify-content: center;
}
.swiper-button-next.swiper-button-disabled,
.swiper-button-prev.swiper-button-disabled {
  opacity: 0.25;
  cursor: auto;
  pointer-events: none;
}
/* @import "~/swiper/components/a11y/a11y.min.css";
 */
.swiper-container .swiper-notification {
  position: absolute;
  left: 0;
  top: 0;
  pointer-events: none;
  opacity: 0;
  z-index: -1000;
}
</style>

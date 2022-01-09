<template>
  <div class="bg-ochre-10 mb-16" aria-labelledby="footer-heading">
    <h2 id="footer-heading" class="sr-only">Footer</h2>
    <div class="max-w-7xl mx-auto py-12 px-4 sm:px-6 lg:py-16 lg:px-8">
      <div class="pb-8 xl:grid xl:grid-cols-5 xl:gap-8">
        <div class="grid grid-cols-2 gap-8 xl:col-span-4">
          <div class="md:grid md:grid-cols-2 md:gap-8">
            <div>
              <h3
                class="
                  text-sm
                  font-semibold
                  text-ochre-400
                  tracking-wider
                  uppercase
                "
              >
                Qwyre.com
              </h3>
              <ul
                v-for="(nav, i) in navigationAbout"
                :key="`footer-about-${i}`"
                role="list"
                class="mt-4 space-y-4"
              >
                <li>
                  <NuxtLink
                    :to="nav.to"
                    class="text-base text-ochre-700 hover:text-ochre-800"
                    >{{ $t(nav.i18n) }}</NuxtLink
                  >
                </li>
              </ul>
            </div>
            <div class="mt-12 md:mt-0">
              <h3
                class="
                  text-sm
                  font-semibold
                  text-ochre-400
                  tracking-wider
                  uppercase
                "
              >
                Sitemap
              </h3>
              <ul
                v-for="(nav, i) in navigationConversion"
                :key="`footer-about-${i}`"
                role="list"
                class="mt-4 space-y-4"
              >
                <li>
                  <NuxtLink
                    :to="nav.to"
                    class="text-base text-ochre-700 hover:text-ochre-800"
                    >{{ $t(nav.i18n) }}</NuxtLink
                  >
                </li>
              </ul>
            </div>
          </div>
          <div class="md:grid md:grid-cols-2 md:gap-8">
            <div>
              <h3
                class="
                  text-sm
                  font-semibold
                  text-ochre-400
                  tracking-wider
                  uppercase
                "
              >
                Roadmap
              </h3>
              <ul
                v-for="(nav, i) in navigationRoadmap"
                :key="`footer-about-${i}`"
                role="list"
                class="mt-4 space-y-4"
              >
                <li>
                  <NuxtLink
                    :to="nav.to"
                    class="text-base text-ochre-700 hover:text-ochre-800"
                    >{{ $t(nav.i18n) }}</NuxtLink
                  >
                </li>
              </ul>
            </div>
          </div>
        </div>
        <div class="mt-12 xl:mt-0">
          <h3
            class="
              text-sm
              font-semibold
              text-ochre-400
              tracking-wider
              uppercase
            "
          >
            Language
          </h3>
          <form class="mt-4 sm:max-w-xs">
            <fieldset class="w-full">
              <label for="language" class="sr-only">Language</label>
              <div class="relative">
                <select
                  v-model="$i18n.locale"
                  class="
                    appearance-none
                    block
                    w-full
                    bg-none
                    py-2
                    pl-3
                    pr-10
                    text-xs
                    font-sans
                    rounded-md
                    border border-woad-600
                    shadow-sm
                    border-none
                    focus:outline-none
                    focus:border-woad-300
                    focus:ring-transparent
                  "
                >
                  <option
                    v-for="lang in $i18n.locales"
                    :key="lang.code"
                    :value="lang.code"
                  >
                    {{ lang.name }}
                  </option>
                </select>

                <div
                  class="
                    pointer-events-none
                    absolute
                    inset-y-0
                    right-0
                    px-2
                    flex
                    items-center
                  "
                >
                  <SvgIcon
                    terms="h-4 w-4 inline-flex text-woad-700"
                    icon="svgChevronDown"
                  />
                </div>
              </div>
            </fieldset>
          </form>
        </div>
      </div>
      <div
        class="
          mt-8
          border-t border-ochre-100
          pt-8
          md:flex md:items-center md:justify-between
        "
      >
        <div class="flex space-x-6 md:order-2">
          <a
            href="https://whythawk.com/"
            rel="nofollow"
            class="text-ochre-600 hover:text-ochre-800"
          >
            <span class="sr-only">Whythawk</span
            ><SvgIcon terms="h-6 w-12" icon="svgWhythawk" />
          </a>
          <a
            href="https://www.grantfortheweb.org/"
            rel="nofollow"
            class="text-ochre-600 hover:text-ochre-800"
          >
            <span class="sr-only">GrantForTheWeb</span
            ><SvgIcon terms="h-5 w-24" icon="svgGrantForTheWeb" />
          </a>
          <a
            href="https://webmonetization.org/"
            rel="nofollow"
            class="text-ochre-600 hover:text-ochre-800"
          >
            <span class="sr-only">Web Monetization</span
            ><SvgIcon terms="h-6 w-6" icon="svgMonetizationStatic" />
          </a>
          <a
            href="https://coil.com/"
            rel="nofollow"
            class="text-ochre-600 hover:text-ochre-800"
          >
            <span class="sr-only">Coil</span
            ><SvgIcon terms="h-4 w-9 pt-1" icon="svgCoilLogo" />
          </a>
        </div>
        <p class="mt-8 text-sm text-ochre-600 md:mt-0 md:order-1">
          Qwyre by
          <a class="text-ochre-700 font-semibold" href="https://whythawk.com"
            >Whythawk</a
          >.
          {{ $t("footer-licence") }}
          <a
            class="text-ochre-700 font-semibold"
            href="https://creativecommons.org/licenses/by/4.0/"
            >Attribution 4.0 International (CC BY 4.0)</a
          >.
        </p>
      </div>
    </div>
  </div>
</template>

<script lang="ts">
import { Component, Vue } from "nuxt-property-decorator"

@Component
export default class FooterBar extends Vue {
  public navigationAbout = [
    { i18n: "about", to: "/about" },
    { i18n: "fees", to: "/fees" },
    { i18n: "footer-rights", to: "/privacy-rights" },
    { i18n: "support", to: "/support-us" },
  ]

  public navigationConversion = [
    { i18n: "guide", to: "/get-started" },
    { i18n: "streaming", to: "/get-streaming" },
    { i18n: "workshop", to: "/workshop" },
    { i18n: "library", to: "/library" },
  ]

  public navigationRoadmap = [
    { i18n: "roadmap", to: "/roadmap" },
    { i18n: "footer-feedback", to: "/contact-us" },
  ]
}
</script>

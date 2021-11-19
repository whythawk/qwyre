<template>
  <div>
    <!-- Standard menu -->
    <div class="relative pt-6 px-4 sm:px-6 lg:px-8 z-50">
      <nav
        class="relative flex items-center justify-between sm:h-10 lg:justify-start"
        aria-label="Global"
      >
        <div class="flex items-center flex-grow flex-shrink-0 lg:flex-grow-0">
          <div class="flex items-center justify-between w-full md:w-auto">
            <NuxtLink
              to="/"
              class="font-medium fill-current text-ochre-700 hover:text-ochre-500"
            >
              <SvgIcon terms="h-10 w-10 fill-current" icon="qwyreLogo" />
            </NuxtLink>
            <div class="-mr-2 flex items-center md:hidden">
              <button
                type="button"
                class="rounded-md p-2 inline-flex items-center justify-center text-ochre-700 hover:text-ochre-500 hover:bg-ochre-100 focus:outline-none focus:ring-2 focus:ring-inset focus:ring-ochre-500"
                aria-expanded="false"
                @click="isOpen = !isOpen"
              >
                <span class="sr-only">Open main menu</span>
                <SvgIcon terms="h-6 w-6" icon="svgMenu" />
              </button>
            </div>
          </div>
        </div>
        <div class="hidden md:block md:ml-10 md:pr-4 md:space-x-8">
          <NuxtLink
            v-for="(nav, i) in navigation"
            :key="`nav-${i}`"
            :to="nav.to"
            class="font-medium text-ochre-800 hover:text-ochre-500"
          >
            <SvgIcon
              v-show="nav.icon"
              :terms="`h-4 w-6 inline-block opacity-60 ${
                nav.iconcolor ? nav.iconcolor : ''
              }`"
              :icon="nav.icon"
            />
            {{ nav.name }}</NuxtLink
          >
          <span v-show="!isLoggedIn">
            <NuxtLink
              class="font-medium text-ochre-500 hover:text-ochre-700"
              to="/login"
              >Sign in</NuxtLink
            >
            |
            <NuxtLink
              class="font-medium text-ochre-800 hover:text-ochre-500"
              to="/join"
              >Join</NuxtLink
            >
          </span>
          <a
            v-show="isLoggedIn"
            class="font-medium text-ochre-800 hover:text-ochre-500"
            @click="logout"
            >Sign out</a
          >
        </div>
      </nav>
    </div>
    <!-- Mobile menu -->
    <transition
      enter-active-class="transition ease-out duration-100"
      enter-class="transform opacity-0 scale-95"
      enter-to-class="transform opacity-100 scale-100"
      leave-active-class="transition ease-in duration-75"
      leave-class="transform opacity-100 scale-100"
      leave-to-class="transform opacity-0 scale-95"
    >
      <div
        v-show="isOpen"
        class="absolute top-0 inset-x-0 p-2 transition transform origin-top-right md:hidden"
      >
        <div
          class="rounded-lg shadow-md bg-ochre-10 ring-1 ring-black ring-opacity-5 overflow-hidden"
        >
          <div class="px-5 pt-4 flex items-center justify-between">
            <div>
              <NuxtLink
                to="/"
                class="font-medium fill-current text-ochre-700 hover:text-ochre-500"
              >
                <SvgIcon terms="h-10 w-10 fill-current" icon="qwyreLogo" />
              </NuxtLink>
            </div>
            <div class="-mr-2">
              <button
                type="button"
                class="bg-ochre-10 rounded-md p-2 inline-flex items-center justify-center text-ochre-700 hover:text-ochre-500 hover:bg-ochre-100 focus:outline-none focus:ring-2 focus:ring-inset focus:ring-woad-500"
                @click="isOpen = !isOpen"
              >
                <span class="sr-only">Close main menu</span>
                <!-- Heroicon name: outline/x -->
                <SvgIcon terms="h-6 w-6" icon="svgX" />
              </button>
            </div>
          </div>
          <div class="px-2 pt-2 pb-3 space-y-1">
            <NuxtLink
              v-for="(nav, i) in navigation"
              :key="`nav-mobile-${i}`"
              :to="nav.to"
              class="block px-3 py-2 rounded-md text-base font-medium text-ochre-800 hover:text-ochre-500"
            >
              <SvgIcon
                v-show="nav.icon"
                :terms="`h-4 w-6 inline-block object-center opacity-60 ${
                  nav.iconcolor ? nav.iconcolor : ''
                }`"
                :icon="nav.icon"
              />
              {{ nav.name }}</NuxtLink
            >
          </div>
          <span
            v-show="!isLoggedIn"
            class="block w-full px-5 py-3 text-center font-medium bg-ochre-50"
          >
            <NuxtLink class="text-ochre-500 hover:bg-ochre-100" to="/login"
              >Sign in</NuxtLink
            >
            |
            <NuxtLink class="text-ochre-800 hover:bg-ochre-100" to="/register"
              >Join</NuxtLink
            >
          </span>
          <a
            v-show="isLoggedIn"
            class="block w-full px-5 py-3 text-center font-medium text-ochre-800 bg-ochre-50 hover:bg-ochre-100"
            @click="logout"
            >Sign out</a
          >
        </div>
      </div>
    </transition>
  </div>
</template>

<script lang="ts">
import { Component, Vue, Getter, Action } from "nuxt-property-decorator"
import { qwyreLogo } from "@/assets/images"

@Component
export default class NavigationBar extends Vue {
  @Getter("main/isLoggedIn") isLoggedIn
  @Action("main/logOut") userLogOut
  public isOpen: boolean = false
  public qwyreLogo: string = qwyreLogo

  public navigation = [
    { name: "Guide", to: "/get-started" },
    { name: "Test-Land", to: "/test-index" },
    { name: "Testing", to: "/testsocket" },
    { name: "Reader", to: "/read" },
    {
      name: "Tip jar",
      to: "/tip-jar",
      icon: "svgCash",
      iconcolor: "text-malachite-700",
    },
  ]

  public async logout() {
    await this.userLogOut()
  }
}
</script>

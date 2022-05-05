<template>
  <div
    class="relative mx-auto p-3 sm:p-6 flex flex-col items-center text-center lg:px-0"
  >
    <div class="w-full flex justify-between px-2 sm:px-16 space-x-3">
      <div class="flex-1">
        <h1 class="text-lg font-semibold text-ochre-800">
          This isn't the end
          <span v-if="streamFields.title">
            of <span class="italic">{{ streamFields.title }}</span>
          </span>
          ...
        </h1>
      </div>
      <div v-if="streamFields.cover">
        <SourcesCoverImage :src="streamFields.cover" />
      </div>
    </div>
    <p v-if="!isLoggedIn" class="mt-2 px-2 sm:px-3 text-md text-ochre-800">
      To continue reading, please:
    </p>
    <ul v-if="!isLoggedIn" class="list-disc text-left px-6 sm:px-8 mt-2">
      <li class="text-md text-ochre-800 underline">
        <NuxtLink to="/login">Sign in, or create an account,</NuxtLink>
      </li>
      <li class="text-md text-ochre-800">
        Subscribe to <span class="font-semibold">Coil</span> to stream per
        second micropayments.
      </li>
    </ul>
    <p v-if="isLoggedIn" class="mt-2 px-2 sm:px-3 text-md text-ochre-800">
      To continue reading, please sign up (or sign in) with
      <span class="font-semibold">Coil</span> to stream per second payments
      directly to authors.
    </p>
    <a class="mt-2 sm:mt-4" :href="uri"
      ><SvgIcon terms="w-56 h-10" icon="svgCoilWhite"
    /></a>
    <p class="mt-2 sm:mt-4 px-2 sm:px-3 text-md text-ochre-800">
      <span class="font-semibold">You control your payments.</span> Read as
      much, or as little, as you like. Stop after two pages and pay only 2.5
      cents, or finish and pay about $2.
    </p>
    <p class="mt-2 px-2 sm:px-3 text-md text-ochre-800">
      <span v-if="streamFields.author">{{ streamFields.author }}</span
      ><span v-else>We</span> will receive
      <span class="font-semibold">36 cents per hour</span> while you stream.
    </p>
    <p class="mt-2 px-2 sm:px-3 text-md text-ochre-800">
      Learn more at these links:
    </p>
    <div class="mt-2 sm:mt-4 inline-flex text-md text-ochre-800">
      <a href="https://www.grantfortheweb.org/" rel="nofollow"
        ><SvgIcon terms="h-8 w-32" icon="svgGrantForTheWeb"
      /></a>
      <a href="https://webmonetization.org/" rel="nofollow" class="ml-6"
        ><SvgIcon terms="h-8 w-8" icon="svgMonetizationStatic"
      /></a>
      <a href="https://coil.com/" rel="nofollow" class="ml-6"
        ><SvgIcon terms="h-7 w-14" icon="svgCoilLogo"
      /></a>
    </div>
  </div>
</template>

<script lang="ts">
import { Component, Vue, Getter, Prop } from "nuxt-property-decorator"
import { IKeyable } from "@/interfaces"

@Component
export default class MonetizationCallSign extends Vue {
  @Prop(String) readonly uri!: String
  @Prop(Object) readonly streamFields!: IKeyable
  @Getter("main/isLoggedIn") isLoggedIn
}
</script>

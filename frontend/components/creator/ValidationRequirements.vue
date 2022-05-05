<template>
  <div>
    <p class="text-gray-500 text-sm font-semibold italic">
      Before you can make offers:
    </p>
    <div v-if="!userProfile.email_validated">
      <p class="my-2 text-gray-500 text-sm">
        Validate your email, or - if you prefer to use a different email address
        -
        <NuxtLink to="/creator/security" class="underline"
          >update your profile</NuxtLink
        >.
      </p>
      <div class="flex mx-auto justify-center my-2">
        <CreatorValidateEmailButton />
      </div>
    </div>
    <div v-if="creatorProfile.isPrivate || !creatorProfile.wallet">
      <p v-if="creatorProfile.isPrivate" class="mt-1 text-gray-500 text-sm">
        You are welcome to remain anonymous, but you'll need to make your
        profile public.
      </p>
      <p v-if="!creatorProfile.wallet" class="mt-1 text-gray-500 text-sm">
        Add your wallet payment pointer to your profile so you can be paid.
      </p>
      <div class="flex mx-auto justify-center my-2">
        <NuxtLink
          to="/creator/edit"
          class="btn-woad-extended-sm flex items-center h-8"
        >
          <SvgIcon terms="w-5 h-4 inline-block mr-1 mb-1" icon="svgPencilAlt" />
          <span class="text-sm">Update profile</span>
        </NuxtLink>
      </div>
    </div>
  </div>
</template>

<script lang="ts">
import { Component, Getter, Vue } from "nuxt-property-decorator"

@Component
export default class CreatorValidationRequirements extends Vue {
  @Getter("main/creatorProfile") creatorProfile
  @Getter("main/userProfile") userProfile
}
</script>

<template>
  <img :src="imgSrc()" :alt="alt" class="inline-block" />
</template>

<script lang="ts">
import { Component, Prop, Vue } from "nuxt-property-decorator"
// https://gilberttanner.com/blog/creating-a-blog-with-nuxt-content#gettingimagestowork
@Component
export default class ContentImage extends Vue {
  @Prop(String) readonly src!: String
  @Prop(String) readonly alt!: String

  public imgSrc() {
    try {
      // const { article } = this.$parent
      // return require(`~/content${article.dir}/images/${this.src}`)
      return require(`~/assets/images/${this.src}`)
    } catch (error) {
      return null
    }
  }
}
</script>

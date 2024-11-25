<template>
  <div>
    <h3>Article List</h3>
    <ArticleListItem 
      v-for="article in store.communities.articles"
      :key="article.id"
      :article="article"
    />
    <p>{{ store.communities }}</p>
    <p></p>
  </div>
</template>

<script setup>
import ArticleListItem from '@/components/ArticleListItem.vue'
import { useCounterStore } from '@/stores/counter'

const store = useCounterStore()
</script>

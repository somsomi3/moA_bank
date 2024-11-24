<template>
  <div>
    <h1>자유게시판</h1>
    <RouterLink :to="{ name: 'CreateView' }">Create</RouterLink>
    <h3>{{ store.communities.community }}</h3>
    <h3>커뮤니티 기본 인덱스 번호 : {{ store.communities.community?.id }}</h3>
    <h3>{{ store.communities.community?.name }} 커뮤니티</h3>
    <ArticleList />
  </div>
</template>

<script setup>
import ArticleList from '@/components/ArticleList.vue'
import { onMounted } from 'vue'
import { useCounterStore } from '@/stores/counter'
import { RouterLink } from 'vue-router'

const store = useCounterStore()

onMounted(() => {
  // mount 되기전에 store에 있는 전체 게시글 요청 함수를 호출
  store.getArticles()
  store.getcommunityid()
})
</script>

<style>

</style>

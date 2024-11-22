<template>
  <header>
    <nav>
      <RouterLink :to="{ name: 'ArticleView' }">커뮤니티</RouterLink> |
      <RouterLink :to="{ name: 'MyPageView' }" >마이페이지</RouterLink> |
      <RouterLink :to="{ name: 'LogInView' }">로그인</RouterLink> | 
      <RouterLink :to="{ name: 'SignUpView' }">회원가입</RouterLink> |
    </nav>
  </header>
</template>

<script setup>
import StartPage from './StartPage.vue';
import { RouterView, RouterLink } from 'vue-router'
import { useCounterStore } from '@/stores/counter'

// const store = useCounterStore()

// const logOut = function () {
//   store.logOut()
// }
</script>

<style scoped>
</style>

<template>
  <header>
    <nav>
      <RouterLink :to="{ name: 'ArticleView' }">커뮤니티</RouterLink> |
      <RouterLink :to="{ name: 'MyPageView' }" >마이페이지</RouterLink> |
      <RouterLink :to="{ name: 'LogInView' }">로그인</RouterLink> | 
      <RouterLink :to="{ name: 'SignUpView' }">회원가입</RouterLink> |
      <a href=""></a>
      <button @click="logOut">로그아웃</button>
    </nav>
  </header>

  <div>
    <h1>커뮤니티 목록</h1>
    <ul>
      <!-- 커뮤니티 1~10번 링크 생성 -->
      <li v-for="id in communities" :key="id">
        <router-link :to="`/articles/${id}`">커뮤니티 {{ id }}로 이동</router-link>
      </li>
    </ul>
  </div>
</template>

<script setup>
import StartPage from './StartPage.vue';
import { RouterView, RouterLink } from 'vue-router'
import { useCounterStore } from '@/stores/counter'
import { ref } from 'vue';
// const store = useCounterStore()
const store = useCounterStore()
const logOut = function () {
  store.logOut()
}

// 커뮤니티 ID 목록 생성 (1~10)
const communities = ref([...Array(10).keys()].map((n) => n + 1));
</script>

<style scoped>
</style>

<template>
  <div id="app">
    <!-- 헤더 -->
    <header>
      <nav>
        <!-- 상단 네비게이션 -->
        <div>
          <!-- <RouterLink :to="{ name: 'SignUpView' }">시작하기</RouterLink> | -->
          <!-- <RouterLink :to="{ name: 'HomePage' }">홈페이지 바로가기</RouterLink> -->
        </div>
      </nav>
    </header>

    <!-- 라우터 뷰 -->
    <main>
      <RouterView />
       <!-- 위에 주석 처리 안하면 두 번 출력됨, -->
    </main>
  </div>
</template>

<script setup>
import { RouterView, RouterLink } from 'vue-router'; // Vue Router 컴포넌트
import SearchProduct from "./views/SearchProductView.vue"; // 검색 컴포넌트
import SearchProductView from './views/SearchProductView.vue';

import { useCounterStore } from '@/stores/counter'
import HomePage from './components/HomePage.vue';

import { ref } from 'vue';
</script>

<style scoped>
/* 기본 레이아웃 스타일 */
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

header {
  background-color: #f8f9fa;
  padding: 10px 20px;
  border-bottom: 1px solid #ddd;
}

nav {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

nav div {
  margin: 5px;
}

main {
  padding: 20px;
}
</style>

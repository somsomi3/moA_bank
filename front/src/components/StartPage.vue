<template>
  <header>
    <nav  v-if="showNav"  >
      <RouterLink :to="{ name: 'HelloView' }" @click="toggleNav">시작하기</RouterLink> |
      <RouterLink :to="{ name: 'HomePage' }" @click="toggleNav">홈페이지 바로가기</RouterLink> |
      
    </nav>
  </header>
  
</template>

<script setup>
import { RouterView, RouterLink } from 'vue-router'
import HomePage from './HomePage.vue';
import { ref } from 'vue';


const showNav = ref(true); // nav 표시 여부 상태

// nav 표시 여부를 토글하는 함수
function toggleNav() {
  showNav.value = !showNav.value; // true <-> false 전환
}
</script>



<style scoped>

</style>
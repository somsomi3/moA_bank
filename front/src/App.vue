<template>
  
  
  
  <header>
    <nav>
      <StartPage />
      <!-- <HomePage /> -->
    </nav>
  </header>
  <!-- <RouterView /> -->
</template>

<script setup>
import { RouterView, RouterLink } from 'vue-router'
import { useCounterStore } from '@/stores/counter'
import StartPage from './components/StartPage.vue';
import HomePage from './components/HomePage.vue';
// const store = useCounterStore()

// const logOut = function () {
//   store.logOut()
// }
</script>

<style scoped>
</style>

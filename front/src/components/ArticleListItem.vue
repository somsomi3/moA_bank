<template>
  <div>
    <h5>{{ article.id }}번 게시글</h5>
    <p>제목 : {{ article.title}}</p>
    <p>내용 : {{ article.content }}</p>
    <RouterLink 
      :to="{ name: 'DetailView', params: { id: article.id } }"  
    >
      자세히 보기
    </RouterLink>
    <hr>
  </div>
</template>

<script setup>
import { RouterLink } from 'vue-router'

defineProps({
  article: Object
})
</script>

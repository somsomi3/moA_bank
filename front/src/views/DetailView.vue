<template>
  <div>
    <h1>Detail</h1>
    <div v-if="store">
      <p>게시글 번호 : {{ store.communities.articles[route.params.id-1].id }}</p>
      <p>제목 : {{ store.communities.articles[route.params.id-1].title }}</p>
      <p>내용 : {{ store.communities.articles[route.params.id-1].content }}</p>
      <p>생성일 : {{ store.communities.articles[route.params.id-1].created_at }}</p>
      <p>{{route.params.id}}</p>
      <router-link to="/">← 돌아가기</router-link>
    </div>
  </div>
</template>

<script setup>
import axios from 'axios'
import { onMounted, ref } from 'vue'
import { useCounterStore } from '@/stores/counter'
import { useRoute, useRouter } from 'vue-router'
import { errorMessages } from 'vue/compiler-sfc';

// 라우터에서 커뮤니티 ID 가져오기
const route = useRoute()
const communityId = route.params.id;


const store = useCounterStore()

const article = ref(null)

// DetailView가 마운트되기전에 DRF로 단일 게시글 조회를 요청 후 응답데이터를 저장
onMounted(() => {
  axios({
    method: 'get',
    url: `${store.API_URL}/communities/${communityId}/articles/list/`,
    headers: {
        Authorization: `Token ${store.token}`
      },
  })
    .then((res) => {
      console.log(res.data)
      
      article.value = res.data
    })
    .catch((err) => {
      console.log(err)
    })
})

</script>

<style>

</style>

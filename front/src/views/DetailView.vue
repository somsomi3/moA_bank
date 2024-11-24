<template>
  <div>
    
    <div v-if="article">
      <h1>{{article.community.name }}</h1>
      <p v-for="perarticle in article.articles">
        <p>
          <p>{{ perarticle.id }}번 게시글</p>
          <p>제목 : {{ perarticle.title }}</p>
          <p>내용 : {{ perarticle.content}}</p>
          <hr>
        </p>
      </p>
      <router-link to="/HomePage">← 돌아가기</router-link>
      <p>{{article}}</p>
    </div>
    <div v-else>
      <p>데이터를 불러오는 중입니다...</p>
    </div>
     <!-- 글 작성하기 버튼 -->
     <p>
      <router-link v-if="canWrite" to="/create">글 작성하기</router-link>
     </p>
     <!-- <p>{{store.communities}}</p> -->
     <p>{{store}}</p>
  </div>


</template>

<script setup>
import axios from 'axios'
import { onMounted, ref } from 'vue'
import { useCounterStore } from '@/stores/counter'
import { useRoute, useRouter } from 'vue-router'
import { errorMessages } from 'vue/compiler-sfc';
import CreateView from './CreateView.vue';
import { computed } from 'vue';

// 라우터에서 커뮤니티 ID 가져오기
const route = useRoute()
const communityId = parseInt(route.params.id);
const store = useCounterStore()
const article = ref(null)
const canWrite = ref(false)

// 현재 커뮤니티 인덱스와 store.communities.community.id 비교
const check = function () {
  const community = store.communities?.community; // store.communities에서 community 키 확인
  if (!community) {
    console.warn("No community data available in store.communities");
    canWrite.value = false;
    return;
  }

  if (communityId == 1 && [1, 2, 3, 4].includes(store.communities.community?.decile)) {
    canWrite.value = true;
  } else if (communityId == 2 && [5, 6, 7, 8].includes(store.communities.community?.decile)) {
    canWrite.value = true;
  } else if (communityId == 3 && [9, 10].includes(store.communities.community?.decile)) {
    canWrite.value = true;
  } else {
    canWrite.value = false;
  }
};


// DetailView가 마운트되기전에 DRF로 단일 게시글 조회를 요청 후 응답데이터를 저장
onMounted(() => {
  console.log(communityId)
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
      check()
    })
    .catch((err) => {
      console.log(err)
    })
})

</script>

<style>

</style>

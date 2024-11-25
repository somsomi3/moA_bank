<template>
  <div>
    <!-- 게시글 데이터가 있을 때 -->
    <div v-if="article">
      <h1>{{ article.community.name }}</h1>
      <div v-for="perarticle in article.articles" :key="perarticle.id">
        <p>{{ perarticle.id }}번 게시글</p>
        <p>제목 : {{ perarticle.title }}</p>
        <p>내용 : {{ perarticle.content }}</p>
        <hr>
      </div>
      <router-link to="/HomePage">← 돌아가기</router-link>
    </div>
    <!-- 게시글 데이터가 없을 때 -->
    <div v-else>
      <p>데이터를 불러오는 중입니다...</p>
    </div>
    <!-- 글 작성하기 버튼 -->
    <p>
      <router-link v-if="canWrite" to="/create">글 작성하기</router-link>
    </p>
  </div>
</template>

<script setup>
import axios from "axios";
import { onMounted, ref } from "vue";
import { useCounterStore } from "@/stores/counter";
import { useRoute } from "vue-router";

// Pinia 스토어 및 라우터 설정
const store = useCounterStore();
const route = useRoute();
const communityId = parseInt(route.params.id, 10);

// 로컬 상태
const article = ref(null); // 게시글 데이터
const canWrite = ref(false); // 작성 권한

// 작성 권한 체크 함수
const checkWritePermission = () => {
  const userDecile = store.userDecile; // 사용자 decile 값
  if (!userDecile) {
    console.warn("사용자 decile 정보가 없습니다.");
    canWrite.value = false;
    return;
  }

  // communityId와 decile 값을 기반으로 작성 권한 확인
  if (
    (communityId === 1 && [1, 2, 3, 4].includes(userDecile)) ||
    (communityId === 2 && [5, 6, 7, 8].includes(userDecile)) ||
    (communityId === 3 && [9, 10].includes(userDecile))
  ) {
    canWrite.value = true;
  } else {
    canWrite.value = false;
  }
};

// 게시글 데이터 가져오기
const fetchArticle = async () => {
  try {
    const response = await axios.get(`${store.API_URL}/communities/${communityId}/articles/list/`, {
      headers: {
        Authorization: `Token ${store.token}`,
      },
    });
    article.value = response.data; // 게시글 데이터 저장
    console.log("게시글 데이터:", article.value);
    checkWritePermission(); // 작성 권한 체크
  } catch (err) {
    console.error("게시글 데이터 가져오기 실패:", err);
  }
};

// 컴포넌트 마운트 시 실행
onMounted(async () => {
  await store.fetchUserDecile(); // 사용자 decile 정보 가져오기
  fetchArticle(); // 게시글 데이터 가져오기
});
</script>

<style>
/* 스타일은 필요에 따라 추가 */
</style>

<style>

</style>

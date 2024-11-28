<template>
  <div class="article-container">
    <!-- 데이터가 있을 때 -->
    <div v-if="article">
      <h1 class="community-title">{{ article.community.name }}</h1>

      <!-- 게시글 반복 -->
      <div v-for="perarticle in article.articles" :key="perarticle.id" class="article-item">
        <p class="article-id">{{ perarticle.id }}번 게시글</p>
        <p class="article-title"><strong>제목:</strong> {{ perarticle.title }}</p>
        <p class="article-content"><strong>내용:</strong> {{ perarticle.content }}</p>
        <RouterLink
          :to="{ 
            name: 'ArticleListItem2', 
            params: { id: perarticle.id }, 
            query: { community_id: communityId } 
          }"
          class="detail-link"
        >
          게시글 상세 보기
        </RouterLink>
      </div>

      <!-- 돌아가기 링크 -->
      <router-link to="/" class="back-link">← 돌아가기</router-link>
    </div>

    <!-- 데이터 로딩 중 -->
    <div v-else>
      <p class="loading-message">데이터를 불러오는 중입니다...</p>
    </div>

    <!-- 글 작성하기 버튼 -->
    <p v-if="canWrite" class="write-button-container">
      <router-link to="/create" class="write-button">글 작성하기</router-link>
    </p>
  </div>
</template>

<script setup>
import axios from "axios";
import { onMounted, ref } from "vue";
import { useCounterStore } from "@/stores/counter";
import { useRoute } from "vue-router";

const store = useCounterStore();
const route = useRoute();
const communityId = parseInt(route.params.id);
let tempdecile;

// 로컬 상태
const article = ref(null);
const canWrite = ref(false);

// 작성 권한 체크 함수
const checkWritePermission = () => {
  const userDecile = store.userDecile;
  tempdecile = userDecile;
  if (!userDecile) {
    console.warn("사용자 decile 정보가 없습니다.");
    canWrite.value = false;
    return;
  }

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
    article.value = response.data;
    checkWritePermission();
  } catch (err) {
    console.error("게시글 데이터 가져오기 실패:", err);
  }
};

// 컴포넌트 마운트 시 실행
onMounted(async () => {
  await store.fetchUserDecile();
  fetchArticle();
});
</script>

<style scoped>
/* 전체 컨테이너 스타일 */
.article-container {
  max-width: 800px;
  margin: 0 auto;
  padding: 20px;
  font-family: 'Noto Sans KR', Arial, sans-serif;
}

/* 커뮤니티 제목 */
.community-title {
  font-size: 24px;
  font-weight: bold;
  color: #005bac;
  margin-bottom: 20px;
  text-align: center;
}

/* 게시글 아이템 */
.article-item {
  padding: 15px;
  margin-bottom: 15px;
  border: 1px solid #ddd;
  border-radius: 8px;
  background-color: #f9f9f9;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
}

.article-id {
  font-size: 14px;
  color: #666;
}

.article-title {
  font-size: 18px;
  font-weight: bold;
  color: #333;
  margin-bottom: 5px;
}

.article-content {
  font-size: 16px;
  color: #555;
  margin-bottom: 10px;
}

.detail-link {
  font-size: 14px;
  color: #005bac;
  text-decoration: underline;
  cursor: pointer;
}

.detail-link:hover {
  color: #003d80;
}

/* 로딩 메시지 */
.loading-message {
  text-align: center;
  font-size: 16px;
  color: #888;
}

/* 돌아가기 링크 */
.back-link {
  display: inline-block;
  margin-top: 10px;
  font-size: 14px;
  color: #005bac;
  text-decoration: underline;
  cursor: pointer;
}

.back-link:hover {
  color: #003d80;
}

/* 글 작성하기 버튼 */
.write-button-container {
  text-align: center;
  margin-top: 20px;
}

.write-button {
  display: inline-block;
  padding: 10px 20px;
  font-size: 16px;
  font-weight: bold;
  color: #ffffff;
  background-color: #4c8a81;
  border: none;
  border-radius: 8px;
  text-decoration: none;
  cursor: pointer;
  transition: all 0.3s ease;
}

.write-button:hover {
  background-color: #3e7066;
}
</style>

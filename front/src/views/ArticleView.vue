<template>
  <div class="board-container">
    <h1 class="board-title">자유게시판</h1>
    <RouterLink :to="{ name: 'CreateView2' }" class="create-button">새 글 작성</RouterLink>
    <ArticleList />
  </div>
</template>

<script setup>
import ArticleList from '@/components/ArticleList.vue';
import { onMounted } from 'vue';
import { useCounterStore } from '@/stores/counter';
import { RouterLink } from 'vue-router';

const store = useCounterStore();

onMounted(() => {
  store.getArticles(); // 전체 게시글 요청
  store.getcommunityid(); // 커뮤니티 ID 요청
});
</script>

<style scoped>
/* 전체 컨테이너 스타일 */
.board-container {
  max-width: 800px;
  margin: 0 auto;
  padding: 20px;
  font-family: 'Noto Sans KR', Arial, sans-serif;
  background-color: #f8f9fa;
  border-radius: 12px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
}

/* 제목 스타일 */
.board-title {
  font-size: 24px;
  font-weight: bold;
  color: #005bac; /* 금융 블루 */
  text-align: center;
  margin-bottom: 20px;
}

/* 새 글 작성 버튼 */
.create-button {
  display: inline-block;
  margin-bottom: 20px;
  padding: 10px 20px;
  font-size: 16px;
  font-weight: bold;
  color: #ffffff;
  background-color: #4c8a81;
  border-radius: 8px;
  text-decoration: none;
  text-align: center;
  cursor: pointer;
  transition: all 0.3s ease;
}

.create-button:hover {
  background-color: #3e7066;
}

/* ArticleList 컴포넌트 스타일 조정 (공통 적용 가능) */
.article-item {
  padding: 15px;
  margin-bottom: 15px;
  border: 1px solid #ddd;
  border-radius: 8px;
  background-color: #ffffff;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
}

.article-title {
  font-size: 18px;
  font-weight: bold;
  color: #333;
}

.article-content {
  font-size: 14px;
  color: #555;
}

.article-detail-link {
  font-size: 14px;
  color: #005bac;
  text-decoration: underline;
  cursor: pointer;
}

.article-detail-link:hover {
  color: #003d80;
}
</style>

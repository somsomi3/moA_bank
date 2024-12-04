<template>
  <div class="survey-container">
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
  display: flex; /* 왼쪽과 오른쪽 박스를 가로로 배치 */
  align-items: center; /* 수직 중앙 정렬 */
  justify-content: center; /* 전체 컨테이너 중앙 정렬 */
  gap: 20px; /* 왼쪽과 오른쪽 박스 간격 */
  width: 100%;
  padding: 20px;
  box-sizing: border-box;
}

.survey-container {
  flex: 2;
  display: flex;
  flex-direction: column; /* 세로 방향 배치 */
  align-items: center; /* 중앙 정렬 */
  justify-content: flex-start; /* 위쪽에 맞춤 */
  border: 2px solid #ddd;
  border-radius: 10px;
  width: 600px; /* 고정된 너비 */
  height: 900px; /* 고정된 높이 */
  margin: 0 auto; /* 화면 중앙 정렬 */
  background-color: #8db4ae; /* 흰색 배경 */
  padding: 20px;
  box-sizing: border-box; /* 패딩을 포함한 박스 크기 계산 */
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

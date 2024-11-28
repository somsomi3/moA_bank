<template>
  <div class="article-list-container">
    <h3 class="article-list-title">게시글 목록</h3>
    <!-- 게시글 목록 -->
    <div
      v-for="eacharticle in article?.articles"
      :key="eacharticle.id"
      class="article-item"
    >
      <p><strong>번호:</strong> {{ eacharticle.id }}</p>
      <p><strong>제목:</strong> {{ eacharticle.title }}</p>
      <p><strong>내용:</strong> {{ eacharticle.content }}</p>
      <p><strong>생성일:</strong> {{ eacharticle.created_at }}</p>
      <div class="article-actions">
        <RouterLink
          :to="{ name: 'ArticleListItem', params: { id: eacharticle.id } }"
          class="action-link"
        >
          자세히 보기
        </RouterLink>
        <button @click="editArticle(eacharticle.id)" class="action-button">
          수정
        </button>
        <button @click="deleteArticle(eacharticle.id)" class="action-button delete">
          삭제
        </button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { useCounterStore } from "@/stores/counter";
import axios from "axios";
import { onMounted, ref } from "vue";
import { useRouter } from "vue-router";

const store = useCounterStore();
const router = useRouter();

const article = ref(null); // 게시글 데이터

// 게시글 데이터 가져오기
const fetchArticle = async () => {
  try {
    console.log(store.token, "토큰값");
    const response = await axios.get(
      `${store.API_URL}/communities/4/articles/list/`,
      {
        headers: {
          Authorization: `Token ${store.token}`,
        },
      }
    );
    article.value = response.data; // 게시글 데이터 저장
    console.log("게시글 데이터:", article.value);
  } catch (err) {
    console.error("게시글 데이터 가져오기 실패:", err);
  }
};

// 게시글 수정
const editArticle = (articleId) => {
  router.push({ name: "ArticleEdit", params: { id: articleId } });
};

// 게시글 삭제
const deleteArticle = async (articleId) => {
  if (confirm("정말로 이 게시글을 삭제하시겠습니까?")) {
    try {
      await axios.delete(
        `${store.API_URL}/communities/4/articles/${articleId}/`,
        {
          headers: {
            Authorization: `Token ${store.token}`,
          },
        }
      );
      article.value.articles = article.value.articles.filter(
        (eacharticle) => eacharticle.id !== articleId
      );
      alert("게시글이 삭제되었습니다.");
    } catch (err) {
      console.error("게시글 삭제 실패:", err);
      alert("게시글 삭제에 실패했습니다.");
    }
  }
};

// 컴포넌트 마운트 시 실행
onMounted(async () => {
  await store.fetchUserDecile();
  fetchArticle();
});
</script>

<style scoped>
/* 전체 컨테이너 */
.article-list-container {
  max-width: 800px;
  margin: 40px auto;
  padding: 20px;
  background-color: #f8f9fa;
  border-radius: 12px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
  font-family: "Noto Sans KR", Arial, sans-serif;
}

/* 제목 스타일 */
.article-list-title {
  font-size: 24px;
  font-weight: bold;
  color: #005bac; /* 금융 블루 */
  text-align: center;
  margin-bottom: 20px;
}

/* 게시글 아이템 스타일 */
.article-item {
  background-color: #ffffff;
  padding: 20px;
  margin-bottom: 20px;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

/* 강조 텍스트 */
.article-item p {
  margin: 10px 0;
  font-size: 16px;
  color: #333;
}

/* 액션 영역 */
.article-actions {
  margin-top: 20px;
  display: flex;
  gap: 10px;
  flex-wrap: wrap;
}

/* 링크 스타일 */
.action-link {
  text-decoration: none;
  color: #005bac;
  font-weight: bold;
  transition: color 0.3s;
}

.action-link:hover {
  color: #003060;
}

/* 버튼 스타일 */
.action-button {
  padding: 8px 16px;
  font-size: 14px;
  font-weight: bold;
  color: #ffffff;
  background-color: #4c8a81;
  border: none;
  border-radius: 8px;
  cursor: pointer;
  transition: background-color 0.3s ease, transform 0.2s ease;
}

.action-button:hover {
  background-color: #3e7066;
}

.action-button:active {
  transform: scale(0.97);
}

.action-button.delete {
  background-color: #e63946; /* 삭제 버튼 빨간색 */
}

.action-button.delete:hover {
  background-color: #c92a2a;
}
</style>

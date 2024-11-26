<template>
  <div class="article-form-container">
    <h1 class="form-title">게시글 작성</h1>
    <form @submit.prevent="createArticle" class="article-form">
      <!-- 제목 입력 -->
      <div class="form-group">
        <label for="title" class="form-label">제목 :</label>
        <input
          type="text"
          id="title"
          v-model.trim="title"
          class="form-input"
          placeholder="제목을 입력하세요"
        />
      </div>
      <!-- 내용 입력 -->
      <div class="form-group">
        <label for="content" class="form-label">내용 :</label>
        <textarea
          id="content"
          v-model.trim="content"
          class="form-textarea"
          placeholder="내용을 입력하세요"
        ></textarea>
      </div>
      <!-- 제출 버튼 -->
      <button type="submit" class="submit-button">게시글 작성</button>
    </form>
    
  </div>
</template>

<script setup>
import { ref } from "vue";
import { useCounterStore } from "@/stores/counter";
import axios from "axios";
import { useRouter } from "vue-router";

const title = ref("");
const content = ref("");
const store = useCounterStore();
const router = useRouter();

const createArticle = function () {
  axios({
    method: "post",
    url: `${store.API_URL}/communities/${store.communities.community.id}/articles/create/`,
    data: {
      title: title.value,
      content: content.value,
      community: store.communities.community.id,
    },
    headers: {
      Authorization: `Token ${store.token}`,
    },
  })
    .then(() => {
      router.push({
        name: "DetailView",
        params: { id: store.communities.community.id },
      });
    })
    .catch((err) => {
      console.log(err);
    });
};
</script>

<style scoped>
/* 전체 컨테이너 */
.article-form-container {
  max-width: 600px;
  margin: 40px auto;
  padding: 20px;
  font-family: "Noto Sans KR", Arial, sans-serif;
  background-color: #f8f9fa;
  border-radius: 12px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
}

/* 제목 */
.form-title {
  font-size: 24px;
  font-weight: bold;
  color: #005bac; /* 금융 블루 */
  text-align: center;
  margin-bottom: 20px;
}

/* 폼 그룹 */
.form-group {
  margin-bottom: 20px;
}

/* 라벨 */
.form-label {
  display: block;
  font-size: 16px;
  color: #333;
  margin-bottom: 8px;
}

/* 텍스트 입력 */
.form-input {
  width: 100%;
  padding: 10px;
  font-size: 16px;
  border: 1px solid #ced4da;
  border-radius: 8px;
  background-color: #ffffff;
  transition: border-color 0.3s ease;
}

.form-input:focus {
  border-color: #005bac;
  outline: none;
}

/* 텍스트 영역 */
.form-textarea {
  width: 100%;
  padding: 10px;
  font-size: 16px;
  border: 1px solid #ced4da;
  border-radius: 8px;
  background-color: #ffffff;
  transition: border-color 0.3s ease;
  resize: vertical;
  min-height: 150px;
}

.form-textarea:focus {
  border-color: #005bac;
  outline: none;
}

/* 제출 버튼 */
.submit-button {
  display: block;
  width: 100%;
  padding: 12px 20px;
  font-size: 16px;
  font-weight: bold;
  color: #ffffff;
  background-color: #4c8a81;
  border: none;
  border-radius: 8px;
  cursor: pointer;
  transition: all 0.3s ease;
}

.submit-button:hover {
  background-color: #3e7066;
}

.submit-button:active {
  transform: scale(0.98);
}

/* 디버그 정보 */
.debug-info {
  margin-top: 20px;
  font-size: 14px;
  color: #999999;
  text-align: center;
}
</style>

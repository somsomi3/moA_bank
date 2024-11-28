<template>
  <div>
    <h3>게시글 수정</h3>
    <form @submit.prevent="updateArticle">
      <div>
        <label for="title">제목</label>
        <input
          type="text"
          id="title"
          v-model="article.title"
          required
        />
      </div>
      <div>
        <label for="content">내용</label>
        <textarea
          id="content"
          v-model="article.content"
          rows="5"
          required
        ></textarea>
      </div>
      <button type="submit">수정 완료</button>
      <button @click.prevent="goBack">취소</button>
    </form>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import { useRoute, useRouter } from 'vue-router';
import axios from 'axios';
import { useCounterStore } from '@/stores/counter';

const store = useCounterStore();
const route = useRoute();
const router = useRouter();
const article = ref({
  title: '',
  content: '',
});

// 게시글 데이터 가져오기
const fetchArticle = async () => {
  try {
    const response = await axios.get(
      `${store.API_URL}/communities/4/articles/${route.params.id}/`,
      {
        headers: {
          Authorization: `Token ${store.token}`,
        },
      }
    );
    article.value = response.data.article;
  } catch (err) {
    console.error('게시글 데이터 가져오기 실패:', err);
    alert('게시글을 불러오는 데 실패했습니다.');
  }
};

// 게시글 수정
const updateArticle = async () => {
  try {
    await axios.put(
      `${store.API_URL}/communities/4/articles/${route.params.id}/`,
      article.value,
      {
        headers: {
          Authorization: `Token ${store.token}`,
        },
      }
    );
    alert('게시글이 수정되었습니다.');
    router.push({ name: 'ArticleList' }); // 게시글 목록으로 이동
  } catch (err) {
    console.error('게시글 수정 실패:', err);
    alert('게시글 수정에 실패했습니다.');
  }
};

// 취소 버튼 클릭 시 이전 페이지로 이동
const goBack = () => {
  router.back();
};

// 컴포넌트 마운트 시 실행
onMounted(fetchArticle);
</script>

<style scoped>
form {
  max-width: 600px;
  margin: auto;
}
div {
  margin-bottom: 15px;
}
label {
  display: block;
  font-weight: bold;
  margin-bottom: 5px;
}
input,
textarea {
  width: 100%;
  padding: 8px;
  box-sizing: border-box;
}
button {
  margin-right: 10px;
  padding: 10px 15px;
  cursor: pointer;
}
</style>

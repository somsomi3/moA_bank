<template>
  <div>
    <h3>Article List</h3>
    
    <div v-for="eacharticle in article?.articles" :key="eacharticle.id">
      <p>번호: {{ eacharticle.id }}</p>
      <p>제목: {{ eacharticle.title }}</p>
      <p>내용: {{ eacharticle.content }}</p>
      <p>생성일: {{ eacharticle.created_at }}</p>
      <RouterLink :to="{ name: 'ArticleListItem', params: { id: eacharticle.id } }">
        자세히 보기
      </RouterLink>
      <!-- 수정 및 삭제 버튼 -->
      <button @click="editArticle(eacharticle.id)">수정</button>
      <button @click="deleteArticle(eacharticle.id)">삭제</button>
      <hr />
    </div>
  </div>
</template>

<script setup>
import { useCounterStore } from '@/stores/counter';
import axios from 'axios';
import { onMounted, ref } from 'vue';
import { useRouter } from 'vue-router';

const store = useCounterStore();
const router = useRouter();

const article = ref(null); // 게시글 데이터

// 게시글 데이터 가져오기
const fetchArticle = async () => {
  try {
    console.log(store.token, '토큰값');
    const response = await axios.get(`${store.API_URL}/communities/4/articles/list/`, {
      headers: {
        Authorization: `Token ${store.token}`,
      },
    });
    article.value = response.data; // 게시글 데이터 저장
    console.log('게시글 데이터:', article.value);
  } catch (err) {
    console.error('게시글 데이터 가져오기 실패:', err);
  }
};

// 게시글 수정
const editArticle = (articleId) => {
  // 수정 페이지로 이동
  router.push({ name: 'ArticleEdit', params: { id: articleId } });
};

// 게시글 삭제
const deleteArticle = async (articleId) => {
  if (confirm('정말로 이 게시글을 삭제하시겠습니까?')) {
    try {
      await axios.delete(`${store.API_URL}/communities/4/articles/${articleId}/`, {
        headers: {
          Authorization: `Token ${store.token}`,
        },
      });
      // 삭제 성공 시 목록에서 해당 게시글 제거
      article.value.articles = article.value.articles.filter(
        (eacharticle) => eacharticle.id !== articleId
      );
      alert('게시글이 삭제되었습니다.');
    } catch (err) {
      console.error('게시글 삭제 실패:', err);
      alert('게시글 삭제에 실패했습니다.');
    }
  }
};

// 컴포넌트 마운트 시 실행
onMounted(async () => {
  await store.fetchUserDecile(); // 사용자 decile 정보 가져오기
  fetchArticle(); // 게시글 데이터 가져오기
});
</script>

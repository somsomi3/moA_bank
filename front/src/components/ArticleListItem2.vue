<template>
  <div>
    <h3>게시글 상세 보기</h3>
    <p>글번호: {{ article?.id }}</p>
    <p>제목: {{ article?.title }}</p>
    <p>조회수: {{ article?.viewscount }}</p>
    <p>생성일: {{ article?.created_at }}</p>
    <p>수정일: {{ article?.updated_at }}</p>
    <p>작성자: {{ article?.user }}</p>

    <!-- 댓글 목록 -->
    <div>
      <h4>댓글</h4>
      <div v-if="comments.length > 0">
        <div v-for="comment in comments" :key="comment.id" class="comment-item">
          <p><strong>{{ comment.user }}</strong>: {{ comment.content }}</p>
          <p class="comment-meta">작성일: {{ comment.created_at }}</p>
          <hr />
        </div>
      </div>
      <div v-else>
        <p>댓글이 없습니다. 첫 번째 댓글을 작성해보세요!</p>
      </div>
    </div>

    <!-- 댓글 작성 -->
    <div class="comment-form">
      <h4>댓글 작성</h4>
      <textarea v-model="newComment" placeholder="댓글을 입력하세요..." rows="3"></textarea>
      <button @click="submitComment">댓글 등록</button>
    </div>
  </div>
</template>

<script setup>
import { ref, watch, onMounted } from 'vue';
import { useRoute } from 'vue-router';
import axios from 'axios';
import { useCounterStore } from '@/stores/counter';

const store = useCounterStore();
const route = useRoute();

// 게시글, 댓글 데이터 및 새 댓글 작성 상태
const article = ref(null);
const comments = ref([]);
const newComment = ref('');
const communityId = ref(route.query.community_id);

// watch로 communityId 반응형 관리
watch(() => route.query.community_id, (newVal) => {
  communityId.value = newVal;
});

// 게시글 및 댓글 가져오기
const fetchArticleAndComments = async () => {
  if (!communityId.value) {
    console.error('communityId가 없습니다.');
    return;
  }
  try {
    const response = await axios.get(
      `${store.API_URL}/communities/${communityId.value}/articles/${route.params.id}/`,
      {
        headers: {
          Authorization: `Token ${store.token}`,
        },
      }
    );
    article.value = response.data.article;
    comments.value = response.data.comments;
  } catch (err) {
    console.error('게시글 및 댓글 데이터 가져오기 실패:', err);
  }
};

// 댓글 작성
const submitComment = async () => {
  if (!newComment.value.trim()) {
    alert('댓글 내용을 입력하세요.');
    return;
  }
  try {
    console.log('Community ID:', communityId.value);
console.log('Article ID:', route.params.id);
console.log('API URL:', store.API_URL);
console.log('Token:', store.token);

    const response = await axios.post(
      `${store.API_URL}/communities/${communityId.value}/articles/${route.params.id}/`,
      { content: newComment.value },
      {
        headers: {
          Authorization: `Token ${store.token}`,
          'Content-Type': 'application/json',
        },
      }
    );
    // 작성한 댓글을 목록에 추가
    comments.value.push(response.data);
    newComment.value = ''; // 입력창 초기화
  } catch (err) {
    console.error('댓글 작성 실패:', err);
  }
};

// 컴포넌트가 마운트되면 게시글 및 댓글 가져오기
onMounted(fetchArticleAndComments);
</script>

<style scoped>
.comment-item {
  margin-bottom: 10px;
}

.comment-meta {
  font-size: 0.9em;
  color: gray;
}

.comment-form {
  margin-top: 20px;
}

textarea {
  width: 100%;
  margin-bottom: 10px;
}

button {
  background-color: #007bff;
  color: white;
  border: none;
  padding: 10px;
  cursor: pointer;
}

button:hover {
  background-color: #0056b3;
}
</style>

<template>
  <div>
    <h3>댓글</h3>

    <!-- 댓글 목록 -->
    <div v-if="comments.length > 0">
      <div v-for="comment in comments" :key="comment.id" class="comment">
        <p><strong>{{ comment.user }}</strong>: {{ comment.content }}</p>
        <p class="comment-meta">작성일: {{ comment.created_at }}</p>
        <hr />
      </div>
    </div>
    <div v-else>
      <p>댓글이 없습니다. 첫 번째 댓글을 작성해보세요!</p>
    </div>

    <!-- 댓글 작성 -->
    <div class="comment-form">
      <h4>댓글 작성</h4>
      <textarea v-model="newComment" placeholder="댓글을 입력하세요..." rows="4"></textarea>
      <button @click="submitComment">댓글 등록</button>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import axios from 'axios';
import { useRoute } from 'vue-router';
import { useCounterStore } from '@/stores/counter';

const store = useCounterStore();
const route = useRoute();

// 로컬 상태
const comments = ref([]);
const newComment = ref('');
const articleId = route.params.id;
const communityId = route.query.community_id || route.params.community_id;

// 댓글 가져오기
const fetchComments = async () => {
  try {
    const response = await axios.get(
      `${store.API_URL}/communities/${communityId}/articles/${articleId}/`,
      {
        headers: {
          Authorization: `Token ${store.token}`,
        },
      }
    );
    comments.value = response.data.comments; // 댓글 데이터 저장
  } catch (error) {
    console.error('댓글 가져오기 실패:', error);
  }
};

// 댓글 작성
const submitComment = async () => {
  if (!newComment.value.trim()) {
    alert('댓글 내용을 입력하세요.');
    return;
  }

  try {
    const response = await axios.post(
      `${store.API_URL}/communities/${communityId}/articles/${articleId}/`,
      { content: newComment.value },
      {
        headers: {
          Authorization: `Token ${store.token}`,
        },
      }
    );
    // 작성한 댓글을 목록에 추가
    comments.value.push(response.data);
    newComment.value = ''; // 입력창 초기화
  } catch (error) {
    console.error('댓글 작성 실패:', error);
  }
};

// 컴포넌트 로드 시 댓글 가져오기
onMounted(() => {
  fetchComments();
});
</script>

<style scoped>
.comment {
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

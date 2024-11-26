<template>
  <div>
    <h3>게시글 상세 보기</h3>
    <p>글번호: {{ article?.article?.id }}</p>
    <p>제목: {{ article?.article?.title }}</p>
    <p>조회수: {{ article?.article?.viewscount }}</p>
    <p>생성일: {{ article?.article?.created_at }}</p>
    <p>수정일: {{ article?.article?.updated_at }}</p>
    <p>작성자: {{ article?.article?.user }}</p>

    <!-- 댓글 목록 -->
    <div>
      <h4>댓글</h4>
      <div v-if="comments.length > 0">
        <div v-for="comment in comments" :key="comment.id" class="comment-item">
          <div v-if="editingCommentId !== comment.id">
            <p><strong>{{ comment.user }}</strong>: {{ comment.content }}</p>
            <p class="comment-meta">작성일: {{ comment.created_at }}</p>
            <button @click="startEditing(comment)">수정</button>
            <button @click="deleteComment(comment.id)">삭제</button>
          </div>
          <div v-else>
            <textarea v-model="editingContent" rows="3"></textarea>
            <button @click="updateComment(comment.id)">저장</button>
            <button @click="cancelEditing">취소</button>
          </div>
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
const article = ref(null);
const editingCommentId = ref(null); // 현재 수정 중인 댓글 ID
const editingContent = ref(''); // 수정 중인 댓글 내용




onMounted(async () => {
  try {
    
    const response = await axios.get(
      `${store.API_URL}/communities/4/articles/${route.params.id}/`,
      {
        headers: {
          Authorization: `Token ${store.token}`,
        },
      }
    );
    article.value = response.data;
  } catch (err) {
    console.error('게시글 상세 데이터 가져오기 실패:', err);
  }
});
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
      `${store.API_URL}/communities/4/articles/${route.params.id}/`,
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

// 댓글 수정 시작
const startEditing = (comment) => {
  editingCommentId.value = comment.id;
  editingContent.value = comment.content;
};

// 댓글 수정 취소
const cancelEditing = () => {
  editingCommentId.value = null;
  editingContent.value = '';
};

// 댓글 수정 저장
const updateComment = async (commentId) => {
  if (!editingContent.value.trim()) {
    alert('댓글 내용을 입력하세요.');
    return;
  }
  try {
    const response = await axios.post(
      `${store.API_URL}/communities/4/articles/${route.params.id}/`,
      { content: editingContent.value },
      {
        headers: {
          Authorization: `Token ${store.token}`,
          'Content-Type': 'application/json',
        },
      }
    );
    const updatedComment = response.data;
    const index = comments.value.findIndex((comment) => comment.id === commentId);
    if (index !== -1) {
      comments.value[index] = updatedComment; // 수정된 댓글 업데이트
    }
    cancelEditing();
  } catch (err) {
    console.error('댓글 수정 실패:', err);
  }
};

// 댓글 삭제
const deleteComment = async (commentId) => {
  if (!confirm('정말로 이 댓글을 삭제하시겠습니까?')) {
    return;
  }
  try {
    await axios.delete(
      `${store.API_URL}/communities/4/articles/${route.params.id}/comments/${commentId}/`,
      {
        headers: {
          Authorization: `Token ${store.token}`,
        },
      }
    );
    comments.value = comments.value.filter((comment) => comment.id !== commentId); // 댓글 목록에서 제거
    alert('댓글이 삭제되었습니다.');
  } catch (err) {
    console.error('댓글 삭제 실패:', err);
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

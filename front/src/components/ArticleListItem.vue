<template>
  <div class="article-detail-container">
    <h3 class="article-title">게시글 상세 보기</h3>
    <div class="article-info">
      <p><strong>글번호:</strong> {{ article?.article?.id }}</p>
      <p><strong>제목:</strong> {{ article?.article?.title }}</p>
      <p><strong>조회수:</strong> {{ article?.article?.viewscount }}</p>
      <p><strong>생성일:</strong> {{ article?.article?.created_at }}</p>
      <p><strong>수정일:</strong> {{ article?.article?.updated_at }}</p>
      <p><strong>작성자:</strong> {{ article?.article?.user }}</p>
    </div>

    <!-- 댓글 목록 -->
    <div class="comments-section">
      <h4>댓글</h4>
      <div v-if="comments.length > 0">
        <div v-for="comment in comments" :key="comment.id" class="comment-item">
          <div v-if="editingCommentId !== comment.id">
            <p><strong>{{ comment.user }}</strong>: {{ comment.content }}</p>
            <p class="comment-meta">작성일: {{ comment.created_at }}</p>
            <div class="comment-actions">
              <button @click="startEditing(comment)" class="btn btn-sm btn-primary">
                수정
              </button>
              <button @click="deleteComment(comment.id)" class="btn btn-sm btn-danger">
                삭제
              </button>
            </div>
          </div>
          <div v-else>
            <textarea v-model="editingContent" rows="3" class="form-control"></textarea>
            <div class="edit-actions">
              <button @click="updateComment(comment.id)" class="btn btn-sm btn-success">
                저장
              </button>
              <button @click="cancelEditing" class="btn btn-sm btn-secondary">
                취소
              </button>
            </div>
          </div>
        </div>
      </div>
      <div v-else>
        <p>댓글이 없습니다. 첫 번째 댓글을 작성해보세요!</p>
      </div>
    </div>

    <!-- 댓글 작성 -->
    <div class="comment-form">
      <h4>댓글 작성</h4>
      <textarea
        v-model="newComment"
        placeholder="댓글을 입력하세요..."
        rows="3"
        class="form-control"
      ></textarea>
      <button @click="submitComment" class="btn btn-primary mt-2">
        댓글 등록
      </button>
    </div>
  </div>
</template>

<script setup>
import { ref, watch, onMounted } from "vue";
import { useRoute } from "vue-router";
import axios from "axios";
import { useCounterStore } from "@/stores/counter";

const store = useCounterStore();
const route = useRoute();
const article = ref(null);
const editingCommentId = ref(null);
const editingContent = ref("");
const comments = ref([]);
const newComment = ref("");
const communityId = ref(route.query.community_id);

watch(
  () => route.query.community_id,
  (newVal) => {
    communityId.value = newVal;
  }
);

const fetchArticleAndComments = async () => {
  if (!communityId.value) {
    console.error("communityId가 없습니다.");
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
    console.error("게시글 및 댓글 데이터 가져오기 실패:", err);
  }
};

const submitComment = async () => {
  if (!newComment.value.trim()) {
    alert("댓글 내용을 입력하세요.");
    return;
  }
  try {
    const response = await axios.post(
      `${store.API_URL}/communities/${communityId.value}/articles/${route.params.id}/comments/`,
      { content: newComment.value },
      {
        headers: {
          Authorization: `Token ${store.token}`,
          "Content-Type": "application/json",
        },
      }
    );
    comments.value.push(response.data);
    newComment.value = "";
  } catch (err) {
    console.error("댓글 작성 실패:", err);
  }
};

const startEditing = (comment) => {
  editingCommentId.value = comment.id;
  editingContent.value = comment.content;
};

const cancelEditing = () => {
  editingCommentId.value = null;
  editingContent.value = "";
};

const updateComment = async (commentId) => {
  if (!editingContent.value.trim()) {
    alert("댓글 내용을 입력하세요.");
    return;
  }
  try {
    const response = await axios.put(
      `${store.API_URL}/communities/${communityId.value}/articles/${route.params.id}/comments/${commentId}/`,
      { content: editingContent.value },
      {
        headers: {
          Authorization: `Token ${store.token}`,
          "Content-Type": "application/json",
        },
      }
    );
    const updatedComment = response.data;
    const index = comments.value.findIndex((comment) => comment.id === commentId);
    if (index !== -1) {
      comments.value[index] = updatedComment;
    }
    cancelEditing();
  } catch (err) {
    console.error("댓글 수정 실패:", err);
  }
};

const deleteComment = async (commentId) => {
  if (!confirm("정말로 이 댓글을 삭제하시겠습니까?")) {
    return;
  }
  try {
    await axios.delete(
      `${store.API_URL}/communities/${communityId.value}/articles/${route.params.id}/comments/${commentId}/`,
      {
        headers: {
          Authorization: `Token ${store.token}`,
        },
      }
    );
    comments.value = comments.value.filter((comment) => comment.id !== commentId);
    alert("댓글이 삭제되었습니다.");
  } catch (err) {
    console.error("댓글 삭제 실패:", err);
  }
};

onMounted(fetchArticleAndComments);
</script>

<style>
.article-detail-container {
  max-width: 800px;
  margin: 40px auto;
  padding: 20px;
  background-color: #f8f9fa;
  border-radius: 12px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
}

.article-title {
  font-size: 24px;
  font-weight: bold;
  color: #005bac;
  margin-bottom: 20px;
}

.article-info p {
  font-size: 16px;
  color: #333;
  margin: 5px 0;
}

.comments-section {
  margin-top: 20px;
}

.comment-item {
  background-color: #ffffff;
  border-radius: 8px;
  padding: 15px;
  margin-bottom: 10px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.comment-meta {
  font-size: 12px;
  color: gray;
}

.comment-actions {
  margin-top: 10px;
  display: flex;
  gap: 10px;
}

.comment-form {
  margin-top: 20px;
}

textarea {
  width: 100%;
  margin-bottom: 10px;
  border-radius: 8px;
  border: 1px solid #ced4da;
}

button {
  padding: 8px 12px;
  border-radius: 8px;
  font-size: 14px;
  font-weight: bold;
}

.btn-danger {
  background-color: #e63946;
}

.btn-danger:hover {
  background-color: #c92a2a;
}
</style>

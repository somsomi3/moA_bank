<template>
  <div class="article-detail-container">
    <h3 class="article-title">게시글 상세 보기</h3>
    <div class="article-info">
      <p><strong>글번호:</strong> {{ article?.id }}</p>
      <p><strong>제목:</strong> {{ article?.title }}</p>
      <p><strong>조회수:</strong> {{ article?.viewscount }}</p>
      <p><strong>생성일:</strong> {{ article?.created_at }}</p>
      <p><strong>수정일:</strong> {{ article?.updated_at }}</p>
      <p><strong>작성자:</strong> {{ article?.user }}</p>
    </div>

    <!-- 댓글 목록 -->
    <div class="comments-section">
      <h4 class="comments-title">댓글</h4>
      <div v-if="comments.length > 0" class="comments-list">
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
      <h4 class="comment-form-title">댓글 작성</h4>
      <textarea
        v-model="newComment"
        placeholder="댓글을 입력하세요..."
        rows="3"
        class="comment-input"
      ></textarea>
      <button @click="submitComment" class="btn btn-primary">댓글 등록</button>
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

// 게시글, 댓글 데이터 및 새 댓글 작성 상태
const article = ref(null);
const comments = ref([]);
const newComment = ref("");
const communityId = ref(route.query.community_id);

// watch로 communityId 반응형 관리
watch(() => route.query.community_id, (newVal) => {
  communityId.value = newVal;
});

// 게시글 및 댓글 가져오기
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

// 댓글 작성
const submitComment = async () => {
  if (!newComment.value.trim()) {
    alert("댓글 내용을 입력하세요.");
    return;
  }
  try {
    const response = await axios.post(
      `${store.API_URL}/communities/${communityId.value}/articles/${route.params.id}/`,
      { content: newComment.value },
      {
        headers: {
          Authorization: `Token ${store.token}`,
          "Content-Type": "application/json",
        },
      }
    );
    // 작성한 댓글을 목록에 추가
    comments.value.push(response.data);
    newComment.value = ""; // 입력창 초기화
  } catch (err) {
    console.error("댓글 작성 실패:", err);
  }
};

// 컴포넌트가 마운트되면 게시글 및 댓글 가져오기
onMounted(fetchArticleAndComments);
</script>

<style scoped>
.article-detail-container {
  max-width: 800px;
  margin: 0 auto;
  padding: 20px;
  font-family: "Noto Sans KR", Arial, sans-serif;
  background-color: #f9f9f9;
  border-radius: 8px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
}

.article-title {
  font-size: 24px;
  font-weight: bold;
  color: #0056b3;
  margin-bottom: 20px;
  text-align: center;
}

.article-info p {
  font-size: 16px;
  color: #333;
  margin: 5px 0;
}

.comments-section {
  margin-top: 30px;
}

.comments-title {
  font-size: 20px;
  font-weight: bold;
  color: #333;
  margin-bottom: 15px;
}

.comments-list {
  border-top: 1px solid #ddd;
  padding-top: 15px;
}

.comment-item {
  margin-bottom: 15px;
  padding: 10px;
  background-color: #ffffff;
  border-radius: 5px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.comment-meta {
  font-size: 14px;
  color: gray;
  margin-top: 5px;
}

.comment-form {
  margin-top: 30px;
}

.comment-form-title {
  font-size: 18px;
  font-weight: bold;
  margin-bottom: 10px;
}

.comment-input {
  width: 100%;
  padding: 10px;
  border: 1px solid #ced4da;
  border-radius: 5px;
  margin-bottom: 10px;
  resize: none;
}

.comment-input:focus {
  border-color: #007bff;
  outline: none;
}

button {
  display: inline-block;
  background-color: #007bff;
  color: white;
  border: none;
  padding: 10px 20px;
  border-radius: 5px;
  cursor: pointer;
  font-size: 16px;
  transition: background-color 0.3s ease;
}

button:hover {
  background-color: #0056b3;
}
</style>

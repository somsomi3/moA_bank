<template>
  <div class="container">
    <!-- 왼쪽 카테고리 -->
    <aside class="sidebar">
      <h2>카테고리</h2>
      <ul>
        <li><button>예금 리스트 보기</button></li>
        <li><button>적금 리스트 보기</button></li>
        <li><button>카드 리스트 보기</button></li>
      </ul>
    </aside>

    <!-- 오른쪽 콘텐츠 -->
    <main class="content">
      <h1>카드 생성하기</h1>
      <form @submit.prevent="generateCard" class="card-form">
        <div>
          <label for="prompt">배경 프롬프트:</label>
          <input v-model="prompt" id="prompt" placeholder="배경 프롬프트를 입력하세요" />
        </div>
        <div>
          <label for="text">카드 이름:</label>
          <input v-model="card_name" id="card_name" placeholder="카드 이름을 입력하세요" />
        </div>
        <div>
          <label for="font">폰트 업로드:</label>
          <input type="file" @change="handleFontUpload" accept=".ttf" />
        </div>
        <button type="submit">카드 생성</button>
      </form>

      <!-- 생성된 카드 이미지 표시 -->
      <div v-if="generatedCard" class="generated-card">
        <h2>생성된 카드:</h2>
        <img :src="generatedCard" alt="Generated Card" />
      </div>
    </main>
  </div>
</template>

<script setup>
import { ref, onMounted } from "vue";
import { useCounterStore } from "@/stores/counter";
import axios from "axios";

const store = useCounterStore();
const token = store.token;
const tempuserId = ref(0);

async function getuserId() {
  const userInfoResponse = await fetch(`${store.API_URL}/dj-rest-auth/user/`, {
    method: "GET",
    headers: {
      "Authorization": `Token ${token}`,
    },
  });
  if (userInfoResponse.ok) {
    const userInfo = await userInfoResponse.json();
    tempuserId.value = userInfo.pk;
  } else {
    console.error("Failed to fetch user ID");
  }
}

async function generateCard() {
  if (!prompt.value || !card_name.value || !fontFile.value) {
    alert("Prompt, 카드 이름, 폰트 파일을 모두 입력해주세요.");
    return;
  }

  try {
    const formData = new FormData();
    formData.append("prompt", prompt.value);
    formData.append("card_name", card_name.value);
    formData.append("font", fontFile.value);
    formData.append("user_id", tempuserId.value);

    const response = await axios.post(
      `${store.API_URL}/api/v1/card-designs/generate_card/`,
      formData,
      {
        headers: {
          "Authorization": `Token ${token}`,
        },
        responseType: "blob",
      }
    );

    generatedCard.value = URL.createObjectURL(response.data);
  } catch (error) {
    console.error("Error generating card:", error);
    alert("카드 생성 실패. 입력값을 확인하고 다시 시도하세요.");
  }
}

onMounted(() => {
  getuserId();
});

const prompt = ref("");
const card_name = ref("");
const fontFile = ref(null);
const generatedCard = ref(null);

function handleFontUpload(event) {
  fontFile.value = event.target.files[0];
}
</script>

<style>
/* 전체 컨테이너 */
.container {
  display: flex;
  height: 100vh;
}

/* 사이드바 */
.sidebar {
  width: 20%;
  background-color: #f8f9fa;
  padding: 20px;
  box-shadow: 1px 0 5px rgba(0, 0, 0, 0.1);
}

.sidebar h2 {
  font-size: 18px;
  margin-bottom: 15px;
}

.sidebar ul {
  list-style: none;
  padding: 0;
}

.sidebar li {
  margin-bottom: 10px;
}

.sidebar button {
  width: 100%;
  padding: 10px;
  border: none;
  background-color: #e9ecef;
  border-radius: 5px;
  text-align: left;
  cursor: pointer;
}

.sidebar button:hover {
  background-color: #dee2e6;
}

/* 메인 콘텐츠 */
.content {
  flex: 1;
  padding: 20px;
}

.content h1 {
  text-align: center;
  margin-bottom: 20px;
}

.card-form {
  display: flex;
  flex-direction: column;
  gap: 15px;
  max-width: 600px;
  margin: 0 auto;
}

.card-form label {
  font-weight: bold;
}

.card-form input {
  padding: 8px;
  border: 1px solid #ccc;
  border-radius: 5px;
  width: 100%;
}

.card-form button {
  padding: 10px 20px;
  background-color: #007bff;
  color: white;
  border: none;
  border-radius: 5px;
  cursor: pointer;
}

.card-form button:hover {
  background-color: #0056b3;
}

.generated-card {
  margin-top: 20px;
  text-align: center;
}

.generated-card img {
  margin-top: 20px;
  max-width: 20%; /* 현재 크기의 2/3로 설정 */
  height: auto;
  border: 2px solid #ccc;
  border-radius: 10px;
  transform: scale(0.66); /* 비율 유지하면서 2/3 크기로 축소 */
  transform-origin: center; /* 축소 중심을 중앙으로 */
}
</style>

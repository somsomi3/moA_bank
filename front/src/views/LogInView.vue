<template>
  <div class="login-container">
    <!-- 오른쪽 위 눈사람 이모티콘 -->
    <div class="snowman-icon" @click="promptInfo">☃</div>

    <!-- 로그인 폼 -->
    <div class="login-box">
      <h1>LogIn Page</h1>
      <form @submit.prevent="logIn" class="login-form">
        <label for="username">Username:</label>
        <input type="text" id="username" v-model.trim="username" class="input-field"><br>

        <label for="password">Password:</label>
        <input type="password" id="password" v-model.trim="password" class="input-field"><br>

        <input type="submit" value="Log In" class="submit-button">
      </form>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue';
import { useCounterStore } from '@/stores/counter';

// 사용자 입력 상태
const username = ref(null);
const password = ref(null);

const store = useCounterStore();

// 로그인 함수
const logIn = function () {
  const payload = {
    username: username.value,
    password: password.value,
  };
  store.logIn(payload);
};

// 눈사람 클릭 이벤트
const promptInfo = () => {
  alert("로그인 후 더 많은 기능을 이용해보세요!");
};
</script>

<style scoped>
/* 전체 컨테이너 */
.login-container {
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  height: 100vh; /* 화면 높이 채우기 */
  background-color: #f5f5f5; /* 연한 회색 배경 */
  position: relative;
}

/* 눈사람 아이콘 */
.snowman-icon {
  position: absolute;
  top: 20px;
  right: 20px;
  font-size: 30px; /* 눈사람 크기 */
  cursor: pointer;
  color: #6c757d; /* 중간 회색 */
}

.snowman-icon:hover {
  color: #007bff; /* 호버 시 파란색 */
}

/* 로그인 박스 */
.login-box {
  width: 400px;
  padding: 30px;
  background-color: white; /* 흰색 배경 */
  border-radius: 8px;
  box-shadow: 0px 4px 8px rgba(0, 0, 0, 0.1); /* 그림자 */
  text-align: center;
}

/* 폼 스타일 */
.login-form {
  display: flex;
  flex-direction: column;
  gap: 15px; /* 입력 필드 간격 */
}

.label {
  font-size: 14px;
  color: #333;
}

.input-field {
  width: 100%;
  padding: 10px;
  font-size: 16px;
  border: 1px solid #ccc;
  border-radius: 5px;
  box-sizing: border-box;
}

.input-field:focus {
  border-color: #007bff;
  outline: none;
}

/* 버튼 스타일 */
.submit-button {
  padding: 10px;
  font-size: 16px;
  font-weight: bold;
  color: white;
  background-color: #007bff;
  border: none;
  border-radius: 5px;
  cursor: pointer;
  transition: background-color 0.3s ease;
}

.submit-button:hover {
  background-color: #0056b3;
}
</style>

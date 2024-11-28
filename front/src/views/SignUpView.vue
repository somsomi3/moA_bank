<template>
  <div class="signup-container">
    <h1 class="signup-title">Sign Up</h1>
    <form @submit.prevent="signUp" class="signup-form">
      <div class="form-group">
        <label for="nickname" class="form-label">이름</label>
        <input
          type="text"
          id="nickname"
          v-model.trim="nickname"
          class="form-input"
          placeholder="이름을 입력하세요"
        />
      </div>

      <div class="form-group">
        <label for="username" class="form-label">아이디</label>
        <input
          type="text"
          id="username"
          v-model.trim="username"
          class="form-input"
          placeholder="아이디를 입력하세요"
        />
      </div>

      <div class="form-group">
        <label for="password1" class="form-label">비밀번호</label>
        <input
          type="password"
          id="password1"
          v-model.trim="password1"
          class="form-input"
          placeholder="비밀번호를 입력하세요"
        />
      </div>

      <div class="form-group">
        <label for="password2" class="form-label">비밀번호 확인</label>
        <input
          type="password"
          id="password2"
          v-model.trim="password2"
          class="form-input"
          placeholder="비밀번호를 다시 입력하세요"
        />
      </div>

      <div class="form-group">
        <label for="age" class="form-label">나이</label>
        <input
          type="number"
          id="age"
          v-model.trim="age"
          class="form-input"
          placeholder="나이를 입력하세요"
        />
      </div>

      <div class="form-group">
        <label for="income" class="form-label">월소득</label>
        <input
          type="number"
          id="income"
          v-model.trim="income"
          class="form-input"
          placeholder="월소득을 입력하세요"
        />
      </div>

      <div class="form-group">
        <label for="job" class="form-label">직업</label>
        <input
          type="text"
          id="job"
          v-model.trim="job"
          class="form-input"
          placeholder="직업을 입력하세요"
        />
      </div>

      <div class="form-group">
        <label for="gender" class="form-label">성별</label>
        <input
          type="text"
          id="gender"
          v-model.trim="gender"
          class="form-input"
          placeholder="성별을 입력하세요"
        />
      </div>

      <div class="form-group">
        <label for="grade" class="form-label">최종학력</label>
        <input
          type="text"
          id="grade"
          v-model.trim="grade"
          class="form-input"
          placeholder="최종학력을 입력하세요"
        />
      </div>

      <div class="form-group">
        <label for="main_bank" class="form-label">주거래은행</label>
        <input
          type="text"
          id="main_bank"
          v-model.trim="main_bank"
          class="form-input"
          placeholder="주거래은행을 입력하세요"
        />
      </div>

      <div class="form-group">
        <label for="region" class="form-label">지역</label>
        <input
          type="text"
          id="region"
          v-model.trim="region"
          class="form-input"
          placeholder="지역을 입력하세요"
        />
      </div>

      <div class="form-group">
        <label for="consume" class="form-label">월소비</label>
        <input
          type="number"
          id="consume"
          v-model.trim="consume"
          class="form-input"
          placeholder="월소비를 입력하세요"
        />
      </div>

      <div class="form-group">
        <label for="desire_period" class="form-label">희망 예적금 기간</label>
        <input
          type="number"
          id="desire_period"
          v-model.trim="desire_period"
          class="form-input"
          placeholder="희망 예적금 기간을 입력하세요"
        />
      </div>

      <div class="form-group">
        <label for="financial_product" class="form-label">예적금을 넣고 계시나요?</label>
        <input
          type="text"
          id="financial_product"
          v-model.trim="financial_product"
          class="form-input"
          placeholder="예적금 여부를 입력하세요"
        />
      </div>

      <button type="submit" class="btn btn-primary signup-button">Sign Up</button>
    </form>
  </div>
</template>

<script setup>
import { ref } from "vue";
import { useCounterStore } from "@/stores/counter";

const username = ref(null);
const password1 = ref(null);
const password2 = ref(null);
const age = ref(0);
const income = ref(0);
const job = ref(null);
const gender = ref(null);
const grade = ref(null);
const main_bank = ref(null);
const region = ref(null);
const consume = ref(0);
const desire_period = ref(0);
const financial_product = ref(null);
const nickname = ref(null);

const store = useCounterStore();

const signUp = function () {
  const payload = {
    username: username.value,
    password1: password1.value,
    password2: password2.value,
    age: age.value,
    income: income.value,
    job: job.value,
    gender: gender.value,
    grade: grade.value,
    main_bank: main_bank.value,
    region: region.value,
    consume: consume.value,
    desire_period: desire_period.value,
    financial_product: financial_product.value,
    name: nickname.value,
  };
  store.signUp(payload);
};
</script>

<style scoped>
.signup-container {
  max-width: 600px;
  margin: 30px auto;
  padding: 20px;
  background-color: #f8f9fa;
  border-radius: 10px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  font-family: "Noto Sans KR", Arial, sans-serif;
}

.signup-title {
  text-align: center;
  font-size: 24px;
  font-weight: bold;
  color: #0056b3;
  margin-bottom: 20px;
}

.signup-form {
  display: flex;
  flex-direction: column;
  gap: 15px;
}

.form-group {
  display: flex;
  flex-direction: column;
}

.form-label {
  font-size: 14px;
  color: #333;
  margin-bottom: 5px;
}

.form-input {
  padding: 10px;
  font-size: 14px;
  border: 1px solid #ced4da;
  border-radius: 5px;
}

.form-input:focus {
  border-color: #007bff;
  outline: none;
  box-shadow: 0 0 4px rgba(0, 123, 255, 0.5);
}

.signup-button {
  padding: 10px;
  font-size: 16px;
  font-weight: bold;
  color: white;
  background-color: #007bff;
  border: none;
  border-radius: 5px;
  cursor: pointer;
}

.signup-button:hover {
  background-color: #0056b3;
}
</style>

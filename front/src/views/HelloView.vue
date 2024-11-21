<template>
    <div class="container">
      <!-- 대화형 메시지 -->
      <p class="message">{{ displayedText }}</p>
  
      <!-- 이름 입력 -->
      <div v-if="showNameInput">
        <input v-model="userData.name" type="text" placeholder="이름을 입력하세요" class="input" />
        <button @click="saveName" class="next-button">확인</button>
      </div>
  
      <!-- 성별 선택 -->
      <div v-if="showGenderSelection">
        <button @click="setGender('남성')" class="next-button">남성</button>
        <button @click="setGender('여성')" class="next-button">여성</button>
      </div>
  
      <!-- 예적금 여부 선택 -->
      <div v-if="showSavingsSelection">
        <button @click="setSavings('예')" class="next-button">예</button>
        <button @click="setSavings('아니오')" class="next-button">아니오</button>
      </div>
  
      <!-- 숫자 입력 -->
      <div v-if="showNumericInput">
        <input v-model.number="numericInput" type="number" :placeholder="currentPlaceholder" class="input" />
        <button @click="saveNumericInput" class="next-button">확인</button>
      </div>
  
      <!-- 직업 선택 -->
      <div v-if="showJobSelection">
        <select v-model="userData.job" class="input">
          <option disabled value="">직업을 선택하세요</option>
          <option value="학생">학생</option>
          <option value="회사원">회사원</option>
          <option value="자영업자">자영업자</option>
          <option value="프리랜서">프리랜서</option>
          <option value="기타">기타</option>
        </select>
        <button @click="saveJob" class="next-button">확인</button>
      </div>
  
      <!-- 다음으로 버튼 -->
      <button
        v-if="!showInputFields && isTypingComplete && !submitted"
        @click="nextMessage"
        class="next-button"
      >
        다음으로
      </button>
  
      <!-- 결과 출력 -->
      <div v-if="submitted">
        <h3>입력된 정보</h3>
        <p>이름: {{ userData.name }}</p>
        <p>성별: {{ userData.gender }}</p>
        <p>예적금 여부: {{ userData.hasSavings }}</p>
        <p>나이: {{ userData.age }}</p>
        <p>월소득: {{ userData.income }}</p>
        <p>월소비: {{ userData.spending }}</p>
        <p>직업: {{ userData.job }}</p>
      </div>
    </div>
  </template>
  
  <script setup>
  import { ref } from 'vue';
  
  // 메시지 리스트
  const messages = [
    "안녕하세요! 저는 당신의 경제 생활 매니저 모아에요!",
    "저는 당신의 경제 생활에 대한 간단한 정보를 바탕으로, 유용한 정보를 제공해 드릴거에요!",
    "지금부터 시작해볼까요?",
    "좋아요! 당신의 이름은 무엇인가요?",
    "좋아요! 성별은요?",
    "예적금을 넣고 계신가요",
    "나이를 알려주시면 좋을 것 같아요!",
    "월소득은 얼마쯤 되세요??",
    "월소비는 얼마쯤 되세요??",
    "직업을 선택해주세요!",
    "감사합니다! {{userData.value.name}}님이 입력해주신 자료를 바탕으로 리포트를 만들고 있어요! 잠시만 기다려주세요 :)",
  ];
  
  // 사용자 데이터 상태
  const userData = ref({
    name: "",
    gender: "",
    hasSavings: "",
    age: null,
    income: null,
    spending: null,
    job: "",
  });
  
  // 현재 메시지 및 상태 관리
  const currentIndex = ref(0);
  const displayedText = ref(""); // 현재 한 글자씩 출력 중인 텍스트
  const isTypingComplete = ref(false); // 현재 메시지 출력 완료 여부
  const submitted = ref(false);
  
  // 입력 필드 표시 관리
  const showNameInput = ref(false);
  const showGenderSelection = ref(false);
  const showSavingsSelection = ref(false);
  const showNumericInput = ref(false);
  const showJobSelection = ref(false);
  const showInputFields = ref(false); // 현재 입력 필드 표시 여부
  
  // 숫자 입력 상태
  const numericInput = ref(null);
  const currentPlaceholder = ref("숫자를 입력하세요");
  
  // 한 글자씩 출력하기
  function typeMessage(message) {
    displayedText.value = "";
    isTypingComplete.value = false;
    resetInputFields();
  
    let index = 0;
    const typingInterval = setInterval(() => {
      displayedText.value += message[index];
      index++;
      if (index === message.length) {
        clearInterval(typingInterval);
        isTypingComplete.value = true;
        handleInputFields();
      }
    }, 50); // 글자 출력 간격
  }
  
  // 입력 필드 초기화
  function resetInputFields() {
    showNameInput.value = false;
    showGenderSelection.value = false;
    showSavingsSelection.value = false;
    showNumericInput.value = false;
    showJobSelection.value = false;
  }
  
  // 입력 필드 표시 관리
  function handleInputFields() {
    const currentMessage = messages[currentIndex.value];
    if (currentMessage.includes("이름은")) showNameInput.value = true;
    if (currentMessage.includes("성별은")) showGenderSelection.value = true;
    if (currentMessage.includes("예적금을")) showSavingsSelection.value = true;
    if (currentMessage.includes("나이를")) {
      showNumericInput.value = true;
      currentPlaceholder.value = "나이를 입력하세요";
    }
    if (currentMessage.includes("월소득은")) {
      showNumericInput.value = true;
      currentPlaceholder.value = "월소득을 입력하세요";
    }
    if (currentMessage.includes("월소비는")) {
      showNumericInput.value = true;
      currentPlaceholder.value = "월소비를 입력하세요";
    }
    if (currentMessage.includes("직업을")) showJobSelection.value = true;
  
    // 입력 필드가 표시되면 "다음으로" 버튼 숨기기
    showInputFields.value =
      showNameInput.value ||
      showGenderSelection.value ||
      showSavingsSelection.value ||
      showNumericInput.value ||
      showJobSelection.value;
  }
  
  // 메시지 전환
  function nextMessage() {
    if (currentIndex.value < messages.length - 1) {
      currentIndex.value++;
      isTypingComplete.value = false;
      const nextMsg = messages[currentIndex.value];
      typeMessage(nextMsg);
  
      if (currentIndex.value === messages.length - 1) {
        submitted.value = true;
      }
    }
  }
  
  // 데이터 저장 및 처리
  function saveName() {
    if (userData.value.name.trim()) {
      nextMessage();
    }
  }
  
  function setGender(gender) {
    userData.value.gender = gender;
    nextMessage();
  }
  
  function setSavings(hasSavings) {
    userData.value.hasSavings = hasSavings;
    nextMessage();
  }
  
  function saveNumericInput() {
    if (currentPlaceholder.value.includes("나이")) {
      userData.value.age = numericInput.value;
    } else if (currentPlaceholder.value.includes("월소득")) {
      userData.value.income = numericInput.value;
    } else if (currentPlaceholder.value.includes("월소비")) {
      userData.value.spending = numericInput.value;
    }
    numericInput.value = null;
    nextMessage();
  }
  
  function saveJob() {
    if (userData.value.job) {
      nextMessage();
    }
  }
  
  // 초기 메시지 출력
  typeMessage(messages[currentIndex.value]);
  </script>
  
  <style scoped>
  .container {
    max-width: 600px;
    margin: 0 auto;
    text-align: center;
    font-family: Arial, sans-serif;
  }
  
  .message {
    font-size: 18px;
    margin-bottom: 20px;
    line-height: 1.6;
    min-height: 50px; /* 메시지 출력 영역 고정 */
  }
  
  .input {
    width: 80%;
    padding: 10px;
    margin: 10px 0;
    font-size: 16px;
    border: 1px solid #ccc;
    border-radius: 4px;
    box-sizing: border-box;
  }
  
  .next-button {
    padding: 10px 20px;
    font-size: 16px;
    cursor: pointer;
    border: none;
    border-radius: 5px;
    background-color: #007bff;
    color: white;
    margin: 5px;
  }
  
  .next-button:hover {
    background-color: #0056b3;
  }
  </style>
  
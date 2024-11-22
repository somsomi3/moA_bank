<template>
  <div class="container">
    <!-- 대화형 메시지 -->
    <p class="message">{{ displayedText }}</p>

    <!-- 닉네임, 아이디, 비밀번호 입력 -->
    <div v-if="showNicknameInput">
      <input v-model="userData.nickname" type="text" placeholder="닉네임을 입력하세요" class="input" />
      <input v-model="userData.username" type="text" placeholder="아이디를 입력하세요" class="input" />
      <input v-model="userData.password1" type="password" placeholder="비밀번호를 입력하세요" class="input" />
      <input v-model="userData.password2" type="password" placeholder="비밀번호를 다시 입력하세요" class="input" />
    </div>

    <!-- 성별 선택 -->
    <div v-if="showGenderSelection">
      <button @click="userData.gender = '남성'" class="next-button">남성</button>
      <button @click="userData.gender = '여성'" class="next-button">여성</button>
    </div>

    <!-- 나이, 지역, 주거래 은행 입력 -->
    <div v-if="showMultiInputs">
      <input v-model.number="userData.age" type="number" placeholder="나이를 입력하세요" class="input" />
      <input v-model="userData.region" type="text" placeholder="지역 이름을 입력하세요(시)" class="input" />
      <input v-model="userData.main_bank" type="text" placeholder="은행 이름을 입력하세요" class="input" />
    </div>

    <!-- 월소득, 월소비 입력 -->
    <div v-if="showNumericInputs">
      <input v-model.number="userData.income" type="number" placeholder="월소득을 입력하세요(만원)" class="input" />
      <input v-model.number="userData.consume" type="number" placeholder="월소비를 입력하세요(만원)" class="input" />
    </div>

    <!-- 학력, 직업 선택 -->
    <div v-if="showDropdownInputs">
      <select v-model="userData.grade" class="input">
        <option disabled value="">최종학력을 선택하세요</option>
        <option value="고졸이하">고졸이하</option>
        <option value="전문대졸">전문대졸</option>
        <option value="대졸이상">대졸이상</option>
      </select>
      <select v-model="userData.job" class="input">
        <option disabled value="">직업을 선택하세요</option>
        <option value="학생">학생</option>
        <option value="회사원">회사원</option>
        <option value="자영업자">자영업자</option>
        <option value="프리랜서">프리랜서</option>
        <option value="기타">기타</option>
      </select>
    </div>

    <!-- 예적금 기간 입력 -->
    <div v-if="showNumericInput">
      <input v-model.number="numericInput" type="number" :placeholder="currentPlaceholder" class="input" />
    </div>

    <!-- 확인 버튼 -->
    <button v-if="isTypingComplete && !submitted" @click="saveAllResponses" class="next-button">
      확인
    </button>

    <!-- 결과 출력 -->
    <div v-if="submitted">
      <h3>입력된 정보</h3>
      <p>닉네임: {{ userData.nickname }}</p>
      <p>아이디: {{ userData.username }}</p>
      <p>성별: {{ userData.gender }}</p>
      <p>지역: {{ userData.region }}</p>
      <p>주거래은행: {{ userData.main_bank }}</p>
      <p>예적금 기간: {{ userData.desire_period }}</p>
      <p>나이: {{ userData.age }}</p>
      <p>월소득: {{ userData.income }}</p>
      <p>월소비: {{ userData.consume }}</p>
      <p>최종 학력: {{ userData.grade }}</p>
      <p>직업: {{ userData.job }}</p>
    </div>
  </div>
</template>

<script setup>
import { ref } from "vue";

// 메시지 리스트
const messages = [
  "안녕하세요! 저는 당신의 경제 생활 매니저 모아에요!",
  "닉네임, 아이디, 비밀번호를 입력해주세요.",
  "성별을 선택해주세요.",
  "나이, 지역, 주거래 은행을 입력해주세요.",
  "월소득과 월소비를 입력해주세요.",
  "최종 학력과 직업을 선택해주세요.",
  "희망 예적금 기간을 입력해주세요.",
  "감사합니다! {{userData.nickname}}님이 입력해주신 자료를 바탕으로 리포트를 만들고 있어요!",
];

// 사용자 데이터 상태
const userData = ref({
  username: "",
  nickname: "",
  password1: "",
  password2: "",
  gender: "",
  job: "",
  grade: "",
  main_bank: "",
  region: "",
  age: null,
  income: null,
  consume: null,
  desire_period: null,
});

// 상태 관리
const currentIndex = ref(0);
const displayedText = ref("");
const isTypingComplete = ref(false);
const submitted = ref(false);

// 입력 필드 표시 관리
const showNicknameInput = ref(false);
const showNameInput = ref(false);
const showPasswordInput = ref(false);
const showGenderSelection = ref(false);
const showMultiInputs = ref(false); // 나이, 지역, 은행
const showNumericInputs = ref(false); // 월소득, 월소비
const showDropdownInputs = ref(false); // 학력, 직업
const showNumericInput = ref(false); // 예적금 기간


// 숫자 입력 상태
const numericInput = ref(null);
const currentPlaceholder = ref("숫자를 입력하세요");


// 메시지 출력
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
  }, 40);
}

// 입력 필드 초기화
function resetInputFields() {
  showNicknameInput.value = false;
  showNameInput.value = false;
  showPasswordInput.value = false;
  showGenderSelection.value = false;
  showMultiInputs.value = false;
  showNumericInputs.value = false;
  showDropdownInputs.value = false;
  showNumericInput.value = false;
}

// 입력 필드 표시 관리
function handleInputFields() {
  const currentMessage = messages[currentIndex.value];
  if (currentMessage.includes("닉네임")) {
    showNicknameInput.value = true;
    showNameInput.value = true;
    showPasswordInput.value = true;
  }
  if (currentMessage.includes("성별")) showGenderSelection.value = true;
  if (currentMessage.includes("나이")) showMultiInputs.value = true;
  if (currentMessage.includes("월소득")) showNumericInputs.value = true;
  if (currentMessage.includes("학력")) showDropdownInputs.value = true;
  if (currentMessage.includes("예적금")) {
    showNumericInput.value = true;
    currentPlaceholder.value = "기간을 입력하세요(달)";
  }
}

// 모든 답변이 입력되었는지 확인
function validateInputs() {
  if (showNicknameInput.value) {
    if (!userData.value.nickname.trim() || !userData.value.username.trim()) {
      alert("닉네임과 아이디를 모두 입력해주세요.");
      return false;
    }
    if (userData.value.password1 !== userData.value.password2 || !userData.value.password1.trim()) {
      alert("비밀번호가 일치하지 않거나 입력되지 않았습니다.");
      return false;
    }
  }
  if (showGenderSelection.value && !userData.value.gender) {
    alert("성별을 선택해주세요.");
    return false;
  }
  if (showMultiInputs.value) {
    if (!userData.value.age || !userData.value.region.trim() || !userData.value.main_bank.trim()) {
      alert("나이, 지역, 주거래 은행을 모두 입력해주세요.");
      return false;
    }
  }
  if (showNumericInputs.value) {
    if (!userData.value.income || !userData.value.consume) {
      alert("월소득과 월소비를 모두 입력해주세요.");
      return false;
    }
  }
  if (showDropdownInputs.value) {
    if (!userData.value.grade || !userData.value.job) {
      alert("최종 학력과 직업을 모두 선택해주세요.");
      return false;
    }
  }
  if (showNumericInput.value && !numericInput.value) {
    alert("희망 예적금 기간을 입력해주세요.");
    return false;
  }
  return true;
}

// 모든 답변 저장 및 진행
function saveAllResponses() {
  if (!validateInputs()) return;

  // 저장 후 다음으로 진행
  if (showNumericInput.value) {
    userData.value.desire_period = numericInput.value;
    numericInput.value = null;
  }
  resetInputFields();
  nextMessage();
}

// 메시지 전환
function nextMessage() {
  if (currentIndex.value < messages.length - 1) {
    currentIndex.value++;
    const nextMsg = messages[currentIndex.value];
    typeMessage(nextMsg);

    if (currentIndex.value === messages.length - 1) {
      submitted.value = true;
    }
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
  


  <template>
    <div class="container">
      <!-- 대화형 메시지 -->
      <p class="message">{{ displayedText }}</p>
  
      <!-- 닉네임 입력 -->
      <div v-if="showNicknameInput">
        <input v-model="userData.nickname" type="text" placeholder="닉네임을 입력하세요" class="input" />
        <button @click="saveNickname" class="next-button">확인</button>
      </div>
  
      <!-- 아이디 입력 -->
      <div v-if="showNameInput">
        <input v-model="userData.username" type="text" placeholder="아이디를 입력하세요" class="input" />
        <button @click="saveName" class="next-button">확인</button>
      </div>
  
      <!-- 비밀번호 입력 -->
      <div v-if="showPasswordInput">
        <input v-model="userData.password1" type="password" placeholder="비밀번호를 입력하세요" class="input" />
        <input v-model="userData.password2" type="password" placeholder="비밀번호를 다시 입력하세요" class="input" />
        <button @click="savePasswords" class="next-button">확인</button>
      </div>
  
      <!-- 성별 선택 -->
      <div v-if="showGenderSelection">
        <button @click="setGender('남성')" class="next-button">남성</button>
        <button @click="setGender('여성')" class="next-button">여성</button>
      </div>
  
      <!-- 예적금 여부 선택 -->
      <div v-if="showFinancialProductsSelection">
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
  
      <!-- 지역 입력 -->
      <div v-if="showRegionInput">
        <input v-model="userData.region" type="text" placeholder="지역 이름을 입력하세요(시)" class="input" />
        <button @click="saveRegion" class="next-button">확인</button>
      </div>
  
      <!-- 주거래은행 입력 -->
      <div v-if="showMainBank">
        <input v-model="userData.main_bank" type="text" placeholder="은행 이름을 입력하세요" class="input" />
        <button @click="saveMainBank" class="next-button">확인</button>
      </div>
  
      <!-- 학력 선택 -->
      <div v-if="showGradeSelection">
        <select v-model="userData.grade" class="input">
          <option disabled value="">최종학력을 선택하세요</option>
          <option value="고졸이하">고졸이하</option>
          <option value="전문대졸">전문대졸</option>
          <option value="대졸이상">대졸이상</option>
        </select>
  
    
        <button @click="saveGrade" class="next-button">확인</button>
      </div>
  
      <!-- "다음으로" 버튼 -->
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
        <p>닉네임: {{ userData.nickname }}</p>
        <p>아이디: {{ userData.username }}</p>
        <p>성별: {{ userData.gender }}</p>
        <p>지역: {{ userData.region }}</p>
        <p>주거래은행: {{ userData.main_bank }}</p>
        <p>예적금 여부: {{ userData.financial_products }}</p>
        <p>희망 예적금 기간: {{ userData.desire_period }}</p>
        <p>나이: {{ userData.age }}</p>
        <p>월소득: {{ userData.income }}</p>
        <p>월소비: {{ userData.consume }}</p>
        <p>최종 학력: {{ userData.grade }}</p>
        <p>직업: {{ userData.job }}</p>
      </div>
    </div>
  </template>
  
  <script setup>
  import { ref } from 'vue';
  
  // 메시지 리스트
  const messages = [
    "안녕하세요! 저는 당신의 경제 생활 매니저 모아에요!",
    "지금부터 시작해볼까요?",
    "좋아요! 당신이 사용할 닉네임은 무엇인가요?",
    " {{userData.value.nickname }}사용할 아이디를 입력해주세요!",
    "사용할 비밀번호를 입력해주세요!",
    "좋아요! 성별은요?",
    "나이를 알려주시면 좋을 것 같아요!",
    "어느 지역에 살고 계시나요?",
    "주거래 은행을 선택해주세요!",
    "예적금을 넣고 계신가요?",
    "혹시 추가로 예적금을 넣는다면 원하시는 기간은 얼마정도 될까요?",
    "월소득은 얼마쯤 되세요?",
    "월소비는 얼마쯤 되세요?",
    "최종 학력을 선택해주세요!",
    "직업을 선택해주세요!",
    "감사합니다! {{userData.nickname}}님이 입력해주신 자료를 바탕으로 리포트를 만들고 있어요!",
  ];
  
  // 사용자 데이터 상태
  const userData = ref({
    username: "",
    nickname: "",
    password1: "",
    password2: "",
    gender: "",
    job: "",
    grade: "",
    main_bank: "",
    region: "",
    age: null,
    income: null,
    consume: null,
    desire_period: null,
    financial_products: "",
  });
  
  // 상태 관리
  const currentIndex = ref(0);
  const displayedText = ref("");
  const isTypingComplete = ref(false);
  const submitted = ref(false);
  
  // 입력 필드 표시 관리
  const showNameInput = ref(false);
  const showGenderSelection = ref(false);
  const showFinancialProductsSelection = ref(false);
  const showDesirePeriod = ref(false)
  const showNumericInput = ref(false);
  const showJobSelection = ref(false);
  const showGradeSelection = ref(false);
  const showRegionInput = ref(false);
  const showMainBank = ref(false);
  const showNicknameInput = ref(false);
  const showPasswordInput = ref(false);
  const showInputFields = ref(false); // 현재 입력 필드 표시 여부
  
  // 숫자 입력 상태
  const numericInput = ref(null);
  const currentPlaceholder = ref("숫자를 입력하세요");
  
  // 메시지 출력
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
    }, 40);
  }
  
  // 입력 필드 초기화
  function resetInputFields() {
    showNameInput.value = false;
    showGenderSelection.value = false;
    showFinancialProductsSelection.value = false;
    showNumericInput.value = false;
    showJobSelection.value = false;
    showGradeSelection.value = false;
    showRegionInput.value = false;
    showMainBank.value = false;
    showNicknameInput.value = false;
    showPasswordInput.value = false;
    showInputFields.value = false;
  }
  
  // 입력 필드 표시 관리
  function handleInputFields() {
    const currentMessage = messages[currentIndex.value];
    if (currentMessage.includes("닉네임")) showNicknameInput.value = true;
    if (currentMessage.includes("아이디")) showNameInput.value = true;
    if (currentMessage.includes("비밀번호")) showPasswordInput.value = true;
    if (currentMessage.includes("성별")) showGenderSelection.value = true;
    if (currentMessage.includes("나이")) {
      showNumericInput.value = true;
      currentPlaceholder.value = "나이를 입력하세요";
    }
    if (currentMessage.includes("지역")) showRegionInput.value = true;
    if (currentMessage.includes("주거래")) showMainBank.value = true;
    if (currentMessage.includes("예적금을 넣고")) showFinancialProductsSelection.value = true;
    if (currentMessage.includes("기간")) {
      showNumericInput.value = true;
      currentPlaceholder.value = "기간을 입력하세요(달)";
    }
    if (currentMessage.includes("월소득")) {
      showNumericInput.value = true;
      currentPlaceholder.value = "월소득을 입력하세요";
    }
    if (currentMessage.includes("월소비")) {
      showNumericInput.value = true;
      currentPlaceholder.value = "월소비를 입력하세요";
    }
    if (currentMessage.includes("학력")) showGradeSelection.value = true;
    if (currentMessage.includes("직업")) showJobSelection.value = true;
  
    // 입력 필드가 표시 중인지 확인
    showInputFields.value =
      showNameInput.value ||
      showNicknameInput.value ||
      showPasswordInput.value ||
      showGenderSelection.value ||
      showFinancialProductsSelection.value ||
      showNumericInput.value ||
      showJobSelection.value ||
      showGradeSelection.value ||
      showRegionInput.value ||
      showMainBank.value;
  }
  
  // 메시지 전환
  function nextMessage() {
    if (currentIndex.value < messages.length - 1) {
      currentIndex.value++;
      const nextMsg = messages[currentIndex.value];
      typeMessage(nextMsg);
  
      if (currentIndex.value === messages.length - 1) {
        submitted.value = true;
      }
    }
  }
  
  // 입력 저장 및 처리 함수
  function saveNickname() {
    if (userData.value.nickname.trim()) {
      resetInputFields();
      nextMessage();
    }
  }
  
  function saveName() {
    if (userData.value.username.trim()) {
      resetInputFields();
      nextMessage();
    }
  }
  
  function savePasswords() {
    // 비밀번호가 일치할 때만 진행
    if (userData.value.password1 && userData.value.password2) {
      if (userData.value.password1 === userData.value.password2) {
        resetInputFields();
        nextMessage();
      } else {
        alert("비밀번호가 일치하지 않습니다. 다시 입력해주세요.");
      }
    }
  }
  
  
  function setGender(gender) {
    userData.value.gender = gender;
    resetInputFields();
    nextMessage();
  }
  
  function setSavings(financial_products) {
    userData.value.financial_products = financial_products;
    resetInputFields();
    nextMessage();
    }
  
  
  function saveNumericInput() {
    if (currentPlaceholder.value.includes("나이")) userData.value.age = numericInput.value;
    if (currentPlaceholder.value.includes("월소득")) userData.value.income = numericInput.value;
    if (currentPlaceholder.value.includes("월소비")) userData.value.consume = numericInput.value;
    if (currentPlaceholder.value.includes("기간")) userData.value.desire_period = numericInput.value;
    numericInput.value = null;
    resetInputFields();
    nextMessage();
  }
  
  function saveRegion() {
    if (userData.value.region.trim()) {
      resetInputFields();
      nextMessage();
    }
  }
  
  function saveMainBank() {
    if (userData.value.main_bank.trim()) {
      resetInputFields();
      nextMessage();
    }
  }
  
  function saveGrade() {
    if (userData.value.grade) {
      resetInputFields();
      nextMessage();
    }
  }
  
  function saveJob() {
    if (userData.value.job) {
      resetInputFields();
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
    
<template>
  <div class="survey-container">
    <!-- 왼쪽 배너 -->
    <aside class="input-summary" v-show="!showReport">
  <ul>
    <li v-if="userData.nickname" class="circle-item">{{ userData.nickname }}</li>
    <li v-if="userData.username" class="circle-item">{{ userData.username }}</li>
    <li v-if="userData.gender" class="circle-item">{{ userData.gender }}</li>
    <li v-if="userData.age" class="circle-item">{{ userData.age }}</li>
    <li v-if="userData.region" class="circle-item">{{ userData.region }}</li>
    <li v-if="userData.main_bank" class="circle-item">{{ userData.main_bank }}</li>
    <li v-if="userData.income" class="circle-item">{{ userData.income }}만원</li>
    <li v-if="userData.consume" class="circle-item">{{ userData.consume }}만원</li>
    <li v-if="userData.grade" class="circle-item">{{ userData.grade }}</li>
    <li v-if="userData.job" class="circle-item">{{ userData.job }}</li>
    <li v-if="userData.desire_period" class="circle-item">{{ userData.desire_period }}개월</li>
  </ul>
</aside>



    
    <!-- 메인 설문지 영역 -->
    <main class="form-area" v-if="!showReport">
      <p v-if="!showReport" class="message">{{ displayedText }}</p>

      <!-- 닉네임, 아이디, 비밀번호 입력 -->
      <div v-if="showNicknameInput">
        <input v-model="userData.nickname" type="text" placeholder="닉네임을 입력하세요" class="input" />
        <input v-model="userData.username" type="text" placeholder="아이디를 입력하세요" class="input" />
        <input v-model="userData.password1" type="password" placeholder="비밀번호를 입력하세요" class="input" />
        <input v-model="userData.password2" type="password" placeholder="비밀번호를 다시 입력하세요" class="input" />
      </div>

      <!-- 성별 선택 -->
      <div v-if="showGenderSelection">
        <button @click="setGender('남자')" class="next-button">남성</button>
        <button @click="setGender('여자')" class="next-button">여성</button>
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
          <option value="경영·사무·금융·보험직">경영·사무·금융·보험직</option>
          <option value="연구직 및 공학 기술직">연구직 및 공학 기술직</option>
          <option value="교육·법률·사회복지·경찰·소방직 및 군인">교육·법률·사회복지·경찰·소방직 및 군인</option>
          <option value="보건·의료직">보건·의료직</option>
          <option value="예술·디자인·방송·스포츠직">예술·디자인·방송·스포츠직</option>
          <option value="미용·여행·숙박·음식·경비·청소직">미용·여행·숙박·음식·경비·청소직</option>
          <option value="영업·판매·운전·운송직">영업·판매·운전·운송직</option>
          <option value="건설·채굴직">건설·채굴직</option>
          <option value="설치·정비·생산직">설치·정비·생산직</option>
          <option value="농림어업직">농림어업직</option>
          <option value="미분류">미분류</option>
        </select>
      </div>

    <!-- 예적금 기간 입력 -->
      <div v-if="showNumericInput">
        <input v-model.number="numericInput" type="number" :placeholder="currentPlaceholder" class="input" />
      </div>

      <!-- 예적금여부 선택 -->
    <div v-if="showDepositTrueFalse">
        <button @click="saveProductsYesNo(1)" class="next-button">예</button>
        <button @click="saveProductsYesNo(0)" class="next-button">아니오</button>
      </div>

        <!-- 확인 버튼 -->
        <button v-if="isTypingComplete && !submitted && !showDepositTrueFalse && !showGenderSelection" @click="saveAllResponses" class="next-button">
      확인
    </button>
    </main>



  
  <!-- 결과 출력 -->
  <div v-if="submitted && !showReport">
    <h3>입력된 정보</h3>
    <p>닉네임: {{ userData.nickname }}</p>
    <p>아이디: {{ userData.username }}</p>
    <p>성별: {{ userData.gender }}</p>
    <p>지역: {{ userData.region }}</p>
    <p>주거래은행: {{ userData.main_bank }}</p>
    <p>예적금 기간: {{ userData.desire_period }}</p>
    <p>예적금 여부: {{ yesno }}</p>
    <p>나이: {{ userData.age }}</p>
    <p>월소득: {{ userData.income }}</p>
    <p>월소비: {{ userData.consume }}</p>
    <p>최종 학력: {{ userData.grade }}</p>
    <p>직업: {{ userData.job }}</p>
    <button  @click="registerUser" class="next-button">회원가입</button>
  </div>

    
      <!-- 결과 리포트 -->
      <div v-if="showReport">
      <h2>🎉 {{ userData.nickname }}님의 맞춤형 리포트</h2>
      <p><strong>소득 분석:</strong> {{ recommendations.income_analysis }}</p>
      <p><strong>소득 분위:</strong> {{ recommendations.income_decile }}</p>
      <p><strong>소비 분석:</strong> {{ recommendations.spending_analysis }}</p>
      <p><strong>예상 세금:</strong> {{ recommendations.tax_refund_estimation.annual_income_tax }}</p>
      <p><strong>세금 환급 예상:</strong> {{ recommendations.tax_refund_estimation.refund_estimation }}</p>
      <p><strong>동일 직업 소비 수준 분석:</strong> {{ recommendations.job_analysis }}</p>
      <p><strong>동일 학력 소비 수준 분석:</strong> {{ recommendations.grade_analysis }}</p>

      <div class="chartsize">
        <div>
          <h3>성별/연령대 소득 비교</h3>
          <Bar
            v-if="genderAgeChartData.datasets.length && jobChartData.datasets.length && gradeChartData.datasets.length"
            :chart-data="genderAgeChartData"
            :options="chartOptions"
          />
        </div>

        <div>
          <h3>직군 소득 비교</h3>
          <Bar
            v-if="genderAgeChartData.datasets.length && jobChartData.datasets.length && gradeChartData.datasets.length"
            :chart-data="jobChartData"
            :options="chartOptions"
          />
        </div>

        <div>
          <h3>학력별 소득 비교</h3>
          <Bar
            v-if="genderAgeChartData.datasets.length && jobChartData.datasets.length && gradeChartData.datasets.length"
            :chart-data="gradeChartData"
            :options="chartOptions"
          />
        </div>
      </div>

      <h3>추천 카드</h3>
      <ul>
        <li v-for="(card, index) in recommendations.card_recommendations" :key="index">
          {{ card.card_name }} - {{ card.merit_summary }}
        </li>
      </ul>

      <h3>추천 예금 상품</h3>
      <ul>
        <li v-for="(deposit, index) in recommendations.deposit_recommendations" :key="index">
          {{ deposit.name }} - {{ deposit.max_interest_rate }}% ({{ deposit.term }}) - {{ deposit.bank_name }}
        </li>
      </ul>

      <h3>추천 적금 상품</h3>
      <ul>
        <li v-for="(saving, index) in recommendations.saving_recommendations" :key="index">
          {{ saving.name }} - {{ saving.max_interest_rate }}% ({{ saving.term }}) - {{saving.bank_name}}
        </li>
      </ul>
      <!-- 리포트 저장 버튼 -->
      <button @click="saveReport(tempuserId)" class="save-button">리포트 저장하기</button>
    </div>
    
  </div>
   <!-- 메인으로 가기 버튼 -->
      <button @click="goToMain" class="main-button">메인으로 가기</button>

  
</template>


<script setup>
import {  useRouter } from 'vue-router';
import { onMounted } from 'vue'
import { ref } from "vue";
import { useCounterStore } from "@/stores/counter";
const store = useCounterStore()
const router = useRouter(); // 라우터 인스턴스 가져오기
const goToMain = () => {
  router.push({ path: "/" }); // 메인 페이지로 이동
};



// 메시지 리스트
const messages = [
  "안녕하세요! 저는 당신의 경제 생활 매니저 모아에요!",
  "닉네임, 아이디, 비밀번호를 입력해주세요.",
  "성별을 선택해주세요.",
  "나이, 지역, 주거래 은행을 입력해주세요.",
  "월소득과 월소비를 입력해주세요.",
  "최종 학력과 직업을 선택해주세요.",
  "예적금을 현재 넣고 계신가요?",
  "추가로 넣게 된다면 희망 예적금 기간을 입력해주세요.",
  "",
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

// 추천 결과 상태
const recommendations = ref({});
const showReport = ref(false);

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
const showDepositTrueFalse = ref(false) // 예적금 넣고있는지 여부
const yesno = ref("")
// 숫자 입력 상태
const numericInput = ref(null);
const currentPlaceholder = ref("숫자를 입력하세요");

const change = function () {
  if (showDepositTrueFalse.value == true) {
    yesno.value = "X"
  } else {
    yesno.value = "O"
  }
}

// userId 임시저장
let tempuserId = null

// 메시지 출력
function typeMessage(message) {
  displayedText.value = "";
  isTypingComplete.value = false;
  resetInputFields();

  if (currentIndex.value === messages.length - 1) {
    message =  `감사합니다! ${userData.value.nickname}님이 입력해주신 자료를 바탕으로 리포트를 만들고 있어요!`;
  }

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
  showDepositTrueFalse.value = false
}

// 입력 필드 표시 관리
function handleInputFields() {
  const currentMessage = messages[currentIndex.value];
  if (currentMessage.includes("닉네임")) {
    showNicknameInput.value = true;
    showNameInput.value = true;
    showPasswordInput.value = true;
  }
  if (currentMessage.includes('예적금을 현재')) showDepositTrueFalse.value = true
  if (currentMessage.includes("성별")) showGenderSelection.value = true;
  if (currentMessage.includes("나이")) showMultiInputs.value = true;
  if (currentMessage.includes("월소득")) showNumericInputs.value = true;
  if (currentMessage.includes("학력")) showDropdownInputs.value = true;
  if (currentMessage.includes("예적금 기간")) {
    showNumericInput.value = true;
    currentPlaceholder.value = "기간을 입력하세요(달)";
  }
}

function setGender(gender) {
  userData.value.gender = gender; // 성별 저장
  resetInputFields(); // 현재 입력 필드 초기화
  nextMessage(); // 다음 메시지로 이동
}

function saveProductsYesNo(a) {
  userData.value.financial_products = a; // 성별 저장
  resetInputFields(); // 현재 입력 필드 초기화
  nextMessage(); // 다음 메시지로 이동
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
  change()
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


// 회원가입 요청 함수
async function registerUser() {
  const url = `${store.API_URL}/dj-rest-auth/registration/`; // Django의 회원가입 API URL

  // 사용자 데이터를 POST 요청으로 전송
 try {
    const response = await fetch(url, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        username: userData.value.username,
        password1: userData.value.password1,
        password2: userData.value.password2,
        nickname: userData.value.nickname,
        gender: userData.value.gender,
        region: userData.value.region,
        main_bank: userData.value.main_bank,
        age: userData.value.age,
        income: userData.value.income ,
        consume: userData.value.consume ,
        grade: userData.value.grade,
        job: userData.value.job,
        desire_period: userData.value.desire_period,
        financial_products : userData.value.financial_products,
      }),
    });

    if (response.ok) {
      const result = await response.json();
      alert("회원가입 성공!");
      console.log(result);
      const token = result.key;

      const username = userData.value.username;
      const password = userData.value.password1; // 사용자가 입력한 비밀번호
      await store.logIn2({ username, password }); // Pinia 스토어의 logIn 함수 호출

      const userInfoResponse = await fetch(`${store.API_URL}/dj-rest-auth/user/`, {
        method: "GET",
        headers: {
          "Authorization": `Token ${token}`,
        },
      });
      if (userInfoResponse.ok) {
        const userInfo = await userInfoResponse.json();
        const userId = userInfo.pk; // 사용자 ID 가져오기
        tempuserId = userId
        console.log(userId,'dskfj')
        fetchRecommendations(userId); // 추천 API 호출
      } else {
        alert("사용자 정보를 가져오는 데 실패했습니다.");
      }
    } else {
      const errorData = await response.json();
      alert(`회원가입 실패: ${JSON.stringify(errorData)}`);
    }
  } catch (error) {
    console.error("회원가입 요청 중 오류 발생:", error);
    alert("회원가입 요청 중 오류가 발생했습니다.");
  }
}

// 리포터 저장함수
async function saveReport(userId) {
  const url = `${store.API_URL}/api/v1/save_profile/${userId}/`;
  console.log(userId, '12345')
  const counter = localStorage.getItem("counter");
  console.log(counter)
  if (!counter) {
    alert("로그인이 필요합니다.");
    return;
  }

  const counterData = JSON.parse(counter);
  const token = counterData?.token;
  if (!token) {
    alert("로그인이 필요합니다.");
    return;
  }


  try {
    console.log(token)
    const response = await fetch(url, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        "Authorization": `Token ${token}`, // 인증 토큰 사용
      },
      body: JSON.stringify(recommendations.value), // Vue의 recommendations 데이터 전송
    });

    if (response.ok) {
      alert("리포트가 성공적으로 저장되었습니다!");
    } else {
      const errorData = await response.json();
      console.error("리포트 저장 실패:", errorData);
    }
  } catch (error) {
    console.error("리포트 저장 요청 중 오류 발생:", error);
  }
}
// 추천 결과 API 호출

async function fetchRecommendations(userId) {
  const url = `${store.API_URL}/data/recommend_view/${userId}/`;
 
  try {
    const response = await fetch(url);
    console.log(userId)
    if (response.ok) {
      const result = await response.json();
      recommendations.value = result; // 추천 결과 저장


      // db와 연결해서 report저장
      // 리포트 저장 호출
      // await saveReport(userId);
      // print(saveReport)

      showReport.value = true; // 리포트 표시
    } else {
      console.error("추천 API 오류:", await response.json());
    }
  } catch (error) {
    console.error("추천 API 호출 중 오류 발생:", error);
  }
}


import { watch } from 'vue';

watch(recommendations, (newRecommendations) => {
  if (newRecommendations) {
    // 그래프 데이터를 설정하는 로직
    updateGraphs(newRecommendations);
  }
});




import { Bar } from "vue-chartjs";

import {
  Chart as ChartJS,
  Title,
  Tooltip,
  Legend,
  BarElement,
  CategoryScale,
  LinearScale,
} from "chart.js";
import { useRoute } from 'vue-router';

// Chart.js 컴포넌트 등록
ChartJS.register(Title, Tooltip, Legend, BarElement, CategoryScale, LinearScale);


// 그래프 데이터
const genderAgeChartData = ref({ labels: [], datasets: [] });
const jobChartData = ref({ labels: [], datasets: [] });
const gradeChartData = ref({ labels: [], datasets: [] });
const chartOptions = {
  responsive: true,
  plugins: {
    legend: { position: "top" },
    title: { display: true, text: "소득 비교" },
  },
};

// 비교 로직
function adjustHeight(comparisonText = "비슷합니다") {
  if (comparisonText.includes("높습니다")) return 3; // 높으면 높게 표시
  if (comparisonText.includes("낮습니다")) return 1; // 낮으면 낮게 표시
  return 2; // 비슷하면 중간 높이
}

// 리포트 데이터 로드

  
// 그래프 데이터 업데이트 함수
function updateGraphs(recommendations) {
  const genderHeight = adjustHeight(recommendations.income_analysis || "비슷합니다");
  const gradeHeight = adjustHeight(recommendations.grade_analysis || "비슷합니다");
  const jobHeight = adjustHeight(recommendations.job_analysis || "비슷합니다");

    // 성별/연령별 그래프 데이터
    genderAgeChartData.value = {
    labels: ["성별 평균"],
    datasets: [
      {
        label: "사용자 소득 (상대적 높이)",
        data: [genderHeight],
        backgroundColor: "rgba(75, 192, 192, 0.6)",
        borderColor: "rgba(75, 192, 192, 1)",
        borderWidth: 1,
      },
      {
        label: "평균 소득 (실제 값)",
        data: [2],
        backgroundColor: "rgba(255, 99, 132, 0.6)",
        borderColor: "rgba(255, 99, 132, 1)",
        borderWidth: 1,
      },
    ],
  };

  gradeChartData.value = {
    labels: ["학력별 평균"],
    datasets: [
      {
        label: "사용자 소득 (상대적 높이)",
        data: [gradeHeight],
        backgroundColor: "rgba(75, 192, 192, 0.6)",
        borderColor: "rgba(75, 192, 192, 1)",
        borderWidth: 1,
      },
      {
        label: "평균 소득 (실제 값)",
        data: [2],
        backgroundColor: "rgba(255, 99, 132, 0.6)",
        borderColor: "rgba(255, 99, 132, 1)",
        borderWidth: 1,
      },
    ],
  };

  // 직군별 그래프 데이터
  jobChartData.value = {
    labels: ["직군 평균"],
    datasets: [
      {
        label: "사용자 소득 (상대적 높이)",
        data: [jobHeight],
        backgroundColor: "rgba(54, 162, 235, 0.6)",
        borderColor: "rgba(54, 162, 235, 1)",
        borderWidth: 1,
      },
      {
        label: "평균 소득 (실제 값)",
        data: [2],
        backgroundColor: "rgba(255, 205, 86, 0.6)",
        borderColor: "rgba(255, 205, 86, 1)",
        borderWidth: 1,
      },
    ],
  };
}

// Watch로 recommendations 변화 감지
watch(recommendations, (newRecommendations) => {
  if (newRecommendations && Object.keys(newRecommendations).length) {
    updateGraphs(newRecommendations);
  }
});

</script>

<style scoped>
.survey-container {
  display: flex;
  flex-wrap: nowrap; /* 줄바꿈 허용하지 않음 */
  border: 2px solid #ddd;
  border-radius: 10px;
  padding: 20px;
  gap: 20px;
  background-color: #f9f9f9;
  width: 70%; /* 전체 화면의 70%를 사용 */
  height: 600px; /* 고정된 전체 높이 */
  margin: 0 auto; /* 중앙 정렬 */
}
/* 왼쪽 배너 스타일 */
.input-summary {
  width: 300px; /* 고정된 왼쪽 영역 너비 */
  background-color: #f0f0f0;
  border-radius: 10px;
  padding: 20px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  overflow: auto; /* 스크롤 가능 */
}
.input-summary ul {
  list-style: none;
  padding: 0;
  display: flex;
  flex-wrap: wrap; /* 줄바꿈 허용 */
  gap: 20px; /* 원 사이 간격 */
  justify-content: center; /* 가운데 정렬 */
}
.input-summary h3 {
  font-size: 18px;
  color: #007bff;
  margin-bottom: 15px;
  text-align: center;
}

.input-summary li {
  width: 120px; /* 고정된 타원의 가로 크기 */
  height: 80px; /* 고정된 타원의 세로 크기 */
  display: flex;
  align-items: center;
  justify-content: center;
  background-color: #ffffff; /* 흰색 배경 */
  border-radius: 50% 40%; /* 비대칭 타원형 */
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1); /* 부드러운 그림자 */
  font-size: 14px;
  font-weight: bold;
  color: #333;
  border: 2px solid #007bff; /* 파란색 테두리 */
  transition: transform 0.2s ease, background-color 0.2s ease;
}

.input-summary li:hover {
  transform: scale(1.1); /* 호버 시 확대 */
  background-color: #f0f8ff; /* 호버 시 배경색 변화 */
}

/* 메인 설문지 영역 스타일 */
/* 메인 설문지 영역 스타일 */
.form-area {
  flex: 1;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: flex-start;
  background-color: white;
  border-radius: 10px;
  padding: 20px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  overflow: auto; /* 스크롤 가능 */
}

.input {
  width: 80%;
  margin: 10px 0;
  padding: 10px;
  border: 1px solid #ddd;
  border-radius: 8px;
}


.next-button {
  margin-top: 10px;
  padding: 10px 20px;
  border: none;
  border-radius: 8px;
  background-color: #007bff;
  color: white;
  font-weight: bold;
  cursor: pointer;
}

.next-button:hover {
  background-color: #0056b3;
}


.chartsize {
  display: flex; /* 차트를 가로로 나열 */
  flex-wrap: wrap; /* 화면 크기에 따라 차트가 줄 바꿈될 수 있도록 설정 */
  justify-content: space-between; /* 차트 간 간격을 균등 분배 */
  gap: 20px; /* 차트 사이의 간격 */
  padding: 20px;
}

.chartsize h3 {
  text-align: center;
  font-size: 16px;
  margin-bottom: 10px;
  width: 100%; /* 제목은 각 줄의 전체 너비를 차지 */
}

.chartsize > * {
  flex: 1 1 calc(33.333% - 20px); /* 차트가 3등분으로 배치되도록 설정 */
  max-width: calc(33.333% - 20px); /* 각 차트 최대 너비 제한 */
  display: flex;
  flex-direction: column; /* 제목과 차트를 세로로 배치 */
  align-items: center;
}

.chartsize canvas {
  width: 100% !important; /* 차트 크기를 부모 컨테이너에 맞춤 */
  height: auto !important; /* 비율을 유지하며 높이를 자동 조정 */
}

</style> 
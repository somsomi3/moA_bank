<template>
  <div class="container">
    <h1 class="mypage-title">마이페이지</h1>

    <!-- 개인정보 섹션 -->
    <div class="section">
      <h2>개인정보</h2>
      <div class="section-content">
        <p><strong>닉네임:</strong> {{ userData.nickname }}</p>
        <p><strong>아이디:</strong> {{ userData.username }}</p>
        <p><strong>성별:</strong> {{ userData.gender }}</p>
        <p><strong>나이:</strong> {{ userData.age }}</p>
        <p><strong>지역:</strong> {{ userData.region }}</p>
        <p><strong>주거래 은행:</strong> {{ userData.main_bank }}</p>
        <p><strong>월소득:</strong> {{ userData.income }}만원</p>
        <p><strong>월소비:</strong> {{ userData.consume }}만원</p>
        <p><strong>최종 학력:</strong> {{ userData.grade }}</p>
        <p><strong>직업:</strong> {{ userData.job }}</p>
        <p><strong>예적금 여부:</strong> {{ userData.financial_products ? '예' : '아니오' }}</p>
        <p><strong>희망 예적금 기간:</strong> {{ userData.desire_period }}개월</p>
      </div>
    </div>

    <!-- 리포트 섹션 -->
    <div class="section">
      <h2>저장된 리포트</h2>
      <div class="section-content">
        <div v-if="report">
          <p><strong>소득 분석:</strong> {{ report.income_analysis }}</p>
          <p><strong>소득 분위:</strong> {{ report.income_decile }}</p>
          <p><strong>소비 분석:</strong> {{ report.spending_analysis }}</p>
          <p><strong>세금 환급 예상:</strong> {{ report.tax_refund_estimation.refund_estimation }}</p>
          <p><strong>동일 직업 소비 수준 분석:</strong> {{ report.job_analysis }}</p>
          <p><strong>동일 학력 소비 수준 분석:</strong> {{ report.grade_analysis }}</p>

          <h3>추천 카드</h3>
          <ul class="recommendation-list">
            <li v-for="(card, index) in report.card_recommendations" :key="index">
              {{ card.card_name }} - {{ card.merit_summary }}
            </li>
          </ul>

          <h3>추천 예금 상품</h3>
          <ul class="recommendation-list">
            <li v-for="(deposit, index) in report.deposit_recommendations" :key="index">
              {{ deposit.name }} - {{ deposit.rate }}% ({{ deposit.term }})
            </li>
          </ul>

          <h3>추천 적금 상품</h3>
          <ul class="recommendation-list">
            <li v-for="(saving, index) in report.saving_recommendations" :key="index">
              {{ saving.name }} - {{ saving.rate }}% ({{ saving.term }})
            </li>
          </ul>
        </div>
        <p v-else>저장된 리포트가 없습니다.</p>
      </div>
    </div>
  </div>
</template>



<script setup>
import { ref, onMounted } from "vue";
import { useCounterStore } from "@/stores/counter";
const store = useCounterStore()
// 상태 변수
const userData = ref({
  nickname: "",
  username: "",
  gender: "",
  age: null,
  region: "",
  main_bank: "",
  income: null,
  consume: null,
  grade: "",
  job: "",
  financial_products: null,
  desire_period: null,
});
const report = ref(null);

async function fetchUserIdFromServer(token) {
  try {
    const response = await fetch(`${store.API_URL}/api/v1/profile/`, {
      method: "GET",
      headers: {
        "Content-Type": "application/json",
        "Authorization": `Token ${token}`, // 인증 토큰 사용
      },
    });

    if (response.ok) {
      const userData = await response.json();
      console.log(userData.id)
      return userData.id; // 서버에서 반환된 user_id
    } else {
      console.error("서버에서 user_id를 가져오지 못했습니다:", await response.json());
      return null;
    }
  } catch (error) {
    console.error("서버 요청 중 오류 발생:", error);
    return null;
  }
}

async function fetchMyPageData() {
  const counter = localStorage.getItem("counter");
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

  // 사용자 ID 가져오기
  const user_id = await fetchUserIdFromServer(token);
  if (!user_id) {
    alert("사용자 정보를 불러오는 데 실패했습니다.");
    return;
  }

  const url = `${store.API_URL}/api/v1/save_profile/${user_id}/`;
  
  try {
    const response = await fetch(url, {
      method: "GET",
      headers: {
        "Content-Type": "application/json",
        "Authorization": `Token ${token}`,
      },
    });

    if (response.ok) {
      const result = await response.json();
      console.log(result)
      userData.value = result.user_data; // 사용자 정보 저장
      report.value = result.report; // 리포트 데이터 저장
      // console.log("사용자 데이터:", userData.value);
      // console.log("리포트 데이터:", report.value);
    } else {
      const errorData = await response.json();
      console.error("마이페이지 데이터 가져오기 실패:", errorData);
    }
  } catch (error) {
    console.error("마이페이지 요청 중 오류 발생:", error);
  }
}
onMounted(async () => {
  await fetchMyPageData();
});
</script>

<style scoped>
/* 스타일 업데이트 */
.section-content {
  overflow: auto; /* 스크롤을 추가하여 잘리지 않도록 함 */
  word-wrap: break-word; /* 긴 텍스트 줄 바꿈 */
  max-width: 100%; /* 콘텐츠가 섹션 박스를 초과하지 않도록 제한 */
}

.recommendation-list li {
  margin: 8px 0;
  padding: 8px; /* 패딩을 줄여서 내용 표시 영역 확대 */
  border: 1px solid #ddd;
  border-radius: 8px;
  background-color: #ffffff;
  max-width: 100%;
  font-size: 14px; /* 글씨 크기를 줄여서 더 많은 내용 표시 */
  overflow: hidden;
}

.recommendation-list li:hover {
  background-color: #f1f3f5;
}

.section-content > div {
  max-width: 100%;
  overflow: hidden;
}

.section {
  margin-bottom: 30px;
  padding: 20px;
  border: 1px solid #e0e0e0;
  border-radius: 12px;
  background-color: #f9f9f9;
  box-shadow: 0 2px 6px rgba(0, 0, 0, 0.05);
  overflow: hidden;
}

p,
.recommendation-list li {
  font-size: 14px; /* 모든 텍스트 크기 줄이기 */
  line-height: 1.4; /* 텍스트 줄 간격 축소 */
}

h3 {
  font-size: 16px; /* 제목 크기 조정 */
}

.recommendation-list {
  list-style: none;
  padding: 0;
  margin: 0;
}

.recommendation-list li {
  margin: 8px 0;
}

</style>


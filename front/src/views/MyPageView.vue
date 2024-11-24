

<!-- 헬로 뷰에 있는 레포드
 레포드를 마이페이지에 저장해야함.. 아마 "백엔드 ""모델로""" 연결"해서
 db에 저장해야 할 거같은데? -->

 <template>
  <div class="container">
    <h1>마이페이지</h1>
    <div class="content">
      <!-- 왼쪽: 입력한 개인정보 -->
      <div class="user-info">
        <h2>개인정보</h2>
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

      <!-- 오른쪽: 리포트 -->
      <div class="report-info">
        <h2>저장된 리포트</h2>
        <div v-if="report">
          <p><strong>소득 분석:</strong> {{ report.income_analysis }}</p>
          <p><strong>소득 분위:</strong> {{ report.income_decile }}</p>
          <p><strong>소비 분석:</strong> {{ report.spending_analysis }}</p>
          <p><strong>세금 환급 예상:</strong> {{ report.tax_refund_estimation.refund_estimation }}</p>
          <p><strong>동일 직업 소비 수준 분석:</strong> {{ report.job_analysis }}</p>
          <p><strong>동일 학력 소비 수준 분석:</strong> {{ report.grade_analysis }}</p>

          <h3>추천 카드</h3>
          <ul>
            <li v-for="(card, index) in report.card_recommendations" :key="index">
              {{ card.card_name }} - {{ card.merit_summary }}
            </li>
          </ul>

          <h3>추천 예금 상품</h3>
          <ul>
            <li v-for="(deposit, index) in report.deposit_recommendations" :key="index">
              {{ deposit.name }} - {{ deposit.rate }}% ({{ deposit.term }})
            </li>
          </ul>

          <h3>추천 적금 상품</h3>
          <ul>
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

// 마이페이지 데이터 가져오기
async function fetchMyPageData() {
  const url = "http://127.0.0.1:8000/save_profile/"; // 백엔드 마이페이지 API 엔드포인트
  const token = localStorage.getItem("userToken");

  if (!token) {
    alert("로그인이 필요합니다.");
    return;
  }

  try {
    const response = await fetch(url, {
      method: "GET",
      headers: {
        "Content-Type": "application/json",
        "Authorization": `Token ${token}`, // 인증 토큰 사용
      },
    });

    if (response.ok) {
      const result = await response.json();
      userData.value = result.user_data; // 사용자 정보 저장
      report.value = result.report; // 리포트 데이터 저장
    } else {
      console.error("마이페이지 데이터 가져오기 실패:", await response.json());
    }
  } catch (error) {
    console.error("마이페이지 요청 중 오류 발생:", error);
  }
}

// 컴포넌트 로드 시 데이터 가져오기
onMounted(() => {
  fetchMyPageData();
});
</script>

<style scoped>
.container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 20px;
  font-family: Arial, sans-serif;
}

.content {
  display: flex;
  gap: 20px;
}

.user-info,
.report-info {
  flex: 1;
  padding: 20px;
  border: 1px solid #ddd;
  border-radius: 8px;
  background-color: #f9f9f9;
}

h1 {
  text-align: center;
  margin-bottom: 20px;
}

h2 {
  color: #333;
}

p {
  margin: 5px 0;
  color: #555;
}

ul {
  list-style: none;
  padding: 0;
}

li {
  margin: 5px 0;
}
</style>

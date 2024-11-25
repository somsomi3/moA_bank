<template>
 <div class="container">
    <!-- 왼쪽 세로 배너 -->
    <aside class="vertical-banner">
      <h2>상품 카테고리</h2>
      <ul class="menu-list">
        <li @click="fetchCategoryItems('deposit')">예금 리스트 보기</li>
        <li @click="fetchCategoryItems('saving')">적금 리스트 보기</li>
        <li @click="fetchCategoryItems('card')">카드 리스트 보기</li>
      </ul>
    </aside>

    <!-- 본문 컨텐츠 -->
    <main class="content">
      <h1>상품 검색</h1>

<!-- 카테고리 선택 버튼 -->
<div class="button-container">
      <button
        v-for="(label, category) in categoryLabels"
        :key="category"
        class="category-button"
        @click="setCategory(category)"
      >
        {{ label }}
      </button>
    </div>

      <!-- 검색 입력창 -->
      <div v-if="selectedCategory">
        <h2>{{ categoryLabel }} 상품 검색</h2>
        <form @submit.prevent="fetchProducts" class="search-form">
          <label for="search">검색:</label>
          <input
            type="text"
            id="search"
            v-model="query"
            placeholder="상품명을 입력하세요"
            class="search-input"
          />
          <button type="submit" class="search-button">검색</button>
        </form>
      </div>

      <!-- 로딩 상태 -->
      <div v-if="loading" class="loading">로딩 중...</div>

            <!-- 검색 결과 -->
      <div v-if="products.length">
        <h1>검색 결과</h1>
        <ul class="product-list">
          <li
            v-for="(product, index) in products"
            :key="index"
            class="product-item"
          >
            <!-- 공통 상품 정보 -->
            <h3>{{ product.fin_prdt_nm || product.card_name }}</h3>
            <p v-if="product.kor_co_nm || product.bank">
              은행: {{ product.kor_co_nm || product.bank }}
            </p>
            <p>상세정보: {{ product.etc_note || product.merit_summary }}</p>
            <p v-if="product.max_limit">최고 가입한도: {{ product.max_limit }}</p>
            <p v-if="product.notification">알림: {{ product.notification }}</p>
            <p v-if="product.annual_fee">연회비: {{ product.annual_fee }}</p>

            <!-- 카드 신청 사이트 버튼 -->
            <a
              v-if="product.card_apply_link"
              :href="product.card_apply_link"
              target="_blank"
              rel="noopener noreferrer"
              class="apply-button"
            >
              신청 사이트
            </a>

            <!-- 옵션 보기/접기 버튼 -->
            <button @click="toggleOptions(index)">
              {{ expandedIndexes.includes(index) ? '옵션 접기' : '옵션 보기' }}
            </button>

            <!-- 추가 옵션 -->
            <ul
              v-if="expandedIndexes.includes(index)"
              class="options-list"
            >
              <!-- 카드 전용 추가 옵션 -->
              <template v-if="selectedCategory === 'card'">
                <li>
                  <p>연회비: {{ product.annual_fee }}</p>
                  <p>기본 성능: {{ product.base_performance }}</p>
                  <p>이달의 혜택: {{ product.merit_summary }}</p>
                </li>
              </template>

              <!-- 예금/적금 옵션 -->
              <template v-else>
                <li
                  v-for="(option, idx) in product.options"
                  :key="idx"
                >
                  <p>저축금리유형: {{ option.intr_rate_type_nm }}</p>
                  <p>기본금리: {{ option.intr_rate }}%</p>
                  <p>최고우대금리: {{ option.intr_rate2 }}%</p>
                  <p>저축기간: {{ option.save_trm }}개월</p>
                </li>
              </template>
            </ul>
          </li>
        </ul>
      </div>
      <p v-else-if="!loading && !products.length">결과가 없습니다.</p>

      <!-- 여기부터 리스트 -->
       <!-- 카테고리별 리스트 결과 -->
       <div v-if="categoryItems.length">
        <h2>{{ selectedCategoryLabel }} 리스트</h2>
        <ul class="product-list">
          <li
            v-for="(item, index) in categoryItems"
            :key="index"
            class="product-item"
          >
            <h3>{{ item.fin_prdt_nm || item.card_name }}</h3>
            <p v-if="item.kor_co_nm || item.bank">은행: {{ item.kor_co_nm || item.bank }}</p>
          </li>
        </ul>
      </div>
      <p v-else-if="!loading && !categoryItems.length">카테고리 결과가 없습니다.</p>

      <!-- 메인으로 가기 버튼 -->
      <button @click="goToMain" class="main-button">메인으로 가기</button>
    </main>
  </div>


  
</template>

### Script

```vue
<script setup>
import axios from "axios";
import { ref, computed } from "vue";
import { useRouter } from "vue-router"; // 라우터 임포트

// 상태 관리
const query = ref(""); // 검색어
const products = ref([]); // 검색 결과
const categoryItems = ref([]); // 카테고리별 리스트 결과
const selectedCategory = ref(""); // 선택된 카테고리
const selectedCategoryLabel = ref(""); // 선택된 카테고리 이름
const loading = ref(false); // 로딩 상태

// 카테고리별 API URL
const apiUrls = {
  deposit: "http://127.0.0.1:8000/api/v1/deposits",
  saving: "http://127.0.0.1:8000/api/v1/savings",
  card: "http://127.0.0.1:8000/api/v1/search/cards",
};

// 검색 API URL
const searchApiUrls = {
  deposit: "http://127.0.0.1:8000/api/v1/deposits?search=",
  saving: "http://127.0.0.1:8000/api/v1/savings?search=",
  card: "http://127.0.0.1:8000/api/v1/search/cards?search=",
};

// 카테고리별 라벨
const categoryLabels = {
  deposit: "예금",
  saving: "적금",
  card: "카드",
};

// 선택된 카테고리의 라벨
const categoryLabel = computed(() => categoryLabels[selectedCategory.value] || "");

// 카테고리 리스트 가져오기
const fetchCategoryItems = async (category) => {
  selectedCategory.value = category;
  selectedCategoryLabel.value = categoryLabels[category]; // 카테고리 라벨 설정
  try {
    loading.value = true;
    const response = await axios.get(apiUrls[category]); // 카테고리 API 호출
    categoryItems.value = response.data; // 응답 데이터 저장
    products.value = []; // 검색 결과 초기화
  } catch (error) {
    console.error("Error fetching category items:", error);
    alert("카테고리 데이터를 가져오는 중 오류가 발생했습니다.");
  } finally {
    loading.value = false;
  }
};



// 메인으로 가기
const router = useRouter(); // 라우터 인스턴스 가져오기
const goToMain = () => {
  router.push({ path: "/" }); // 메인 페이지로 이동
};


// 카테고리 설정
const setCategory = (category) => {
  selectedCategory.value = category;
  query.value = ""; // 검색어 초기화
  products.value = []; // 검색 결과 초기화
  expandedIndexes.value = []; // 옵션 초기화
};

// API 호출 함수
const fetchProducts = async () => {
  if (!query.value.trim()) {
    alert("Please enter a search term.");
    return;
  }

  loading.value = true; // 로딩 시작
  try {
    // 선택된 카테고리에 따라 API 호출
    const response = await axios.get(`${apiUrls[selectedCategory.value]}${encodeURIComponent(query.value)}`);
    products.value = response.data; // 결과 저장
    expandedIndexes.value = []; // 검색 시 모든 옵션 초기화
  } catch (error) {
    console.error("Error fetching products:", error);
    alert("An error occurred while fetching the data.");
  } finally {
    loading.value = false; // 로딩 종료
  }
};

// 옵션 접기/펼치기 토글 함수
const toggleOptions = (index) => {
  if (expandedIndexes.value.includes(index)) {
    // 이미 열려 있으면 닫음
    expandedIndexes.value = expandedIndexes.value.filter((i) => i !== index);
  } else {
    // 닫혀 있으면 열음
    expandedIndexes.value.push(index);
  }
};
</script>

<style scoped>
.container {
  display: flex;
  max-width: 1200px;
  margin: 0 auto;
  padding: 20px;
}

.vertical-banner {
  width: 250px;
  margin-right: 20px;
  padding: 15px;
  background-color: #f8f9fa;
  border: 1px solid #dee2e6;
  border-radius: 5px;
}

.vertical-banner h2 {
  font-size: 18px;
  margin-bottom: 15px;
  color: #4c8a81;
}

.menu-list {
  list-style: none;
  padding: 0;
}

.menu-list li {
  padding: 10px;
  border-bottom: 1px solid #ddd;
  cursor: pointer;
  font-size: 16px;
}

.menu-list li:hover {
  background-color: #e9ecef;
}

.content {
  flex: 1;
  padding: 20px;
  background-color: white;
  border-radius: 5px;
  border: 1px solid #dee2e6;
}

.product-list {
  list-style: none;
  padding: 0;
}

.product-item {
  padding: 15px;
  margin-bottom: 10px;
  border: 1px solid #ddd;
  border-radius: 5px;
  background-color: #f9f9f9;
}

.pagination {
  display: flex;
  justify-content: center;
  align-items: center;
  gap: 10px;
}

.pagination-button {
  padding: 10px 15px;
  background-color: #4c8a81;
  color: white;
  border: none;
  border-radius: 5px;
  cursor: pointer;
}

.pagination-button:disabled {
  background-color: #ccc;
  cursor: not-allowed;
}

.customer-center p {
  font-size: 14px;
}

.content {
  float: right; /* 오른쪽으로 배치 */
  width: 920px; /* 고정 너비 */
  padding: 20px;
  background-color: white;
  border-radius: 5px;
  border: 1px solid #dee2e6;
}

/* 버튼 컨테이너 고정 */
.button-container {
  display: flex; /* Flexbox 활성화 */
  justify-content: space-between; /* 버튼 간 동일 간격 */
  gap: 10px; /* 버튼 사이 간격 */
  margin-bottom: 20px;
  width: 100%; /* 부모 컨테이너 너비를 가득 채움 */
}

.category-button {
  flex: 1; /* 버튼을 균등하게 확장 */
  height: 50px; /* 고정 높이 */
  margin: 0; /* 버튼 간 여백 제거 (gap으로 설정) */
  padding: 10px;
  border: none;
  background-color: #4c8a81; /* 버튼 배경색 */
  color: white; /* 글자색 */
  border-radius: 10px; /* 모서리를 둥글게 */
  font-size: 18px; /* 글자 크기 증가 */
  font-weight: bold; /* 글자 두께 */
  cursor: pointer;
  text-align: center;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1); /* 그림자 효과 */
  transition: all 0.3s ease; /* 부드러운 애니메이션 효과 */
}

.category-button:hover {
  background-color: #3e7066; /* 호버 시 색상 */
}

.category-button:active {
  transform: scale(0.98); /* 클릭 시 살짝 줄어듦 */
}

/* 검색 폼 고정 */
.search-form {
  display: block; /* flex 제거 */
  margin-bottom: 20px;
}

.search-label {
  display: inline-block;
  margin-right: 10px;
  font-size: 16px;
}

.search-input-container {
  display: inline-block;
  vertical-align: top;
}

.search-input {
  display: inline-block;
  padding: 10px;
  border: 1px solid #ced4da;
  border-radius: 5px 0 0 5px; /* 왼쪽 모서리 둥글게 */
  width: 300px; /* 고정 너비 */
}

.search-button {
  display: inline-block;
  padding: 10px 20px;
  background-color: #4c8a81; /* 버튼 배경색 */
  color: white; /* 텍스트 색상 */
  border: none;
  border-radius: 0 5px 5px 0; /* 오른쪽 모서리 둥글게 */
  cursor: pointer;
  font-size: 16px;
  font-weight: bold;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  vertical-align: top; /* 입력 필드와 맞춤 */
}

.search-button:hover {
  background-color: #3e7066; /* 호버 시 색상 */
}

.search-button:active {
  transform: scale(0.98);
}

/* 상품 리스트 고정 */
.product-list {
  list-style: none;
  padding: 0;
}

.product-item {
  padding: 15px;
  margin-bottom: 10px;
  border: 1px solid #ddd;
  border-radius: 5px;
  background-color: #f9f9f9;
  width: 100%; /* 고정 너비 */
}

.main-button {
  position: fixed; /* 고정 위치 */
  bottom: 20px;
  right: 20px;
  background-color: #007bff;
  color: white;
  padding: 10px 20px;
  border: none;
  border-radius: 5px;
  cursor: pointer;
}
</style>


<template>
  <div class="container">
    <!-- 왼쪽 세로 배너 -->
    <aside class="vertical-banner">
      <h2>{{categoryLabel}}상품 카테고리</h2>
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
        <h2>상품 검색</h2>
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
      <div v-if="paginatedProducts.length > 0">
        <h2>검색 결과</h2>
        <ul class="product-list">
          <li
            v-for="(product, index) in paginatedProducts"
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

            <!-- 옵션 보기/접기 버튼 -->
            <button @click="toggleOptions(index)">
              {{ expandedIndexes.includes(index) ? '옵션 접기' : '옵션 보기' }}
            </button>

            <!-- 추가 옵션 -->
            <ul v-if="expandedIndexes.includes(index)" class="options-list">
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

      <!-- 페이지네이션 -->
      <div class="pagination">
        <button
          class="pagination-button"
          :disabled="currentPage === 1"
          @click="changePage(currentPage - 1)"
        >
          이전
        </button>
        <button
          v-for="page in totalPages"
          :key="page"
          class="pagination-button"
          :class="{ active: currentPage === page }"
          @click="changePage(page)"
        >
          {{ page }}
        </button>
        <button
          class="pagination-button"
          :disabled="currentPage === totalPages"
          @click="changePage(currentPage + 1)"
        >
          다음
        </button>
      </div>

      </div>
      <p v-else-if="!loading && products.length === 0">검색 결과가 없습니다.</p>

      <!-- 카테고리별 리스트 -->
      <div v-if="paginatedCategoryItems.length > 0 && products.length === 0">
        <h2>{{ selectedCategoryLabel }} 리스트</h2>
        <ul class="product-list">
          <li
            v-for="(item, index) in paginatedCategoryItems"
            :key="index"
            class="product-item"
          >
            <h3>{{ item.fin_prdt_nm || item.card_name }}</h3>
            <p v-if="item.kor_co_nm || item.bank">
              은행: {{ item.kor_co_nm || item.bank }}
            </p>
          </li>
        </ul>
         <!-- 페이지네이션 -->
        <div class="pagination">
          <button
            class="pagination-button"
            :disabled="currentPage === 1"
            @click="changePage(currentPage - 1)"
          >
            이전
          </button>
          <button
            v-for="page in totalCategoryPages"
            :key="page"
            class="pagination-button"
            :class="{ active: currentPage === page }"
            @click="changePage(page)"
          >
            {{ page }}
          </button>
          <button
            class="pagination-button"
            :disabled="currentPage === totalCategoryPages"
            @click="changePage(currentPage + 1)"
          >
            다음
          </button>
        </div>

      </div>
      <p v-else-if="!loading && products.length === 0 && categoryItems.length === 0">
        카테고리 결과가 없습니다.
      </p>

      <!-- 메인으로 가기 버튼 -->
      <button @click="goToMain" class="main-button">메인으로 가기</button>
    </main>
  </div>
</template>


### Script

```vue
<script setup>
import axios from "axios";
import { ref, computed, onMounted } from "vue";
import { useRouter } from "vue-router"; // 라우터 임포트
import { useCounterStore } from "@/stores/counter";
const store = useCounterStore()

// 상태 관리
const categoryLabel = ref("")
const query = ref(""); // 검색어
const products = ref([]); // 검색 결과
const categoryItems = ref([]); // 카테고리별 리스트 결과

const selectedCategory = ref(""); // 선택된 카테고리
const selectedCategoryLabel = ref(""); // 선택된 카테고리 이름
const loading = ref(false); // 로딩 상태

// 페이지네이션 상태
const currentPage = ref(1); // 현재 페이지
const itemsPerPage = ref(4); // 페이지당 항목 수
const totalItems = computed(() => products.value.length); // 전체 항목 수
const totalPages = computed(() => Math.ceil(totalItems.value / itemsPerPage.value)); // 총 페이지 수

// 현재 페이지에 표시할 데이터
const paginatedProducts = computed(() => {
  const start = (currentPage.value - 1) * itemsPerPage.value;
  const end = start + itemsPerPage.value;
  return products.value.slice(start, end);
});
// 현재 페이지에 표시할 카테고리 데이터
const paginatedCategoryItems = computed(() => {
  const start = (currentPage.value - 1) * itemsPerPage.value;
  const end = start + itemsPerPage.value;
  return categoryItems.value.slice(start, end);
});
// 카테고리별 총 페이지 수
const totalCategoryPages = computed(() => {
  return Math.ceil(categoryItems.value.length / itemsPerPage.value);
});


// 카테고리별 API URL
const apiUrls = {
  deposit: `${store.API_URL}/api/v1/deposits/`,
  saving: `${store.API_URL}/api/v1/savings/`,
  card: `${store.API_URL}/api/v1/search/cards/`,
};

// 검색 API URL
const searchApiUrls = {
  deposit: `${store.API_URL}/api/v1/deposits?search=`,
  saving: `${store.API_URL}/api/v1/savings?search=`,
  card: `${store.API_URL}/api/v1/search/cards?search=`,
};

// 카테고리별 라벨
const categoryLabels = {
  deposit: "예금",
  saving: "적금",
  card: "카드",
};

// ***************리스트
// 선택된 카테고리의 라벨
// 카테고리별 리스트 가져오기
// 카테고리별 리스트 가져오기
const fetchCategoryItems = async (category) => {
  if (!category) return; // 카테고리가 없으면 종료

  selectedCategory.value = category;
  selectedCategoryLabel.value = categoryLabels[category];
  currentPage.value = 1; // 페이지 초기화
  try {
    loading.value = true;
    const response = await axios.get(apiUrls[category]);
    categoryItems.value = response.data || []; // null 방지
    products.value = [];
  } catch (error) {
    console.error("Error fetching category items:", error);
    alert("카테고리 데이터를 가져오는 중 오류가 발생했습니다.");
    categoryItems.value = []; // 실패 시 빈 배열로 초기화
  } finally {
    loading.value = false;
  }
};
// *****************리스트


// 메인으로 가기
const router = useRouter(); // 라우터 인스턴스 가져오기
const goToMain = () => {
  router.push({ path: "/" }); // 메인 페이지로 이동
};
const expandedIndexes = ref([])
const categorynum = ref(0)
// 카테고리 설정
const setCategory = (category) => {
  selectedCategory.value = category;
  query.value = ""; // 검색어 초기화
  products.value = []; // 검색 결과 초기화
  if (selectedCategory.value == 'deposit') {
    categorynum.value = 0
   } else if (selectedCategory.value == 'saving') {
    categorynum.value = 1}
    else if (selectedCategory.value == 'card') {
      categorynum.value = 2
    }
  expandedIndexes.value = []; // 옵션 초기화
  console.log("Selected Category:", selectedCategory.value); // 디버그용
};

// API 호출 함수
const fetchProducts = async () => {
  if (!query.value.trim()) {
    alert("Please enter a search term.");
    return;
  }

  categoryItems.value = []; // 카테고리 리스트 초기화
  products.value = []; // 검색 결과 초기화
  expandedIndexes.value = []; // 옵션 초기화

  loading.value = true; // 로딩 시작
  try {
    // 선택된 카테고리에 따라 API 호출
    const response = await axios.get(
      `${searchApiUrls[selectedCategory.value]}${encodeURIComponent(query.value)}`
    );

    products.value = response.data; // 검색 결과 저장
  } catch (error) {
    console.error("Error fetching products:", error);
    alert("검색 중 오류가 발생했습니다.");
  } finally {
    loading.value = false; // 로딩 상태 비활성화
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

// 페이지 변경 함수
const changePage = (page) => {
  if (page < 1 || page > totalPages.value) return; // 검색 결과 페이지
  if (page < 1 || page > totalCategoryPages.value) return; // 카테고리 결과 페이지
  currentPage.value = page;
};

// 컴포넌트가 로드되면 자동으로 "예금" 데이터를 가져옵니다.
onMounted(() => {
  selectedCategory.value = "deposit"; // 기본 카테고리 설정
  fetchCategoryItems("deposit"); // "예금" 데이터를 기본으로 가져옴
});
  
</script>

<style scoped>

.pagination {
  display: flex;
  justify-content: center;
  align-items: center;
  gap: 5px; /* 버튼 간격 조정 */
  margin-top: 20px; /* 페이지네이션과 리스트 간 간격 */
  flex-wrap: wrap; /* 버튼이 줄어들 때 자동으로 줄 바꿈 */
}

.pagination-button {
  padding: 10px 15px;
  background-color: #4c8a81;
  color: white;
  border: none;
  border-radius: 5px;
  cursor: pointer;
  font-size: 14px;
  white-space: nowrap; /* 버튼 안 텍스트가 줄 바꿈되지 않도록 설정 */
}

.pagination-button:disabled {
  background-color: #ccc;
  cursor: not-allowed;
}

.pagination-button.active {
  background-color: #007bff;
  font-weight: bold;
}

.container {
  display: flex;
  max-width: 1200px;
  height: 95vh; /* 화면 전체 높이 */
  margin: 0 auto;
  /* padding: 20px; */
  box-sizing: border-box; /* 패딩 포함 크기 계산 */
  overflow: hidden; /* 컨텐츠가 부모 영역을 초과하지 않도록 설정 */
}

.vertical-banner {
  width: 250px;
  margin-right: 20px;
  padding: 15px;
  background-color: #f8f9fa;
  border: 1px solid #dee2e6;
  border-radius: 5px;
  flex-shrink: 0; /* 크기가 줄어들지 않도록 고정 */
  height: 100%; /* 부모 컨테이너의 전체 높이 채움 */
  box-sizing: border-box; /* 패딩 포함 크기 계산 */
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
  height: 100%; /* 부모 컨테이너의 전체 높이 채움 */
  box-sizing: border-box; /* 패딩 포함 크기 계산 */
  overflow-y: auto; 
  /* 내용이 초과하면 스크롤 */
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
  background-color: rgba(211, 211, 211, 0.8); /* 흐릿하고 투명한 연한 회색 */
  color: #4c4c4c; /* 진한 회색 글씨 */
  padding: 15px 25px; /* 버튼 크기를 키움 */
  border: none;
  border-radius: 10px; /* 더 둥글게 */
  font-size: 18px; /* 글씨 크기 키움 */
  font-weight: bold; /* 글씨 두껍게 */
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.2); /* 부드러운 그림자 */
  cursor: pointer;
  transition: all 0.3s ease; /* 부드러운 애니메이션 */
}

.main-button:hover {
  background-color: rgba(200, 200, 200, 0.9); /* 호버 시 약간 더 진해짐 */
  color: #333; /* 글씨 색 조금 더 진하게 */
  transform: scale(1.05); /* 살짝 커짐 */
}
</style>


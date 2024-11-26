<template>


  
  <div>
    <h1>상품 검색</h1>

    <!-- 카테고리 선택 버튼 -->
    <div>
      <button @click="setCategory('deposit')">예금</button>
      <button @click="setCategory('saving')">적금</button>
      <button @click="setCategory('card')">카드</button>
    </div>

    <!-- 검색 입력창 -->
    <div v-if="selectedCategory">
      <h2>{{ categoryLabel }} 상품 검색</h2>
      <form @submit.prevent="fetchProducts">
        <label for="search">Search:</label>
        <input
          type="text"
          id="search"
          v-model="query"
          placeholder="Enter product name"
        />
        <button type="submit">Search</button>
      </form>
    </div>

    <!-- 로딩 상태 -->
    <div v-if="loading">Loading...</div>

    <!-- 검색 결과 -->
    <h1 v-if="products.length">검색 결과</h1>
    <ul v-if="products.length">
      <li v-for="(product, index) in products" :key="index">
        <!-- 상품 기본 정보 -->
        <h3>{{ product.fin_prdt_nm || product.card_name }}</h3>
        <p v-if="product.kor_co_nm">Bank: {{ product.kor_co_nm }}</p>
        <p v-if="product.bank">Bank: {{ product.bank }}</p>
        <p>상세정보:</p>
        <p class="description">{{ product.etc_note || product.merit_summary }}</p>
        <p v-if="product.max_limit">최고 가입한도: {{ product.max_limit }}</p>

        <!-- 옵션 보기 (예금/적금 전용) -->
        <button v-if="selectedCategory !== 'card'" @click="toggleOptions(index)">
          {{ expandedIndexes.includes(index) ? '옵션 접기' : '옵션 보기' }}
        </button>

        <!-- 상품 옵션 반복 -->
        <ul v-if="selectedCategory !== 'card' && expandedIndexes.includes(index)">
          <li v-for="(option, idx) in product.options" :key="idx">
            <p>저축금리유형: {{ option.intr_rate_type_nm }}</p>
            <p>기본금리: {{ option.intr_rate }}%</p>
            <p>최고우대금리: {{ option.intr_rate2 }}%</p>
            <p>저축기간: {{ option.save_trm }}개월</p>
          </li>
        </ul>
      </li>
    </ul>
    <p v-else-if="!loading && !products.length">No results found.</p>
  </div>
  <!-- 메인으로 가기 버튼 -->
  <button @click="goToMain" class="main-button">메인으로 가기</button>
</template>

---

### Script

```vue
<script setup>
import axios from "axios";
import { ref, computed } from "vue";

import { useRouter } from "vue-router"; // 라우터 임포트

const router = useRouter(); // 라우터 인스턴스 가져오기

const goToMain = () => {
  router.push({ path: "/" }); // 메인 페이지로 이동
};


// 상태 관리
const query = ref(""); // 검색어
const products = ref([]); // 검색 결과
const loading = ref(false); // 로딩 상태
const expandedIndexes = ref([]); // 옵션 표시 상태를 관리하는 배열
const selectedCategory = ref(""); // 선택된 카테고리

// 카테고리별 API URL
const apiUrls = {
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
/* 검색 폼 스타일 */
form {
  margin-bottom: 20px;
}

input {
  padding: 8px;
  margin-right: 10px;
  border: 1px solid #ccc;
  border-radius: 4px;
}

button {
  padding: 8px 16px;
  border: none;
  background-color: #007bff;
  color: white;
  border-radius: 4px;
  cursor: pointer;
}

button:hover {
  background-color: #0056b3;
}

/* 검색 결과 스타일 */
ul {
  list-style: none;
  padding: 0;
}

li {
  border: 1px solid #ddd;
  padding: 15px;
  margin-bottom: 10px;
  border-radius: 4px;
}

.description {
  white-space: pre-line;
}
.main-button {
  margin-bottom: 20px;
  padding: 10px 20px;
  background-color: #d3d3d3; /* 연회색 */
  color: #333; /* 버튼 글자색 */
  border: none;
  border-radius: 4px;
  cursor: pointer;
}

.main-button:hover {
  background-color: #b0b0b0; /* 조금 더 어두운 연회색 */
}
</style>

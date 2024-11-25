<template>
  <div class="container">
    <!-- 페이지 헤더 -->
    <header class="page-header">
      <h1>Deposit Saving Card Search</h1>
      <div class="snowman-icon" @click="promptSignUp">☃</div>
    </header>

    <!-- 카테고리 박스 -->
    <div class="category-container">
      <div class="category-box" @click="setCategory('deposit')">
        <h2>예금</h2>
      </div>
      <div class="category-box" @click="setCategory('saving')">
        <h2>적금</h2>
      </div>
      <div class="category-box" @click="setCategory('card')">
        <h2>카드</h2>
      </div>
    </div>

    <!-- 검색 섹션 -->
    <div v-if="selectedCategory" class="search-section">
      <h2>{{ categoryLabel }} 상품 검색</h2>
      <form @submit.prevent="fetchProducts" class="search-form">
        <input
          type="text"
          v-model="query"
          placeholder="상품 이름을 입력하세요"
          class="rounded-input"
        />
        <button type="submit" class="custom-button">검색</button>
      </form>
    </div>

    <!-- 출력 공간 -->
    <div class="output-space">
      <!-- 검색 결과가 없을 때 -->
      <div v-if="products.length === 0" class="empty-content">
        <p>결과가 없습니다. 추천 상품을 확인해보세요!</p>
        <div class="recommended-products">
          <h4>추천 상품</h4>
          <ul>
            <li
              v-for="(product, index) in randomProducts"
              :key="index"
              class="product-item"
            >
              <h3>{{ product.fin_prdt_nm || product.card_name }}</h3>
              <p v-if="product.kor_co_nm">Bank: {{ product.kor_co_nm }}</p>
              <p v-if="product.bank">Bank: {{ product.bank }}</p>
              <p>{{ product.etc_note || product.merit_summary }}</p>
            </li>
          </ul>
        </div>
      </div>

      <!-- 검색 결과가 있을 때 -->
      <ul v-else>
        <li v-for="(product, index) in products" :key="index" class="product-item">
          <button class="product-button" @click="viewProduct(product)">
            <h3>{{ product.fin_prdt_nm || product.card_name }}</h3>
            <p v-if="product.kor_co_nm">Bank: {{ product.kor_co_nm }}</p>
            <p v-if="product.bank">Bank: {{ product.bank }}</p>
            <p class="description">{{ product.etc_note || product.merit_summary }}</p>
            <p v-if="product.max_limit">최고 가입한도: {{ product.max_limit }}</p>
          </button>
        </li>
      </ul>
    </div>

    <!-- 카드 모달 -->
    <div v-if="isProductModalOpen" class="modal-overlay" @click="closeProductModal">
      <div class="modal-content" @click.stop>
        <button class="close-modal" @click="closeProductModal">X</button>
        <h3>{{ selectedProduct?.card_name }}</h3>
        <p v-if="selectedProduct?.bank">Bank: {{ selectedProduct.bank }}</p>
        <p>{{ selectedProduct?.merit_summary }}</p>
        <p v-if="selectedProduct?.max_limit">최고 가입한도: {{ selectedProduct.max_limit }}</p>
        <a
          v-if="selectedProduct?.link"
          :href="selectedProduct.link"
          target="_blank"
          class="modal-link"
        >
          상품 상세 보기
        </a>
      </div>
    </div>
  </div>
</template>

<script setup>
import axios from "axios";
import { ref, computed } from "vue";

const query = ref("");
const products = ref([]);
const selectedCategory = ref("");
const isProductModalOpen = ref(false);
const selectedProduct = ref(null);

const apiUrls = {
  deposit: "http://127.0.0.1:8000/api/v1/deposits?search=",
  saving: "http://127.0.0.1:8000/api/v1/savings?search=",
  card: "http://127.0.0.1:8000/api/v1/search/cards?search=",
};

const setCategory = (category) => {
  selectedCategory.value = category;
  query.value = "";
  products.value = [];
};

const fetchProducts = async () => {
  if (!query.value.trim()) {
    alert("Please enter a search term.");
    return;
  }
  const response = await axios.get(
    `${apiUrls[selectedCategory.value]}${encodeURIComponent(query.value)}`
  );
  products.value = response.data;
};

const viewProduct = (product) => {
  selectedProduct.value = product;
  isProductModalOpen.value = true;
};

const closeProductModal = () => {
  isProductModalOpen.value = false;
  selectedProduct.value = null;
};

const promptSignUp = () => {
  alert("회원가입을 해보세요!");
};

const dummyProducts = [
  { fin_prdt_nm: "우리은행 정기예금", kor_co_nm: "우리은행", etc_note: "최대 금리 3.5%" },
  { fin_prdt_nm: "국민은행 장기적금", kor_co_nm: "국민은행", etc_note: "최대 금리 4.0%" },
  { fin_prdt_nm: "삼성카드 Platinum", bank: "삼성카드", merit_summary: "여행 혜택 제공" },
  { fin_prdt_nm: "신한은행 청년저축", kor_co_nm: "신한은행", etc_note: "최대 금리 4.2%" },
  { fin_prdt_nm: "농협 적금 상품", kor_co_nm: "농협", etc_note: "최대 금리 3.8%" },
];

const randomProducts = computed(() => {
  const shuffled = [...dummyProducts].sort(() => 0.5 - Math.random());
  return shuffled.slice(0, 3);
});

const categoryLabels = {
  deposit: "예금",
  saving: "적금",
  card: "카드",
};

const categoryLabel = computed(() => categoryLabels[selectedCategory.value] || "");
</script>

<style scoped>
.container {
  padding: 20px 40px;
  font-family: Arial, sans-serif;
  max-width: 1200px;
  margin: 0 auto;
}


/* 페이지 헤더 */
.page-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  background-color: #f0f8ff;
  padding: 10px;
  border-radius: 10px;
  margin-bottom: 20px;
}

/* 눈사람 아이콘 */
.snowman-icon {
  font-size: 30px;
  cursor: pointer;
}

/* 카테고리 박스 */
.category-container {
  display: flex;
  justify-content: space-between;
  gap: 10px;
}

.category-box {
  flex: 1;
  height: 150px;
  border: 1px solid #ccc;
  background-color: #f9f9f9;
  border-radius: 10px;
  display: flex;
  justify-content: center;
  align-items: center;
  cursor: pointer;
  transition: all 0.3s ease;
}

.category-box:hover {
  background-color: #e0f7ff;
}

.search-section {
  margin-top: 20px;
}

/* 검색 섹션 */
.rounded-input {
  width: 70%;
  padding: 8px;
  border: 1px solid #ccc;
  border-radius: 10px;
  margin-right: 10px;
}

.custom-button {
  padding: 8px 16px;
  background-color: #007bff;
  color: white;
  border: none;
  border-radius: 10px;
  cursor: pointer;
}

.output-space {
  margin-top: 20px;
  border: 1px dashed #ccc;
  padding: 20px;
  border-radius: 10px;
  min-height: 200px; /* 항상 일정한 높이 유지 */
  background-color: #f9f9f9;
}

/* 랜덤 추천 상품 */
.recommended-products {
  margin-top: 20px;
}

.recommended-products h4 {
  font-size: 18px;
  margin-bottom: 10px;
}

.recommended-products ul {
  list-style: none;
  padding: 0;
}

.recommended-products li {
  border: 1px solid #ddd;
  padding: 10px;
  margin-bottom: 10px;
  background-color: #fff;
}

/* 모달 */
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(0, 0, 0, 0.5);
  display: flex;
  justify-content: center;
  align-items: center;
}

.modal-content {
  background-color: white;
  border-radius: 10px;
  padding: 20px;
  max-width: 500px;
  text-align: center;
}

.modal-link {
  display: block;
  margin-top: 10px;
  color: #007bff;
  text-decoration: underline;
}
</style>

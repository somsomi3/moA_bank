<template>
  <div class="container">
    <!-- 왼쪽 세로 배너 -->
    <aside class="vertical-banner">
      <h2>신탁/ISA</h2>
      <ul class="menu-list">
        <li>특정금전신탁(MMT/CMT) <span>+</span></li>
        <li>연금저축신탁 해지/예상조회 <span>+</span></li>
        <li>연금저축신탁 연금개시 신청/조회 <span>+</span></li>
        <li>ISA 소개/가입 <span>+</span></li>
        <li>ISA 입금/지급/해지 <span>+</span></li>
        <li>나의 ISA 조회/변경 <span>+</span></li>
        <li>ISA 공지 · 공지 <span>+</span></li>
        <li>스튜어드십 코드 <span>+</span></li>
      </ul>
      <div class="customer-center">
        <h3>고객센터</h3>
        <p>1588-1111</p>
        <p>1599-1111</p>
      </div>
    </aside>

    <!-- 본문 컨텐츠 -->
    <main class="content">
      <h1>상품 검색</h1>

      <!-- 카테고리 선택 버튼 -->
      <div class="button-container">
        <button class="category-button" @click="setCategory('deposit')">예금</button>
        <button class="category-button" @click="setCategory('saving')">적금</button>
        <button class="category-button" @click="setCategory('card')">카드</button>
      </div>

      <!-- 검색 입력창 -->
      <div v-if="selectedCategory" class="search-container">
        <h2>{{ categoryLabel }} 상품 검색</h2>
        <form @submit.prevent="fetchProducts">
          <input
            type="text"
            v-model="query"
            placeholder="상품명을 입력하세요"
            class="search-input"
          />
          <button type="submit" class="search-button">검색</button>
        </form>
      </div>

      <!-- 검색 결과 -->
      <ul v-if="products.length" class="product-list">
        <li v-for="(product, index) in products" :key="index" class="product-item">
          <h3>{{ product.fin_prdt_nm || product.card_name }}</h3>
          <p v-if="product.kor_co_nm">Bank: {{ product.kor_co_nm }}</p>
          <p>{{ product.etc_note || product.merit_summary }}</p>
        </li>
      </ul>

      <!-- 랜덤 상품 영역 -->
      <section class="random-products">
        <h2>추천 상품</h2>
        <div class="random-grid">
          <div
            v-for="(item, index) in randomItems"
            :key="index"
            class="random-item"
          >
            <img :src="item.image" alt="product image" />
            <p>{{ item.name }}</p>
          </div>
        </div>
      </section>
    </main>
  </div>
</template>

<script>
import axios from "axios";
import { ref, computed, onMounted } from "vue";

export default {
  name: "ProductSearch",
  setup() {
    const query = ref("");
    const products = ref([]);
    const selectedCategory = ref("");

    const apiUrls = {
      deposit: "http://127.0.0.1:8000/api/v1/deposits?search=",
      saving: "http://127.0.0.1:8000/api/v1/savings?search=",
      card: "http://127.0.0.1:8000/api/v1/search/cards?search=",
    };

    const categoryLabels = {
      deposit: "예금",
      saving: "적금",
      card: "카드",
    };

    const categoryLabel = computed(() => categoryLabels[selectedCategory.value] || "");

    const setCategory = (category) => {
      selectedCategory.value = category;
      query.value = "";
      products.value = [];
    };

    const fetchProducts = async () => {
      if (!query.value.trim()) {
        alert("검색어를 입력하세요.");
        return;
      }

      try {
        const response = await axios.get(`${apiUrls[selectedCategory.value]}${encodeURIComponent(query.value)}`);
        products.value = response.data;
      } catch (error) {
        console.error("데이터 가져오기 실패:", error);
      }
    };

    // 랜덤 상품 데이터
    const randomItems = ref([]);

    const fetchRandomItems = async () => {
      const items = [
        { name: "예금 상품 A", image: "https://via.placeholder.com/150" },
        { name: "적금 상품 B", image: "https://via.placeholder.com/150" },
        { name: "카드 상품 C", image: "https://via.placeholder.com/150" },
        { name: "카드 상품 D", image: "https://via.placeholder.com/150" },
      ];
      randomItems.value = items.sort(() => Math.random() - 0.5); // 랜덤 정렬
    };

    onMounted(fetchRandomItems);

    return {
      query,
      products,
      selectedCategory,
      setCategory,
      fetchProducts,
      categoryLabel,
      randomItems,
    };
  },
};
</script>


<style scoped>
/* 전체 레이아웃 */
/* 전체 레이아웃 */
.container {
  display: flex;
  font-family: Arial, sans-serif;
  max-width: 1200px;
  margin: 0 auto;
  padding: 20px;
}

/* 세로 배너 스타일 */
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
  margin-bottom: 20px;
  color: #007bff;
}

.menu-list {
  list-style: none;
  padding: 0;
  margin: 0;
}

.menu-list li {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 10px 0;
  border-bottom: 1px solid #ddd;
  font-size: 14px;
  cursor: pointer;
}

.menu-list li:last-child {
  border-bottom: none;
}

.menu-list span {
  color: #6c757d;
  font-weight: bold;
}

.customer-center {
  margin-top: 20px;
  text-align: center;
}

.customer-center h3 {
  margin-bottom: 10px;
  font-size: 16px;
  color: #007bff;
}

.customer-center p {
  margin: 0;
  font-size: 14px;
  color: #333;
}

/* 본문 스타일 */
.content {
  flex: 1;
  background-color: white;
  padding: 20px;
  border-radius: 5px;
  border: 1px solid #dee2e6;
}

/* 버튼 컨테이너 */
.button-container {
  display: flex;
  justify-content: space-between;
  margin-bottom: 20px;
}

.category-button {
  flex: 1;
  margin: 0 10px;
  padding: 15px;
  font-size: 16px;
  background-color: #f1f3f5;
  border: 1px solid #ced4da;
  border-radius: 5px;
  cursor: pointer;
  text-align: center;
}

.category-button:hover {
  background-color: #e9ecef;
}

/* 검색 입력 */
.search-container {
  margin-bottom: 20px;
}

.search-input {
  width: calc(100% - 120px);
  padding: 10px;
  margin-right: 10px;
  font-size: 14px;
  border: 1px solid #ced4da;
  border-radius: 5px;
}

.search-button {
  padding: 10px 20px;
  background-color: #007bff;
  color: white;
  border: none;
  border-radius: 5px;
  cursor: pointer;
}

.search-button:hover {
  background-color: #0056b3;
}

/* 상품 리스트 */
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

/* 랜덤 상품 스타일 */
.random-products {
  margin-top: 30px;
}

.random-products h2 {
  font-size: 18px;
  margin-bottom: 10px;
}

.random-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 15px;
}

.random-item {
  text-align: center;
  background-color: #f8f9fa;
  padding: 10px;
  border: 1px solid #dee2e6;
  border-radius: 5px;
}

.random-item img{
margin-top: 5px;
  font-size: 14px;
  color: #333;
}
</style>

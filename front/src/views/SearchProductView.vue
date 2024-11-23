<template>
  <div>
    <h1>Search Product</h1>
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

    <!-- 로딩 상태 -->
    <div v-if="loading">Loading...</div>

    <!-- 검색 결과 -->
    <ul v-if="products.length">
      <li v-for="product in products" :key="product.id">
        <h3>{{ product.name }}</h3>
        <p>Bank: {{ product.bank }}</p>
        <p>Interest Rate: {{ product.interest_rate }}%</p>
        <p>{{ product.description }}</p>
      </li>
    </ul>
    <p v-else-if="!loading && !products.length">No results found.</p>
  </div>
</template>

<script setup>
import axios from 'axios';
import { ref } from 'vue';
import SearchProductView from '../views/SearchProductView.vue'; // 검색 컴포넌트

// 입력값과 상태 관리
const query = ref(''); // 검색어
const products = ref([]); // 검색 결과
const loading = ref(false); // 로딩 상태

// API URL
const API_URL = 'http://127.0.0.1:8000/api/v1/search/saving?search=';

// API 호출 함수
const fetchProducts = async () => {
  if (!query.value.trim()) {
    alert('Please enter a search term.');
    return;
  }

  loading.value = true; // 로딩 시작
  try {
    // 검색어를 URL에 추가하여 API 요청
    const response = await axios.get(`${API_URL}${encodeURIComponent(query.value)}`);
    products.value = response.data; // 결과 저장
  } catch (error) {
    console.error('Error fetching products:', error);
    alert('An error occurred while fetching the data.');
  } finally {
    loading.value = false; // 로딩 종료
  }
};
</script>

<style scoped>
/* 스타일 정의 */
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
</style>

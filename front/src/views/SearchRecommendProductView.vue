<!-- <template>
  <div>
    <h1>추천 상품 조회</h1>
    <input v-model="desiredAmount" placeholder="희망 금액" type="number" />
    <input v-model="desiredPeriod" placeholder="희망 기간 (개월)" type="number" />
    <button @click="fetchRecommendedProducts">조회</button>
    <div v-if="loading">로딩 중...</div>
    <ul v-if="products.length">
      <li v-for="product in products" :key="product.id">
        <h3>{{ product.product_name }}</h3>
        <p>금리: {{ product.interest_rate }}%</p>
        <p>기간: {{ product.save_term }}개월</p>
      </li>
    </ul>
  </div>
</template>

<script>
import axios from "axios";
export default {
  data() {
    return {
      desiredAmount: "",
      desiredPeriod: "",
      products: [],
      loading: false,
    };
  },
  methods: {
    async fetchRecommendedProducts() {
      this.loading = true;
      try {
        const response = await axios.get("http://127.0.0.1:8000/api/v1/get_recommended_products/", {
          params: {
            desired_amount_deposit: this.desiredAmount,
            desired_period_deposit: this.desiredPeriod,
          },
        });
        this.products = response.data;
      } catch (error) {
        console.error("API 요청 오류:", error);
      } finally {
        this.loading = false;
      }
    },
  },
};
</script> -->

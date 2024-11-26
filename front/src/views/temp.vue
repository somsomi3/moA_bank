<template>
  <div class="homepage">
    <!-- 헤더 -->
    <header class="header">
      <nav class="navbar navbar-expand-lg navbar-light bg-light shadow">
        <div class="container-md">
          <RouterLink class="navbar-brand fw-bold fs-3 text-primary" to="/">moA</RouterLink>
          <button
            class="navbar-toggler"
            type="button"
            data-bs-toggle="collapse"
            data-bs-target="#navbarNav"
            aria-controls="navbarNav"
            aria-expanded="false"
            aria-label="Toggle navigation"
          >
            <span class="navbar-toggler-icon"></span>
          </button>
          <div class="collapse navbar-collapse" id="navbarNav">
            <ul class="navbar-nav ms-auto">
              <li class="nav-item">
                <RouterLink class="nav-link" :to="{ name: 'SearchProductView' }">상품 검색</RouterLink>
              </li>
              <li class="nav-item">
                <RouterLink class="nav-link" :to="{ name: 'MakeCardView' }">카드 만들기</RouterLink>
              </li>
              <li class="nav-item">
                <RouterLink class="nav-link" :to="{ name: 'MyPageView' }">마이페이지</RouterLink>
              </li>
              <li class="nav-item">
                <RouterLink class="nav-link" :to="{ name: 'LogInView' }">로그인</RouterLink>
              </li>
              <li class="nav-item">
                <RouterLink class="nav-link" :to="{ name: 'SignUpView' }">회원가입</RouterLink>
              </li>
            </ul>
          </div>
        </div>
      </nav>
    </header>

    <!-- 메인 배너 -->
    <div class="main-banner py-3 bg-light">
      <div class="container-md d-flex align-items-center flex-column-reverse flex-lg-row text-center text-lg-start">
        <div class="banner-text">
          <h1 class="fs-3 fw-bold text-primary">당신의 경제 생활 매니저, moA</h1>
          <p class="fs-6 text-secondary">경제적인 삶을 위한 맞춤형 금융 솔루션</p>
          <button class="btn btn-primary btn-sm mt-3" @click="navigate('start')">지금 시작하기</button>
        </div>
        <div class="banner-image">
          <img src="/mainPageIcon.svg" alt="아이콘" class="img-fluid" style="max-width: 300px;" />
        </div>
      </div>
    </div>

    <!-- 주요 기능 -->
    <div class="features py-3 bg-white">
      <div class="container-md">
        <h2 class="text-center mb-4 fw-bold fs-4"></h2>
        <div class="row gy-3">
          <div class="col-md-4" v-for="feature in features" :key="feature.id">
            <div class="card shadow-sm text-center">
              <div class="card-body">
                <img :src="feature.icon" alt="icon" class="feature-icon mb-2" style="max-width: 48px;" />
                <h5 class="card-title fw-bold fs-5">{{ feature.title }}</h5>
                <p class="card-text text-muted fs-6">{{ feature.description }}</p>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- 푸터 -->
    <footer class="footer bg-light py-2 mt-auto">
      <div class="container text-center">
        <p class="text-muted mb-0">&copy; 2024 moA. 모든 권리 보유.</p>
      </div>
    </footer>
  </div>
</template>

<script setup>
import { useRouter } from 'vue-router';
const router = useRouter();

const navigate = (page) => {
  if (page === 'start') router.push({ name: 'HelloView' });
};

// 주요 기능 데이터
const features = [
  {
    id: 1,
    icon: '/searchIcon.png',
    title: '금융 상품 검색',
    description: '예적금, 카드 등 맞춤형 금융 상품을 추천받아 보세요.',
  },
  {
    id: 2,
    icon: '/cardIcon.png',
    title: '카드 제작',
    description: '사용자에 맞는 카드를 만들어보세요.',
  },
  {
    id: 3,
    icon: '/analysisIcon.png',
    title: '경제 분석',
    description: '소득과 소비 패턴을 분석하여 효율적인 경제생활을 지원합니다.',
  },
];
</script>

<style scoped>

/* 공통 컨테이너 */
.container,
.homepage {
  max-width: 1200px;
  margin: 0 auto;
  padding: 20px;
  background-color: #f8f9fa;
  border-radius: 12px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
}

/* 헤더 스타일 */
.header {
  background-color: #ffffff;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.navbar {
  padding: 15px;
}

.navbar-brand {
  font-size: 28px;
  font-weight: bold;
  color: #007bff;
}

.nav-item .nav-link {
  font-size: 16px;
  color: #4c4c4c;
  transition: color 0.3s;
}

.nav-item .nav-link:hover {
  color: #007bff;
}

/* 메인 배너 */
.main-banner {
  background-color: #f8f9fa;
  padding: 40px 20px;
  margin: 20px auto;
  display: flex;
  flex-wrap: wrap;
  align-items: center;
  justify-content: space-between;
  text-align: center;
  border-radius: 12px;
}

.banner-text h1 {
  font-size: 32px;
  font-weight: bold;
  color: #333;
}

.banner-text p {
  font-size: 18px;
  color: #666;
}

.banner-image img {
  max-width: 300px;
  border-radius: 8px;
}

/* 주요 기능 */
.features {
  margin-top: 20px;
  display: flex;
  flex-wrap: wrap;
  gap: 20px;
  justify-content: center;
}

.feature-icon {
  max-width: 48px;
  margin-bottom: 10px;
}

.card {
  padding: 20px;
  border-radius: 8px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  transition: transform 0.2s ease;
}

.card:hover {
  transform: translateY(-3px);
  box-shadow: 0 6px 12px rgba(0, 0, 0, 0.15);
}

/* 검색 페이지 스타일 */
.vertical-banner {
  width: 250px;
  margin-right: 20px;
  padding: 15px;
  background-color: #ffffff;
  border-radius: 8px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
}

.menu-list li {
  padding: 10px;
  cursor: pointer;
  border-bottom: 1px solid #ddd;
}

.menu-list li:hover {
  background-color: #e9ecef;
}

.product-list,
.product-item {
  list-style: none;
  padding: 0;
}

.product-item {
  padding: 15px;
  margin-bottom: 10px;
  border-radius: 8px;
  background-color: #ffffff;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
}

/* 버튼 스타일 */
.btn,
.category-button {
  padding: 10px 20px;
  background-color: #007bff;
  color: white;
  font-size: 16px;
  font-weight: bold;
  border: none;
  border-radius: 8px;
  cursor: pointer;
  transition: all 0.3s ease;
}

.btn:hover,
.category-button:hover {
  background-color: #0056b3;
}

.btn:active,
.category-button:active {
  transform: scale(0.95);
}

.pagination {
  display: flex;
  justify-content: center;
  gap: 10px;
}

.pagination-button {
  background-color: #4c8a81;
  color: white;
  border: none;
  border-radius: 5px;
  padding: 10px 15px;
  cursor: pointer;
}

.pagination-button:hover {
  background-color: #3e7066;
}

/* 푸터 스타일 */
.footer {
  text-align: center;
  font-size: 14px;
  padding: 10px;
  background-color: #ffffff;
  margin-top: 20px;
  border-top: 1px solid #ddd;
}
</style>



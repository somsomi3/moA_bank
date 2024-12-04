<template>
  <div class="homepage">
    <!-- 헤더 -->
    <header class="header">
      <nav class="navbar navbar-expand-lg navbar-light bg-light shadow">
        <div class="container-md">
          <RouterLink class="navbar-brand fw-bold fs-3 logo-text" to="/">moA</RouterLink>
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
              <li class="nav-item dropdown">
                <button
                  class="btn btn-link nav-link dropdown-toggle"
                  id="communityDropdown"
                  data-bs-toggle="dropdown"
                  aria-expanded="false"
                >
                  커뮤니티
                </button>
                <ul class="dropdown-menu" aria-labelledby="communityDropdown">
                  <li v-for="community in communities" :key="community.id">
                    <RouterLink
                      class="dropdown-item"
                      :to="{ name: community.id !== 4 ? 'DetailView' : 'ArticleView', params: { id: community.id } }"
                    >
                      {{ community.name }}
                    </RouterLink>
                  </li>
                </ul>
              </li>
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
              <li class="nav-item">
                <button v-if="store.isLogin" class="nav-link btn-link logout-btn" @click="logOut">
                  로그아웃
                </button>
              </li>
            </ul>
          </div>
        </div>
      </nav>
    </header>

      <!-- 메인 배너 -->
      <div class="main-banner py-5 bg-light">
      <div class="container-md d-flex align-items-center justify-content-between flex-column-reverse flex-lg-row text-center text-lg-start">
        <!-- 이미지 왼쪽 -->
        <div class="animation-container me-lg-4">
      <div class="animated-circle circle-1"></div>
      <div class="animated-circle circle-2"></div>
    </div>
    
      <!-- <div class="chart-container">
       <img src="/output.png" alt="금융 그래프" class="responsive-chart">
      </div> -->
    
          <!-- 텍스트 및 버튼 오른쪽 -->
        <div class="banner-text ms-lg-5">
          <h1 class="fs-2 fw-bold banner-heading">당신의 경제 생활 매니저, moA</h1>
          <p class="fs-6 text-secondary mt-2">경제적인 삶을 위한 맞춤형 금융 솔루션</p>
          <div class="button-container">
            <button class="btn2" @click="navigate('start')">리포터 시작하기</button>
            <button class="btn3" @click="navigate('start')">지금 우리지역은</button>
          </div>

        </div>
      </div>
    </div>
    <div class="tempdiv"></div>
    <div class="features py-5 bg-white">
      <div class="container-md">
        <h2 class="text-center mb-5 fw-bold fs-4"></h2>
        <div class="row gy-4">
          <div class="col-md-4" v-for="feature in features" :key="feature.id">
            <div class="card shadow-sm text-center p-4 feature-card">
              
              <h5 class="card-title fw-bold fs-5">{{ feature.title }}</h5>
              <p class="card-text text-muted fs-6 mt-2">{{ feature.description }}</p>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- 푸터 -->
    <footer class="footer bg-light py-4">
      <div class="container text-center">
        <p class="mb-0 text-muted">© 2024 moA. All rights reserved.</p>
        <p class="mb-0 fs-6">문의: support@moa.com</p>
      </div>
    </footer>
  </div>
</template>

<script setup>
import { ref } from "vue";
import { useRouter } from "vue-router";
import { useCounterStore } from "@/stores/counter";

const store = useCounterStore();
const logOut = () => {
  store.logOut();
};

const communities = ref([
  { id: 1, name: "1~4분위 커뮤니티" },
  { id: 2, name: "5~8분위 커뮤니티" },
  { id: 3, name: "9~10분위 커뮤니티" },
  { id: 4, name: "자유 게시판" },
]);

const router = useRouter();

const navigate = (page) => {
  if (page === "start") router.push({ name: "HelloView" });
};

// 주요 기능 데이터
const features = [
  {
    id: 1,
    title: "금융 상품 검색",
    description: "예적금, 카드 등 맞춤형 금융 상품을 추천받아 보세요.",
  },
  {
    id: 2,
    title: "카드 제작",
    description: "사용자에 맞는 카드를 만들어보세요.",
  },
  {
    id: 3,
    title: "경제 분석",
    description: "소득과 소비 패턴을 분석하여 효율적인 경제생활을 지원합니다.",
  },
];
</script>

<style scoped>
/* 공통 헤더 스타일 */


.header {
  background-color: #005bac;
  color: white;
}

/* 네비게이션 바 */
.navbar .nav-link {
  color: black;
  margin-right: 15px;
  transition: color 0.3s ease;
}

.navbar .nav-link:hover {
  color: #ffdd57;
}

/* 드롭다운 메뉴 */
.dropdown-menu {
  box-shadow: 0px 4px 12px rgba(0, 0, 0, 0.1);
  min-width: 200px;
}

.dropdown-item:hover {
  background-color: #f7faff;
  color: #005bac;
}

/* 메인 배너 스타일 */
.main-banner {
  text-align: center;
}

.banner-text {
  margin-bottom: 20px;
  padding: 12px 30px;
  margin-left: auto;
}

.banner-image img {
  max-width: 100%;
}

/* 주요 기능 카드 */
.card {
  border: none;
  transition: transform 0.3s ease;
}

.card:hover {
  transform: translateY(-5px);
}

.feature-icon {
  max-width: 60px;
}

/* 버튼 스타일 */
.btn2 {
  padding: 12px 30px;
  background-color: #4c8a81;
  color: white;
  border: none;
  border-radius: 5px;
  cursor: pointer;
  font-size: 16px;
  font-weight: bold;
}

.btn2:hover {
  background-color: #3b6d62;
}

/* 푸터 */
.footer {
  background-color: #f8f9fa;
  color: #6c757d;
}

/* 주요 기능 카드 */
.feature-card {
  height: 100%;
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  align-items: center;
  max-width: 100%;
  padding: 20px;
}

.feature-icon {
  max-width: 60px;
}

/* 카드 텍스트 */
.card-title {
  margin-top: 15px;
}

.card-text {
  margin-top: 10px;
  font-size: 14px;
  color: #6c757d;
}


/* 차트를 포함하는 컨테이너 스타일 */
.chart-container {
 width: 1000px;
 height:1000x;
}

/* 반응형 이미지를 위한 스타일 */
.responsive-chart {
  max-width: 100%; /* 부모 요소의 크기를 넘지 않도록 설정 */
  height: auto; /* 비율 유지 */
  display: block; /* 중복 여백 제거 */
}


/* 메인 배너 */
.main-banner {
  text-align: center;
}

.banner-image {
  flex: 1;
  display: flex;
  justify-content: center;
  align-items: center;
}

.banner-text {
  flex: 1;
  padding: 20px;
  text-align: left;
}

.chart-container {
  width: 400px;
  height: auto;
  max-width: 100%;
  margin-right: 20px; /* 이미지와 텍스트 간격 */
}

.responsive-chart {
  max-width: 100%;
  height: auto;
  display: block;
}

.button-container {
  display: flex; /* 버튼을 가로로 배치 */
  justify-content: center; /* 가로 중앙 정렬 */
  gap: 20px; /* 버튼 간 간격 */
  margin-top: 40px; /* 위에서 떨어진 간격 */
}

.btn2,
.btn3 {
  padding: 12px 30px;
  color: white;
  border: none;
  border-radius: 5px;
  cursor: pointer;
  font-size: 16px;
  font-weight: bold;
  width: 300px;
  height: 280px;
  display: flex;
  align-items: center; /* 텍스트 세로 중앙 정렬 */
  justify-content: center; /* 텍스트 가로 중앙 정렬 */
}

.btn2 {
  background-color: #4c8a81; /* 첫 번째 버튼 색상 */
}

.btn3 {
  background-color: #7299cb; /* 두 번째 버튼 색상 */
}

.btn2:hover {
  background-color: #3b6d62;
}

/* 애니메이션 컨테이너 */
.animation-container {
  flex: 1;
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 300px;
  position: relative;
}

/* 움직이는 원 스타일 */
.animated-circle {
  position: absolute;
  border-radius: 50%;
  background-color: #4c8a81;
  opacity: 0.8;
}

/* 첫 번째 원 */
.circle-1 {
  width: 50px;
  height: 50px;
  animation: bounce1 2s infinite ease-in-out;
}

/* 두 번째 원 */
.circle-2 {
  width: 80px;
  height: 80px;
  animation: bounce2 3s infinite ease-in-out;
  background-color: #3b6d62;
}

/* 첫 번째 원 애니메이션 */
@keyframes bounce1 {
  0%, 100% {
    transform: translateY(0) translateX(-30px);
  }
  50% {
    transform: translateY(-40px) translateX(-30px);
  }
}

/* 두 번째 원 애니메이션 */
@keyframes bounce2 {
  0%, 100% {
    transform: translateY(0) translateX(30px);
  }
  50% {
    transform: translateY(-60px) translateX(30px);
  }
}


.features {
  margin-top: 0;
}
</style>

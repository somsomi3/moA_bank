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
                <button v-if="store.isLogin" class="nav-link" @click="logOut">
                  로그아웃
                </button>
              </li>
            </ul>
          </div>
        </div>
      </nav>
    </header>

    <!-- 메인 배너 -->
    <div class="main-banner py-3 bg-white">
      <div class="container-md d-flex align-items-center flex-column-reverse flex-lg-row text-center text-lg-start">
        <div class="banner-text">
          <h1 class="fs-3 fw-bold banner-heading">당신의 경제 생활 매니저, moA</h1>
          <p class="fs-6 text-secondary">경제적인 삶을 위한 맞춤형 금융 솔루션</p>
          <button class="btn2 btn-primary btn-sm mt-3" @click="navigate('start')">지금 시작하기</button>
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
    <footer class="footer bg-white py-2 mt-auto">
      <div class="container text-center">
       
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
    icon: "/searchIcon.png",
    title: "금융 상품 검색",
    description: "예적금, 카드 등 맞춤형 금융 상품을 추천받아 보세요.",
  },
  {
    id: 2,
    icon: "/cardIcon.png",
    title: "카드 제작",
    description: "사용자에 맞는 카드를 만들어보세요.",
  },
  {
    id: 3,
    icon: "/analysisIcon.png",
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
  transition: color 0.3s ease;
}

.navbar .nav-link:hover {
  color: #ffdd57;
}

/* 드롭다운 메뉴 */
.dropdown-menu {
  box-shadow: 0px 4px 12px rgba(0, 0, 0, 0.1);
}

.dropdown-item:hover {
  background-color: #f7faff;
  color: #005bac;
}



.btn2 {  display: inline-block;
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
/* 로그아웃 버튼 */
.logout-btn {
  border-color: white;
  color: white;
}

.logout-btn:hover {
  background-color: white;
  color: #005bac;
}
</style>

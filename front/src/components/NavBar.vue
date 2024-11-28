<template>
  <header class="nav-container">
    <nav class="nav-bar">
      <!-- 네비게이션 메뉴 -->
      <ul class="nav-menu">
        <li class="nav-item"><RouterLink to="/lookup">조회</RouterLink></li>
        <li class="nav-item"><RouterLink to="/transfer">이체</RouterLink></li>
        <li class="nav-item"><RouterLink to="/public-funds">공과금</RouterLink></li>
        <li class="nav-item"><RouterLink to="/exchange">외환</RouterLink></li>
        <li class="nav-item"><RouterLink to="/financial-products">금융상품</RouterLink></li>
      </ul>

      <!-- 아이콘 영역 -->
      <div class="nav-icons">
        <span class="icon">💬</span>
        <span class="icon">🔍</span>
        <span class="icon">☰</span>
      </div>
    </nav>
  </header>
</template>

<script setup>
// Vue Router를 통해 링크를 처리하기 위해 RouterLink를 사용합니다.
import { RouterLink } from "vue-router";
</script>

<style scoped>
/* 네비게이션 바 전체 컨테이너 */
.nav-container {

  top: 80px; /* 화면 상단에서 80px 아래로 위치 */
  width: 100%;
  background-color: white; /* 배경색 */
  z-index: 1000; /* 다른 요소 위에 표시 */
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1); /* 살짝 음영 추가 */
}

/* 네비게이션 바 */
.nav-bar {
  display: flex; /* 플렉스 박스 레이아웃 */
  justify-content: space-between; /* 좌우 끝으로 정렬 */
  align-items: center; /* 수직 가운데 정렬 */
  max-width: 1200px; /* 최대 너비 */
  margin: 0 auto; /* 가운데 정렬 */
  padding: 10px 20px; /* 내부 여백 */
}

/* 네비게이션 메뉴 */
.nav-menu {
  display: flex; /* 플렉스 박스 레이아웃 */
  list-style: none; /* 기본 리스트 스타일 제거 */
  gap: 20px; /* 메뉴 간 간격 */
}

.nav-item {
  font-size: 16px; /* 글꼴 크기 */
  font-weight: 500; /* 글꼴 두께 */
  color: #333; /* 텍스트 색상 */
  text-decoration: none; /* 밑줄 제거 */
  cursor: pointer; /* 클릭 가능 커서 */
}

.nav-item:hover {
  color: #007bff; /* 호버 시 색상 변경 */
  text-decoration: underline; /* 밑줄 추가 */
}

/* 아이콘 영역 */
.nav-icons {
  display: flex; /* 플렉스 박스 레이아웃 */
  gap: 15px; /* 아이콘 간 간격 */
}

.icon {
  font-size: 20px; /* 아이콘 크기 */
  cursor: pointer; /* 클릭 가능 커서 */
}

.icon:hover {
  color: #007bff; /* 호버 시 색상 변경 */
}
</style>

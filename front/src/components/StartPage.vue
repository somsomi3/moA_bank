<template>
  <div class="main-container">
    <!-- 오른쪽 상단 눈사람 아이콘 -->
    <div class="snowman-icon" @click="toggleMenu">☃</div>

    <!-- 가운데 영역 -->
    <div class="center-content">
      <div class="start-button" @click="navigate('start')">시작하기</div>
      <div class="settings-button" @click="navigate('settings')">홈페이지</div>
    </div>

    <!-- 하단 검색 버튼 -->
    <div class="bottom-bar">
      <button class="search-button" @click="navigate('search')">검색하기</button>
    </div>
  </div>
</template>

<script>
export default {
  methods: {
    toggleMenu() {
      alert("메뉴가 열렸습니다! (추후 구현 가능)");
    },
    navigate(target) {
      if (target === "start") {
        this.$router.push({ name: "HelloView" }); // "시작하기" 버튼 클릭 시
      } else if (target === "settings") {
        this.$router.push({ name: "HomePage" }); // "설정" 버튼 클릭 시
      } else if (target === "search") {
        this.$router.push({ name: "SearchProductView" }); // "검색하기" 버튼 클릭 시
      }
    },
  },
};
</script>

<style scoped>
.main-container {
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  align-items: center;
  height: 100vh;
  padding: 20px;
  background-color: #f1f4f8; /* 연한 배경색 */
  position: relative;
}

/* 눈사람 아이콘 */
.snowman-icon {
  position: absolute;
  top: 20px;
  right: 20px;
  font-size: 32px; /* 크기 확대 */
  cursor: pointer;
  color: #6c757d; /* 중간 톤 회색 */
}

.snowman-icon:hover {
  color: #343a40; /* 어두운 회색 */
}

/* 가운데 버튼 섹션 */
.center-content {
  display: flex;
  justify-content: center;
  align-items: center;
  gap: 40px;
  flex-grow: 1;
}

/* 가운데 버튼 스타일 */
.start-button,
.settings-button {
  display: flex;
  justify-content: center;
  align-items: center;
  width: 150px;
  height: 150px;
  font-size: 20px;
  font-weight: bold;
  background-color: #ffffff; /* 흰색 배경 */
  border-radius: 20px; /* 둥근 모서리 */
  box-shadow: 0px 4px 8px rgba(0, 0, 0, 0.1); /* 부드러운 그림자 */
  cursor: pointer;
  transition: all 0.3s ease; /* 부드러운 애니메이션 */
}

.start-button:hover,
.settings-button:hover {
  background-color: #f8f9fa; /* 약간 어두운 흰색 */
  box-shadow: 0px 6px 12px rgba(0, 0, 0, 0.2); /* 더 강조된 그림자 */
}

.start-button {
  color: #007bff; /* 파란 텍스트 */
}

.settings-button {
  color: #28a745; /* 초록 텍스트 */
}

/* 하단 바 */
.bottom-bar {
  width: 100%;
  display: flex;
  justify-content: center;
  padding: 20px 0;
}

.search-button {
  width: 33.3%; /* 버튼 가로 길이를 화면의 1/3로 설정 */
  height: 15%; /* 버튼 높이를 화면의 15%로 설정 */
  font-size: 24px;
  font-weight: bold;
  color: white;
  background-color: #007bff;
  border: none;
  border-radius: 20px;
  box-shadow: 0px 4px 8px rgba(0, 0, 0, 0.1);
  cursor: pointer;
  transition: all 0.3s ease;
}

.search-button:hover {
  background-color: #0056b3;
  box-shadow: 0px 6px 12px rgba(0, 0, 0, 0.2);
}

.search-button:active {
  background-color: #003f7f;
}
</style>

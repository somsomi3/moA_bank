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
    <!-- <div class="bottom-bar">
      <button class="search-button" @click="navigate('search')">검색하기</button>
    </div> -->
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
/* 공통 컨테이너 스타일 */
.container {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  max-width: 1200px;
  margin: 0 auto;
  padding: 20px;
  font-family: 'Noto Sans KR', Arial, sans-serif;
  background-color: #f9f9f9;
  border-radius: 12px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
}

/* 버튼 스타일 */
.button {
  padding: 12px 20px;
  font-size: 16px;
  font-weight: bold;
  color: #ffffff;
  background-color: #4c8a81;
  border: none;
  border-radius: 8px;
  cursor: pointer;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  transition: all 0.3s ease;
}

.button:hover {
  background-color: #3e7066;
}

.button:active {
  transform: scale(0.98);
}

/* 텍스트 강조 */
.text-highlight {
  color: #007bff;
  font-weight: bold;
}

/* 공통 네비게이션 바 스타일 */
.nav-bar {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 10px 20px;
  background-color: #ffffff;
  border-bottom: 1px solid #ddd;
}

.nav-item {
  text-decoration: none;
  color: #4c4c4c;
  margin: 0 10px;
  transition: color 0.3s;
}

.nav-item:hover {
  color: #007bff;
}

/* 드롭다운 스타일 */
.dropdown {
  position: relative;
  display: inline-block;
}

.dropdown-label {
  padding: 8px 12px;
  font-size: 16px;
  font-weight: bold;
  color: #4c4c4c;
  cursor: pointer;
}

.dropdown-menu {
  position: absolute;
  top: 100%;
  left: 0;
  background-color: #ffffff;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
  border-radius: 8px;
  overflow: hidden;
  z-index: 10;
}

.dropdown-item {
  padding: 10px;
  font-size: 14px;
  color: #4c4c4c;
  cursor: pointer;
  transition: background-color 0.3s;
}

.dropdown-item:hover {
  background-color: #f1f3f5;
}


.main-container {
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  align-items: center;
  height: 100vh;
  background-color: #f1f4f8;
  text-align: center;
}

/* 중앙 버튼 */
.center-content {
  display: flex;
  gap: 20px;
  flex-direction: column;
}

.start-button,
.settings-button {
  width: 200px;
  height: 50px;
  font-size: 18px;
  font-weight: bold;
  background-color: #ffffff;
  color: #4c8a81;
  border: 2px solid #4c8a81;
  border-radius: 8px;
  cursor: pointer;
  transition: all 0.3s ease;
}

.start-button:hover,
.settings-button:hover {
  background-color: #4c8a81;
  color: white;
}

/* 하단 버튼 */
.bottom-bar {
  display: flex;
  justify-content: center;
  width: 100%;
}

.search-button {
  width: 80%;
  max-width: 400px;
  padding: 15px;
  font-size: 18px;
  font-weight: bold;
  background-color: #4c8a81;
  color: #ffffff;
  border-radius: 8px;
  cursor: pointer;
  box-shadow: 0px 4px 8px rgba(0, 0, 0, 0.1);
  transition: all 0.3s ease;
}

.search-button:hover {
  background-color: #3e7066;
}


</style>

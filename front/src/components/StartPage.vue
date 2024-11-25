<template>
  <div class="main-container">
    <!-- 종이 흩뿌리는 효과 -->
    <div class="scatter-effect">
      <div
        class="paper"
        v-for="(paper, index) in papers"
        :key="index"
        :style="getPaperStyle(paper)"
      ></div>
    </div>

    <!-- 초록색 줄 위의 회색 박스 -->
    <div class="gray-box">
      <div class="box-item" @click="navigateTo('report')">리포트</div>
      <div class="box-item" @click="navigateTo('fund')">펀드</div>
      <div class="box-item" @click="navigateTo('card-making')">카드메이킹</div>
      <div class="box-item" @click="navigateTo('youth-policy')">청년 정책</div>
    </div>

    <!-- 오른쪽 상단 버튼을 감싸는 박스 -->
    <div class="top-right-buttons-container">
      <div class="top-right-buttons green-box">
        <div class="button-box start-button" @click="navigate('start')">시작하기</div>
      </div>
      <div class="top-right-buttons blue-box">
        <div class="button-box settings-button" @click="navigate('settings')">홈페이지</div>
      </div>
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
    navigateTo(target) {
      if (target === "report") {
        this.$router.push({ name: "ReportView" }); // 리포트 페이지로 이동
      } else if (target === "fund") {
        this.$router.push({ name: "FundView" }); // 펀드 페이지로 이동
      } else if (target === "card-making") {
        this.$router.push({ name: "CardMakingView" }); // 카드메이킹 페이지로 이동
      } else if (target === "youth-policy") {
        this.$router.push({ name: "YouthPolicyView" }); // 청년 정책 페이지로 이동
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
  padding: 2vh;
  position: relative;
}

/* 흩뿌리는 효과 텍스트 */
.scatter-effect {
  position: absolute;
  top: 2vh;
  left: 2vw;
  font-size: 2vw;
  font-weight: bold;
  color: #007bff;
  animation: scatter 3s infinite;
  opacity: 0;
}

/* 흩뿌리는 효과 애니메이션 */
@keyframes scatter {
  0% {
    transform: translate(0, 0) scale(1);
    opacity: 1;
  }
  50% {
    transform: translate(-20px, -30px) scale(1.5);
    opacity: 0.5;
  }
  100% {
    transform: translate(-50px, -60px) scale(0);
    opacity: 0;
  }
}

/* 초록색 줄 */
.main-container::after {
  content: "";
  position: absolute;
  top: 60%; /* 위로부터 60% */
  left: 0;
  width: 100%;
  height: 2px; /* 줄 두께 */
  background-color: #28a745; /* 초록색 */
}

/* 회색 박스 */
.gray-box {
  position: absolute;
  top: 55%; /* 초록색 줄 바로 위 */
  left: 50%;
  transform: translateX(-50%);
  width: 90%; /* 박스 너비 */
  background-color: #e9ecef; /* 연한 회색 */
  border-radius: 1vw; /* 둥근 모서리 */
  box-shadow: 0px 1vh 2vh rgba(0, 0, 0, 0.1); /* 그림자 */
  display: flex;
  justify-content: space-around; /* 아이템 간격 */
  align-items: center;
  padding: 2vh 0;
}

/* 오른쪽 상단 버튼을 감싸는 가로 박스 컨테이너 */
.top-right-buttons-container {
  position: absolute;
  top: 2vh;
  right: 2vw;
  display: flex;
  gap: 1vw; /* 버튼 간격 */
}

/* 초록색 박스 */
.green-box {
  background-color: #d4f4dd; /* 연초록색 */
  padding: 1vh;
  border-radius: 1vw; /* 둥근 모서리 */
  box-shadow: 0px 1vh 2vh rgba(0, 0, 0, 0.1); /* 그림자 */
  display: flex;
  justify-content: center;
  align-items: center;
}

/* 파란색 박스 */
.blue-box {
  background-color: #d9ecff; /* 연파란색 */
  padding: 1vh;
  border-radius: 1vw; /* 둥근 모서리 */
  box-shadow: 0px 1vh 2vh rgba(0, 0, 0, 0.1); /* 그림자 */
  display: flex;
  justify-content: center;
  align-items: center;
}

/* 박스 안의 아이템 */
.box-item {
  font-size: 2vw; /* 글자 크기 */
  font-weight: bold;
  color: #495057; /* 중간 회색 텍스트 */
  cursor: pointer;
  transition: all 0.3s ease;
}

.box-item:hover {
  color: #343a40; /* 어두운 회색 */
  text-decoration: underline; /* 강조 효과 */
}
</style>

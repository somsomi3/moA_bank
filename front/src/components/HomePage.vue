<template>
 <header>
    <nav class="nav-bar">
      <div class="dropdown">
        <div class="dropdown-label" @click="toggleDropdown">
          커뮤니티
        </div>
        <ul v-if="dropdownOpen" class="dropdown-menu">
          <li
            v-for="community in communities"
            :key="community.id"
            @click="selectCommunity(community)"
            class="dropdown-item"
          >
            {{ community.name }}
          </li>
        </ul>
      </div>
      <!-- <RouterLink class="nav-item" :to="{ name: 'ArticleView' }">자유게시판</RouterLink> -->
      <RouterLink class="nav-item" :to="{ name: 'MyPageView' }">마이페이지</RouterLink>
      <RouterLink class="nav-item" :to="{ name: 'LogInView' }">로그인</RouterLink>
      <RouterLink class="nav-item" :to="{ name: 'SignUpView' }">회원가입</RouterLink>
      <button v-if="store.isLogin" class="nav-item logout-btn" @click="logOut">로그아웃</button>
    </nav>
  </header>
</template>

<script setup>
import StartPage from './StartPage.vue';
import { RouterView, RouterLink } from 'vue-router'
import { useCounterStore } from '@/stores/counter'
import { ref } from 'vue';
import { useRouter } from 'vue-router';
import DetailView from '@/views/DetailView.vue';
// const store = useCounterStore()
const store = useCounterStore()
const logOut = function () {
  store.logOut()
}

const communities = ref([
  { id: 1, name: '1~4분위 커뮤니티' },
  { id: 2, name: '5~8분위 커뮤니티' },
  { id: 3, name: '9~10분위 커뮤니티' },
  { id: 4, name: '자유 게시판' },
]);

const router = useRouter();

// 선택한 커뮤니티로 이동
const navigateToCommunity = (event) => {
  const selectedId = parseInt(event.target.value); // 선택된 옵션의 ID
  if (selectedId != 4) {
    router.push({ name: 'DetailView', params: { id: selectedId } });
  } else {
    router.push({ name: 'ArticleView', params: { id: selectedId } });
  }
};


// // 커뮤니티 ID 목록 생성 (1~10)
// const communities = ref([...Array(10).keys()].map((n) => n + 1));

const dropdownOpen = ref(false); // 드롭다운 열림 상태
// 드롭다운 열기/닫기 토글

const toggleDropdown = () => {
  dropdownOpen.value = !dropdownOpen.value;
};

// 커뮤니티 선택 시 라우팅
const selectCommunity = function (community) {
  if (community.id != 4 ) {
  dropdownOpen.value = false; // 드롭다운 닫기
  router.push({ name: 'DetailView', params: { id: community.id } })
} else {
  router.push({ name: 'ArticleView', params: { id: community.id } })
};
}


</script>

<style scoped>
/* 드롭다운 스타일링 */
/* 네비게이션 바 */
.nav-bar {
  display: flex;
  align-items: center;
  padding: 10px 20px;
  background-color: #f9f9f9;
  border-bottom: 1px solid #ccc;
  gap: 20px; /* 요소 간 간격 */
  font-size: 16px;
}

/* 공통 네비게이션 아이템 스타일 */
.nav-item {
  text-decoration: none;
  color: #333;
  cursor: pointer;
  transition: color 0.3s;
}

.nav-item:hover {
  color: #007BFF;
}

/* 로그아웃 버튼 */
.logout-btn {
  border: none;
  background: none;
  font-size: 16px;
  color: #333;
  cursor: pointer;
  transition: color 0.3s;
}

.logout-btn:hover {
  color: #FF5733;
}

/* 드롭다운 스타일 */
.dropdown {
  position: relative;
  display: inline-block;
  cursor: pointer;
}

.dropdown-label {
  padding: 8px 12px;
  user-select: none;
  font-size: 16px;
  cursor: pointer;
}

.dropdown-menu {
  position: absolute;
  top: 100%;
  left: 0;
  margin: 8px 0 0;
  padding: 0;
  list-style: none;
  background-color: #fff;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
  border-radius: 4px;
  width: 200px;
  z-index: 10;
}

.dropdown-item {
  padding: 10px;
  cursor: pointer;
  transition: background-color 0.3s;
  border: 1px solid #ccc;
  border-radius: 4px;
  background-color: #f0f0f0;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1)
}

.dropdown-item:hover {
  background-color: #f0f0f0;
}

/* 드롭다운 기본 스타일 제거 */
.dropdown-menu,
.dropdown-item {
  border: none;
  outline: none;
  background: none;
}

.dropdown-menu {
  border: none;
  outline: none;
  box-shadow: none;
}
</style>

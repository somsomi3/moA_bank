import { ref, computed } from 'vue'
import { defineStore } from 'pinia'
import axios from 'axios'
import { useRouter } from 'vue-router'
import DetailView from '@/views/DetailView.vue'
export const useCounterStore = defineStore('counter', () => {
  const communities = ref([])
  const API_URL = "http://127.0.0.1:8000/"
  const token = ref(null)

  const isLogin = computed(() => {
    if (token.value === null) {
      return false
    } else {
      return true
    }
  })
  const router = useRouter()
  

  const communityid = ref(0)
  
  const getcommunityid = async function () {
    try {
      const res = await axios({
        method: 'get',
        url: `${API_URL}/api/v1/profile/`,
        headers: {
          Authorization: `Token ${token.value}`,
        },
      });
      console.log(res.data,'62362')
      communityid.value = res.data.community; // 커뮤니티 ID 업데이트
      console.log(communityid.value, '234')
      return communityid.value; // 업데이트된 community_id 반환
    } catch (err) {
      console.error('Error fetching community ID:', err);
      return 0; // 에러 발생 시 기본값 반환
    }
  };

  const usercommunity = ref(0)
  // DRF로 전체 게시글 요청을 보내고 응답을 받아 articles에 저장하는 함수
  const getArticles = async function () {
    try {
      usercommunity.value = await getcommunityid(); // 비동기 커뮤니티 ID 가져오기
      console.log("User's community ID:", usercommunity.value); // 디버깅 로그
      if (usercommunity.value !== 0) {
        const res = await axios({
          method: 'get',
          url: `${API_URL}/communities/${usercommunity.value}/articles/list/`,
          headers: {
            Authorization: `Token ${token.value}`,
          },
          
        });
        
        communities.value = res.data; // 게시글 저장

        
      } else {
        console.warn('커뮤니티 ID를 가져올 수 없습니다.');
      }
    } catch (err) {
      console.error('Error fetching articles:', err);
    }
  };

  // 회원가입 요청 액션
  const signUp = function (payload) {
    // const username = payload.username
    // const password1 = payload.password1
    // const password2 = payload.password2
    const { username, name, password1, password2, age, income, job, gender, grade, main_bank, region, consume, desire_period, financial_product } = payload

    axios({
      method: 'post',
      url: `${API_URL}/dj-rest-auth/registration/`,
      data: {
        username, name, password1, password2, age, income, job, gender, grade, main_bank, region, consume, desire_period, financial_product
      }
    })
      .then((res) => {
        // console.log('response_data:',  res.data)
        // console.log('회원가입 성공')
        const password = password1
        
        logIn({ username, password })
      })
      .catch((err) => {
        console.log(err)
      })
  }

  // 로그인 요청 액션
  // const logIn = function (payload) {
  //   // const username = payload.username
  //   // const password1 = payload.password
  //   const { username, password } = payload
  //   axios({
  //     method: 'post',
  //     url: `${API_URL}/accounts/login/`,
  //     headers: {
  //       'Content-Type': 'application/json',
  //     },
  //     data: {
  //       username, password
  //     }
  //   })
  //     .then((res) => {
  //       token.value = res.data.key
  //       router.push({ name: 'HomePage' })
  //       // console.log(res.data)
  //       // console.log('로그인 성공')
  //     })
  //     .catch((err) => {
  //       console.log(err)
  //     })
  // }


  const syncUserData = async function () {
    try {
      usercommunity.value = await getcommunityid(); // 사용자 커뮤니티 ID 동기화
      console.log("사용자 커뮤니티 ID 동기화 완료:", usercommunity.value);
    } catch (err) {
      console.error("사용자 정보 동기화 중 오류 발생:", err);
    }
  };

  
  const logIn = async function (payload) {
    const { username, password } = payload;
    try {
      const res = await axios({
        method: "post",
        url: `${API_URL}/accounts/login/`,
        headers: {
          "Content-Type": "application/json",
        },
        data: {
          username,
          password,
        },
      });
      token.value = res.data.key; // 토큰 저장
  
      // 로그인 후 사용자 정보 동기화
      await syncUserData();
  
      router.push({ name: "HomePage" }); // 홈 페이지로 이동
    } catch (err) {
      console.error("로그인 실패:", err);
    }
  };
  
  const logIn2 = async function (payload) {
    const { username, password } = payload;
    try {
      const res = await axios({
        method: "post",
        url: `${API_URL}/accounts/login/`,
        headers: {
          "Content-Type": "application/json",
        },
        data: {
          username,
          password,
        },
      });
      token.value = res.data.key; // 토큰 저장
  
      // 로그인 후 사용자 정보 동기화
      await syncUserData();
  
       // 홈 페이지로 이동
    } catch (err) {
      console.error("로그인 실패:", err);
    }
  };
  // [추가기능] 로그아웃
  const logOut = function () {
    axios({
      method: 'post',
      url: `${API_URL}/accounts/logout/`,
    })
      .then((res) => {
        console.log(res.data)
        token.value = null
        router.push({ name: 'HomePage' })
      })
      .catch((err) => {
        console.log(err)
      })
  }


  const userDecile = ref(null); // 사용자 decile 값 저장

// 사용자 정보를 가져오는 메서드 추가
const fetchUserDecile = async () => {
  try {
    const response = await axios.get(`${API_URL}/api/v1/profile/`, {
      headers: {
        Authorization: `Token ${token.value}`,
      },
    });
    userDecile.value = response.data.user_decile; // 사용자 decile 값 저장
    console.log("사용자 decile:", userDecile.value);
  } catch (err) {
    console.error("사용자 decile 가져오기 실패:", err);
    userDecile.value = null; // 실패 시 기본값 설정
  }
};


  return { communities, API_URL, getArticles, signUp, logIn, token, isLogin, logOut, getcommunityid, userDecile, fetchUserDecile, logIn2 }
}, { persist: true })

export const useLayoutStore = defineStore('layout', {
  state: () => ({
    navVisible: true, // 기본적으로 nav를 표시
  }),
  actions: {
    hideNav() {
      this.navVisible = false;
    },
    showNav() {
      this.navVisible = true;
    },
  },
});
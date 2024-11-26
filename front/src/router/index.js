import { createRouter, createWebHistory } from 'vue-router'
import ArticleView from '@/views/ArticleView.vue'
import DetailView from '@/views/DetailView.vue'
import CreateView from '@/views/CreateView.vue'
import SignUpView from '@/views/SignUpView.vue'
import LoginView from '@/views/LogInView.vue'
import { useCounterStore } from '@/stores/counter'
import HomePage from '@/components/HomePage.vue'
import StartPage from '@/components/StartPage.vue'
import { useLayoutStore } from '@/stores/counter'
import HelloView from '@/views/HelloView.vue'
import MyPageView from '@/views/MyPageView.vue'
import SearchProductView from '@/views/SearchProductView.vue'
import ArticleListItem from '@/components/ArticleListItem.vue'
import ArticleListItem2 from '@/components/ArticleListItem2.vue'
import App from '@/App.vue'
import CreateView2 from '@/views/CreateView2.vue'
import CommentView from '@/views/CommentView.vue'
import ArticleEdit from '@/views/ArticleEdit.vue'
import MakeCardView from '@/views/MakeCardView.vue'


const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/articles/:id',
      name: 'CommunityDetail',
      component: DetailView,
      props: true, // URL 매개변수를 컴포넌트에 props로 전달
    },
    {
      path: '/articlelistitem/:id',
      name: 'ArticleListItem',
      component: ArticleListItem,
      props: true, // URL 매개변수를 컴포넌트에 props로 전달
    },
    {
      path: '/articlelistitem/:id',
      name: 'ArticleListItem2',
      component: ArticleListItem2,
      props: true, // URL 매개변수를 컴포넌트에 props로 전달
    },
    {
      path: '/',
      name: 'StartPage',
      component: StartPage
    },
    {
      path: '/articles/:id',
      name: 'DetailView',
      component: DetailView,
      props: true,
    },
    {
      path: '/create',
      name: 'CreateView',
      component: CreateView
    },
    {
      path: '/signup',
      name: 'SignUpView',
      component: SignUpView
    },
    {
      path: '/login',
      name: 'LogInView',
      component: LoginView
    },    
    {
      path: '/HomePage',
      name: 'HomePage',
      component: HomePage
    },
    {
      path: '/articles',
      name: 'ArticleView', // 라우트 이름 정의
      component: ArticleView, // 관련 컴포넌트 연결
    },
    {
      path: '/create2',
      name: 'CreateView2', // 라우트 이름 정의
      component: CreateView2, // 관련 컴포넌트 연결
    },
    {
      path: '/HelloView',
      name: 'HelloView', // 라우트 이름 정의
      component: HelloView, // 관련 컴포넌트 연결
    },
    {
      path: '/MyPageView',
      name: 'MyPageView', // 라우트 이름 정의
      component: MyPageView, // 관련 컴포넌트 연결
    },
    {
      path: '/SearchProductView',
      name: 'SearchProductView', // 라우트 이름 정의
      component: SearchProductView, // 관련 컴포넌트 연결
    },
    {
      path: '/articles/:id/edit',
      name: 'ArticleEdit',
      component: ArticleEdit
    },
    {
      path: '/communities/:community_id/articles/:id/comments/:comment_id/',
      name: 'CommentView',
      component : CommentView,
      props: true,
    },
    {
      path: '/MakeCardView',
      name: 'MakeCardView',
      component: MakeCardView,
    },

  ]
})

router.beforeEach((to, from) => {
  const store = useCounterStore()
  
  if (to.name === 'App') {
    return true
  }
  // 만약 이동하는 목적지가 메인 페이지이면서
  // 현재 로그인 상태가 아니라면 로그인 페이지로 보냄
  // else if (to.name === 'ArticleView' && !store.isLogin) {
  //   window.alert('로그인이 필요합니다.')
  //   return { name: 'LogInView' }
  // }
  
  else if (to.name === 'DetailView' && !store.isLogin) {
    window.alert('로그인이 필요합니다.')
    return { name: 'LogInView' }
  }

  else if (to.name === 'MyPageView' && !store.isLogin) {
    window.alert('로그인이 필요합니다.')
    return { name: 'LogInView' }
  }
  // 만약 로그인 사용자가 회원가입 또는 로그인 페이지로 이동하려고 하면
  // 메인 페이지로 보냄
  else if ((to.name === 'SignUpView' || to.name === 'LogInView') && (store.isLogin)) {
    window.alert('이미 로그인 되어있습니다.')
    return { name: 'HomePage' }
  }
})

export default router























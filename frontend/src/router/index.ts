import { createRouter, createWebHistory } from 'vue-router'
import AccountPage from '../views/AccountPage.vue'
import AdminPage from '../views/AdminPage.vue'
import ArticlesView from '../views/ArticlesView.vue'
import DashboardPage from '../views/DashboardPage.vue'
import LandingPage from '../views/LandingPage.vue'
import LoginPage from '../views/LoginPage.vue'
import QuizPage from '../views/QuizPage.vue'
import ReaderView from '../views/ReaderView.vue'
import RegisterPage from '../views/RegisterPage.vue'
import SummaryPage from '../views/SummaryPage.vue'

const router = createRouter({
  history: createWebHistory(),
  routes: [
    {
      path: '/',
      name: 'Landing',
      component: LandingPage
    },
    {
      path: '/login',
      name: 'Login',
      component: LoginPage
    },
    {
      path: '/register',
      name: 'Register',
      component: RegisterPage
    },
    {
      path: '/dashboard',
      name: 'Dashboard',
      component: DashboardPage
    },
    {
      path: '/articles',
      name: 'Articles',
      component: ArticlesView
    },
    {
      path: '/article/:id',
      name: 'Reader',
      component: ReaderView
    },
    {
      path: '/quiz',
      name: 'Quiz',
      component: QuizPage
    },
    {
      path: '/summary',
      name: 'Summary',
      component: SummaryPage
    },
    {
      path: '/account',
      name: 'Account',
      component: AccountPage
    },
    {
      path: '/admin',
      name: 'Admin',
      component: AdminPage
    }
  ]
})

export default router

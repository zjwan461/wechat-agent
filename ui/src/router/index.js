import Vue from 'vue'
import VueRouter from 'vue-router'
import NProgress from 'nprogress'
import 'nprogress/nprogress.css'

Vue.use(VueRouter)

const routes = [{
  path: '/',
  redirect: '/home'
},
{
  path: '/login',
  component: () => import('../views/login.vue')
},
{
  path: '/register',
  component: () => import('../views/register')
},
{
  path: '/home',
  name: 'home',
  component: () => import('../views/home.vue'),
  redirect: '/index',
  children: [{
    path: '/index',
    name: 'index',
    component: () => import('../views/watch.vue')
  }, {
    path: '/setting',
    name: 'setting',
    component: () => import('../views/setting.vue')
  }, {
    path: '/agent',
    name: 'agent',
    component: () => import('../views/agent/index.vue')
  }, {
    path: '/ai-role',
    name: 'aiRole',
    component: () => import('../views/aiRole/index.vue')
  }, {
    path: '/reply',
    name: 'reply',
    component: () => import('../views/reply/index.vue')
  }
  ]
}]

const router = new VueRouter({
  routes
})

NProgress.configure({
  easing: 'ease', // 动画方式
  speed: 100, // 递增进度条的速度
  showSpinner: false, // 是否显示加载ico
  trickleSpeed: 200, // 自动递增间隔
  minimum: 0.3 // 初始化时的最小百分比
})

router.beforeEach((to, from, next) => {
  NProgress.start()
  if (to.path === '/login' || to.path === '/register') return next()
  const token = window.sessionStorage.getItem('Authorization')
  if (!token) return next('/login')
  next()
})

router.afterEach(() => {
  NProgress.done() // 关闭进度条
})

export default router

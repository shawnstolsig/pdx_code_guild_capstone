import Vue from 'vue'
import VueRouter from 'vue-router'
import Home from '../views/Home.vue'
import JWTTest from '../views/JWTTest.vue'
import About from '../views/About.vue'
import Login from '../views/Login.vue'
import store from '../store/index.js'

Vue.use(VueRouter)

const routes = [
  // protected route, must be authenticated to access home
  {
    path: '/',
    name: 'home',
    component: Home,
    beforeEnter (to, from, next){
      if(store.state.isAuthenticated){
        next()
      } else {
        next('/login')
      }
    }
  },
  {
    path: '/login',
    name: 'login',
    component: Login
  },
  {
    path: '/jwttest',
    name: 'jwtTest',
    component: JWTTest
  },
  {
    path: '/about',
    name: 'about',
    component: About
  }
]

const router = new VueRouter({
  mode: 'history',
  base: process.env.BASE_URL,
  routes
})

export default router

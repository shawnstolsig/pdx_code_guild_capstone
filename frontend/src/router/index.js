import Vue from 'vue'
import VueRouter from 'vue-router'
import Dashboard from '../views/Dashboard.vue'
import Settings from '../views/Settings.vue'
import Kiosk from '../views/Kiosk.vue'
import JWTTest from '../views/JWTTest.vue'
import Login from '../views/Login.vue'
import store from '../store/index.js'

Vue.use(VueRouter)

const routes = [
  // protected route, must be authenticated to access home
	{
		path: '/',
		name: 'dashboard',
		component: Dashboard,
		beforeEnter (to, from, next){
		if(store.state.isAuthenticated){
				next()

			} else {
				next('/login')
			}
		},
	},
	{
		path: '/settings',
		name: 'settings',
		component: Settings,
		beforeEnter (to, from, next){
			if(store.state.isAuthenticated){
				next()
			} else {
				next('/login')
			}
		}
	},
	{
		path: '/kiosk',
		name: 'kiosk',
		component: Kiosk,
		beforeEnter (to, from, next){
			store.dispatch('setKioskMode', true)
			next()
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
]

const router = new VueRouter({
	mode: 'history',
	base: process.env.BASE_URL,
	routes
})

export default router

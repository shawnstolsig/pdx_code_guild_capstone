import Vue from 'vue'
import VueRouter from 'vue-router'
import Dashboard from '../views/Dashboard.vue'
import Settings from '../views/Settings.vue'
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
				// // load the first workspace if none is loaded
				// if(store.getters.workspace.id == undefined){
				// 	console.log("First login to site, loading workspace with index 0")
				// 	// load workspace data
				// 	store.dispatch('loadWorkspace', {index: 0})
				// } 
				// // reload the same workspace if previously loaded
				// else {
				// 	console.log(`Returning back to dashboard with a workspace already loaded, loading workspace with index ${store.getters.workspace.id}`)
				// 	store.dispatch('loadWorkspace', {key: store.getters.workspace.id})
				// }

				next()

			} else {
				next('/login')
			}
		},
		beforeRouteUpdate(to, from, next){

			next()
		}
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

import Vue from 'vue'
// For connecting to Django backend using JWT
import axios from 'axios'
import VueAxios from 'vue-axios'
import jwt_decode from 'jwt-decode'
import Vuex from 'vuex'
import router from '../router'

// For using JWT and Axios
Vue.use(VueAxios, axios)
Vue.use(Vuex)


export default new Vuex.Store({

	state: {

		// ==========  Authentication =============================================
		// For managing User logins
		authUser: {},
		isAuthenticated: false,
		
		// JSON Web Token 
		jwt_access: localStorage.getItem('accessToken'),
		jwt_refresh: localStorage.getItem('refreshToken'),
		jwt_refresh_expiration: localStorage.getItem('refreshExpiration'),
		jwt_access_expiration: localStorage.getItem('accessExpiration'),
		endpoints: {
			obtainJWT: 'http://localhost:8000/auth/jwt/create',
			refreshJWT: 'http://localhost:8000/auth/jwt/refresh',
			baseURL: 'http://localhost:8000',
			baseAPI: 'http://localhost:8000/api/v1',
		},
		// ========================================================================
		
	},   // end Vuex state

	getters: {
		userInfo(state){
			return state.authUser
		},
		isAuthenticated(state){
			return state.isAuthenticated
		},
		accessToken(state){
			return state.jwt_access
		},
		refreshToken(state){
			return state.jwt_refresh
		},
		endpoints(state){
			return state.endpoints
		},
	},	// end Vuex getters

	mutations: {

		// Login: set the authenticated user in state
		setAuthUser(state,payload){
			Vue.set(state, 'authUser', payload.authUser)
			Vue.set(state, 'isAuthenticated', payload.isAuthenticated)
		},

		// Logout: null authenticated user in state
		unsetAuthUser(state){
			Vue.set(state, 'authUser', {});
			Vue.set(state, 'isAuthenticated', false)
		},

		// Update local storage and Vuex state with new JWT
		updateToken(state, newToken) {
			// Broken into two if statements as the refresh token is not always provided (only get an access when you refresh)
			if(newToken.access){
				state.jwt_access = newToken.access;
				state.jwt_access_expiration = jwt_decode(newToken.access).exp		// expiration datetime of access token
				localStorage.setItem('accessToken', state.jwt_access)
				localStorage.setItem('accessExpiration', state.jwt_access_expiration)
			}
			if(newToken.refresh){
				state.jwt_refresh = newToken.refresh;
				state.jwt_refresh_expiration  = jwt_decode(newToken.refresh).exp;         // expiration datetime of access token
				localStorage.setItem('refreshToken', state.jwt_refresh)
				localStorage.setItem('refreshExpiration', state.jwt_refresh_expiration)
			}
		},
		
		// Remove JWT from local Vuex storage and state
		removeToken(state) {
			state.jwt_access = null;
			state.jwt_refresh = null;
			state.jwt_access_expiration = null;
			state.jwt_refresh_expiration = null;
			localStorage.removeItem('accessToken');
			localStorage.removeItem('refreshToken');
			localStorage.removeItem('accessExpiration');
			localStorage.removeItem('refreshExpiration');
		},
		
	},	// end Vuex mutations
	
	actions: {
		
		// Use Axios to get new JWT, provided username and password payload
		obtainToken(context, payload) {
			
			// Get tokens and update user information (payload is username and password)
			axios.post(this.state.endpoints.obtainJWT, payload)
			.then(response => {
				
				// update tokens in state
				this.commit('updateToken', response.data);
				
				// Set state information for logged in user
				const token = response.data.access
				if (token) {

					// send user_id next axios call, to pull User info from API
					return axios({
						method: 'get',
						url: `${this.state.endpoints.baseURL}/auth/users/me/`,
						headers: {
							authorization: `Bearer ${response.data.access}`
						}
					})

					} else {
						alert("trying to decode user from access token but no token found!")
					}
				})
				// Set user information
				.then(response => {
					this.commit('setAuthUser', {

						// in Vuex store, add user information retrieved from API
						authUser: {
							userId: response.data.id,
							username: response.data.username,
							lastLogin: response.data.last_login,
							firstName: response.data.first_name,
							lastName: response.data.last_name,
							isActive: response.data.is_active,
							dateJoined: response.data.date_joined,
							email: response.data.email,
							darkModeEnabled: response.data.darkModeEnabled,
						},
						isAuthenticated: true,
					})

					// Start logout timer.  Currently, based on simplejwt config, this is 5 min.
					let now = new Date()
					context.dispatch('setLogoutTimer', this.state.jwt_access_expiration * 1000 - now)

					// redirect user to Dashboard
					router.push({name:'home'})

				}).catch((error) => {
					console.log(error);
					if(error == 'Error: Request failed with status code 401'){
						alert('Invalid credentials, please try again')
					} else {
						alert("Server error during login.")
					}
				})
		},

		// Delete stored token, both in localStorage and state
		deleteToken() {
			this.commit("removeToken")
			this.commit("unsetAuthUser")
			router.push({name: "login"})
		},

		// Use Axios to refresh existing JWT (no username/password needed with refresh, just refresh token)
		refreshToken() {
			const payload = {
				refresh: this.state.jwt_refresh
			}

			axios.post(this.state.endpoints.refreshJWT, payload)
				.then((response) => {
					this.commit('updateToken', response.data)
				})
				.catch((error) => {
					console.log(error)
					alert("Error freshing access token...make sure refresh token passed to backend!")
				})
		},

		// Verify JWT is valid.  Prompt user if they need to login again.
		inspectToken() {
			if (this.state.jwt_access) {
				const access_exp = this.state.jwt_access_expiration
				const refresh_exp = this.state.jwt_refresh_expiration
				alert(`refresh_exp is ${refresh_exp} and access_exp is ${access_exp}`)
				if (access_exp - (Date.now() / 1000) < 1800 && (Date.now() / 1000) - refresh_exp < 628200) {
					this.dispatch('refreshToken')
					alert("token inspected, refreshing token")
				} else if (access_exp - (Date.now() / 1000) < 1800) {
					// DO NOTHING, DO NOT REFRESH   
					alert("token inspected, no issues")
				} else {
					// PROMPT USER TO RE-LOGIN
					// THIS ELSE CLAUSE COVERS THEN CONDITION WHERE A TOKEN IS EXPIRED
					alert("Authentication token expired), please login again!")
					router.push({name: 'login'})
				}
			}
			else {
				alert("No token detected.")
			}
		},

		// Auto-logout action
		setLogoutTimer(context, expirationTime){
			setTimeout(() => {
				context.dispatch('deleteToken')
			}, expirationTime)
		},

		// Auto-login
		tryAutoLogin(){
			// get access token from local storage
			let token = localStorage.getItem('accessToken')
			// if no token, abort auto login...return
			if(!token){
				return
			}
			
			// if token is in local storage, get expiration date
			let expirationDate = localStorage.getItem('accessExpiration')
			let now = new Date()			

			// if token has expired, abort auto login....return
			if (now >= expirationDate*1000){
				return 
			}
			
			// valid, unexpired token...so retrieve authenticated user information from backend sending token
			axios({
				method: 'get',
				url: `${this.state.endpoints.baseURL}/auth/users/me/`,
				headers: {
					authorization: `Bearer ${token}`
				}
			}).then(response => {
				this.commit('setAuthUser', {

					// in Vuex store, add user information retrieved from API
					authUser: {
						userId: response.data.id,
						username: response.data.username,
						lastLogin: response.data.last_login,
						firstName: response.data.first_name,
						lastName: response.data.last_name,
						isActive: response.data.is_active,
						dateJoined: response.data.date_joined,
						email: response.data.email,
						darkModeEnabled: response.data.darkModeEnabled,
					},
					isAuthenticated: true,
				})
			})
		},

		// Update authUser after they update their account info
		updateAuthUser(context, payload){
			this.commit('setAuthUser', payload);
		}
	},	// end Vuex actions

	modules: {

	}	// end Vuex modules
})
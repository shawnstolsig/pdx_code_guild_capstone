import Vue from 'vue'
// For connecting to Django backend using JWT
import axios from 'axios'
import VueAxios from 'vue-axios'
import jwt_decode from 'jwt-decode'
import Vuex from 'vuex'
// For using JWT and Axios
Vue.use(VueAxios, axios)
Vue.use(Vuex)


export default new Vuex.Store({

	state: {

		// JSON Web Token 
		jwt_access: localStorage.getItem('accessToken'),
		jwt_refresh: localStorage.getItem('refreshToken'),
		endpoints: {
			obtainJWT: 'http://localhost:8000/api/v1/token/obtain',
			refreshJWT: 'http://localhost:8000/api/v1/token/refresh'
		}

	},   // end Vuex state

	mutations: {

		// Update local storage and Vuex state with new JWT
		updateToken(state, newToken) {
			console.log(`state: `)
			console.log(state)
			console.log(`newToken: `)
			console.log(newToken)
			if(newToken.access){
				localStorage.setItem('accessToken', newToken.access);
				state.jwt_access = newToken.access;
			}
			if(newToken.refresh){
				localStorage.setItem('refreshToken', newToken.refresh);
				state.jwt_refresh = newToken.refresh;
			}
		},
		// Remove JWT from local Vuex storage and state
		removeToken(state) {
			localStorage.removeItem('accessToken');
			localStorage.removeItem('refreshToken');
			state.jwt_access = null;
			state.jwt_refresh = null;
		}

	},	// end Vuex mutations

	actions: {

		// Use Axios to get new JWT, provided username and password payload
		// obtainToken(username, password) {
		obtainToken(context, payload) {
			axios.post(this.state.endpoints.obtainJWT, payload)
				.then((response) => {
					this.commit('updateToken', response.data);
				})
				.catch((error) => {
					console.log(error);
					alert("Error obtaining token...make sure username and password specified!")
				})
		},

		// Delete stored token, both in localStorage and state
		deleteToken() {
			this.commit("removeToken")
		},

		// Use Axios to refresh existing JWT (no username/password needed with refresh)
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
			const token = this.state.jwt_access;
			if (token) {
				const decoded = jwt_decode(token);
				const exp = decoded.exp
				const orig_iat = decoded.orig_iat

				if (exp - (Date.now() / 1000) < 1800 && (Date.now() / 1000) - orig_iat < 628200) {
					this.dispatch('refreshToken')
					alert("token inspected, refreshing token")
				} else if (exp - (Date.now() / 1000) < 1800) {
					// DO NOTHING, DO NOT REFRESH   
					alert("token inspected, no issues")
				} else {
					// PROMPT USER TO RE-LOGIN
					// THIS ELSE CLAUSE COVERS THEN CONDITION WHERE A TOKEN IS EXPIRED
					alert("token inspection failed (expired), please login again!")
				}
			}
			else {
				alert("no token detected")
			}
		}
	},	// end Vuex actions

	modules: {

	}	// end Vuex modules
})
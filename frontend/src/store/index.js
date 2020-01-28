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
        user: {
            userId: '',
            username: '',
            firstName: '',
            lastName: '',
            fullName: '',
            email: '',
            darkModeEnabled: '',
            organization: '',
            department: '',
        },
        isAuthenticated: false,
        organization: {},
        jwt: {
            access: localStorage.getItem('accessToken'),
            refresh: localStorage.getItem('refreshToken'),
            refreshExpiration: localStorage.getItem('refreshExpiration'),
            accessExpiration: localStorage.getItem('accessExpiration'), 
        },
        endpoints: {
            obtainJWT: 'http://localhost:8000/auth/jwt/create',
			refreshJWT: 'http://localhost:8000/auth/jwt/refresh',
			baseURL: 'http://localhost:8000',
			baseAPI: 'http://localhost:8000/api/v1',
        },
        formRules: {
			name: [
				v => !!v || 'Name is required.',
				v => (v && v.length) <= 30 || 'Name must be less than 30 characters.',
				v => (v && v.length) >= 3 || 'Name must be at least 3 characters.',
			],
			email: [
				v => !!v || 'E-mail is required.',
				// v => /.+@.+/.test(v) || 'E-mail must be valid.',
				v => (v && v.indexOf("@") !== 0) || 'Email should have username.',
				v => (v && !!v.includes("@")) || 'Email should have @ sybol.',
				v => (v && v.indexOf(".") - v.indexOf('@') > 1)|| 'Email should have have domain.',
				v => (v && !!v.indexOf(".")) || 'Email should have have domain.',
				v => (v && v.indexOf('.') <= v.length - 3) || 'Email should contain a valid domain extension.'
            ],
            password: [
                v => !!v || 'Password is required.',
                v => (v && v.length) >= 6 || 'Password must be at least 6 characters.',
            ],
            description: [
                v => !!v || 'Description is required.',
                v => (v && v.length) >= 3 || 'Name must be at least 3 characters.',
            ],
            code: [ v => !!v || 'Please input Organization code.' ],
        }

    },      // end Vuex state

    getters: {
        user(state){ return state.user },
        username(state){ return state.user.username },
        isAuthenticated(state){ return state.isAuthenticated },
        accessToken(state){ return state.jwt.access },
        refreshToken(state){ return state.jwt.refresh },
        endpoints(state){ return state.endpoints },
        organization(state) { return state.organization },
        formRules(state){ return state.formRules }
    },    // end Vuex getters

    mutations: {

        // Update tokens
        updateTokens(state, newTokens){
            // Broken into two if statements as the refresh token is not always provided (only get an access when you refresh)
			if(newTokens.access){
				state.jwt.access = newTokens.access;
				state.jwt.accessExpiration = jwt_decode(newTokens.access).exp;		// expiration datetime of access token
				localStorage.setItem('accessToken', state.jwt.access);
				localStorage.setItem('accessExpiration', state.jwt.accessExpiration);
			}
			if(newTokens.refresh){
				state.jwt.refresh = newTokens.refresh;
				state.jwt.refreshExpiration  = jwt_decode(newTokens.refresh).exp;         // expiration datetime of access token
				localStorage.setItem('refreshToken', state.jwt.refresh);
				localStorage.setItem('refreshExpiration', state.jwt.refreshExpiration);
			}
        },

        // Update user information (takes in whatever is sent from API)
        updateUser(state, managerItem){
            state.user = managerItem
        },

        // For reactively updating User model info only
        updateUserInfoOnly(state, userPayload){
            state.user['userId'] = userPayload.id
            state.user['username'] = userPayload.username
            state.user['firstName'] = userPayload.first_name
            state.user['lastName'] = userPayload.last_name
            state.user['email'] = userPayload.email
        },
        
        // For reactively updating Manager model info only
        updateManagerInfoOnly(state, managerPayload){
            state.user['fullName'] = managerPayload.full_name
            state.user['darkModeEnabled'] = managerPayload.dark_mode_enabled
            state.user['organization'] = managerPayload.organization
            state.user['department'] = managerPayload.department

        },

        // Clear state/log user out
        clearStateAndLocalStorage(state){

            // clear state
            state.user = {
                userId: '',
                username: '',
                firstName: '',
                lastName: '',
                fullName: '',
                email: '',
                darkModeEnabled: '', 
                organization: '',
                department: '',
            }
            state.jwt = {
                access: '',
                refresh: '',
                refreshExpiration: '',
                accessExpiration: '', 
            }

            // clear local storage
			localStorage.removeItem('accessToken');
			localStorage.removeItem('refreshToken');
			localStorage.removeItem('accessExpiration');
            localStorage.removeItem('refreshExpiration');

            // set isAuthenticated to false
            state.isAuthenticated = false
        },

        // Set user org after initial login
        setUserOrganization(state, orgId){
            state.user['organization'] = orgId
        },

        // Set organization in state
        setOrganization(state, payload){
            state.organization = payload
        }

    },  // end Vuex mutations

    actions: {
        
        // Register user
        register(context, fullUserPayload){
            
            // Post to djoser registration endpoint
            const registrationPayload = {
                username: fullUserPayload.username,
                password: fullUserPayload.password,
                email: fullUserPayload.email,
            }
            axios({
				method: 'post',
				url: `${this.state.endpoints.baseURL}/auth/users/`,
				data: registrationPayload,
            })
            // Set up for login, now that we have account created (and a user id)
            .then(response => {
                
                // Print status message to console
                console.log(`User ${response.data.username} successfully created.`)
                
                // Store user ID for updating User backend
                fullUserPayload['userId'] = response.data.id
                this.state.user['userId'] = response.data.id
                
                // Log user in...must use another axios here so that we can wait to updateUserBackend once tokens obtained
                const loginPayload = {
                    username: fullUserPayload.username,
                    password: fullUserPayload.password
                }

                // Login
                return axios({
                    method: 'post',
                    url: this.state.endpoints.obtainJWT,
                    data: loginPayload,
                })
            })
            // Setup for posting manager/user info
            .then(response => {

                // Print status message to console
                console.log(`User logged in after registration.`)

                // Update authentication status
                this.state.isAuthenticated = true

                // Store tokens
                this.commit('updateTokens', response.data)

                // Post Manager/User info
                this.dispatch('updateUserBackend', fullUserPayload)

                // Send to home page after registration
                router.push('settings')
            })
            .catch(error => {
                console.log(error)
                if (error == 'Error: request failed with status code 400'){
                    alert("Invalid credentials.  Possible causes:\n Username taken already\nCommon password\nInvalid email")
                }
            })
        },

        // Logs user in when given username/password payload
        login(context, payload){
            
            // Given username/password, get tokens 
            axios({
                method: 'post',
                url: this.state.endpoints.obtainJWT,
                data: payload,
            })
            // With successful login, commit token mutations, set logout timer, and get Manager/User info 
            .then(response => {

                // Set isAuthenticated
                this.state.isAuthenticated = true

                // Mutate tokens
                this.commit('updateTokens', response.data)

                // Set logout timer
                let now = new Date()
                let expirationTime = this.state.jwt.accessExpiration * 1000
                this.dispatch('setLogoutTimer', expirationTime - now)

                // Get Manager/User info
                let userId = jwt_decode(this.state.jwt.access).user_id
                return axios({
                    method: 'get',
                    url: `${this.state.endpoints.baseAPI}/managers/${userId}/`,
                    headers: {
                        authorization: `Bearer ${this.state.jwt.access}`
                    }
                })
            })
            // Once all Manager/User information obtained, commit mutations to store
            .then(response => {

                // Mutate user information
                this.commit('updateUserInfoOnly', response.data.user)
                this.commit('updateManagerInfoOnly', response.data)
                this.dispatch('loadOrganization')

                // Send to home screen
                router.push('home')
            })
            // Catch errors
            .catch(error => {
                if(error == 'Error: Request failed with status code 401'){
                    alert('Invalid credentials, please try again.')
                } else {
                    alert('Server error during login.')
                    console.log(error)
                }

            })
        },
        
        // Logs user out
        logout(){
            this.commit('clearStateAndLocalStorage')
            router.push('login')
        },
        
        // Checks if user is still logged in (are tokens valid?)
        verifyLogin(){
            console.log(Date.now())
            
            // If state has token
            if(this.state.jwt.access){

                // Set user to isAuthenticated
                this.state.isAuthenticated = true

                // Get expirations
                const accessExp = this.state.jwt.accessExpiration
                const refreshExp = this.state.jwt.refreshExpiration
                
                if(accessExp - (Date.now() / 1000) > 0 ){
                    console.log("I think my access token is good")
                }
                if(accessExp - (Date.now() / 1000) < 0 ){
                    console.log("I think my access token is bad")
                }
                if(refreshExp - (Date.now() / 1000) > 0){
                    console.log("I think my refresh token is good")
                }
                if(refreshExp - (Date.now() / 1000) < 0){
                    console.log("I think my refresh token is bad")
                }

                // Access token is good, do nothing.  Still has at least 5 seconds left.
                if (accessExp - (Date.now() / 1000) >= 5) {
                    console.log("Access token checked, it's valid...no refresh needed.")
                } 

                // If access token has expired (or will within 5 seconds) and we have a valid refresh token, then refresh token
				else if ((accessExp - (Date.now() / 1000)) < 5 && (refreshExp - (Date.now() / 1000)) >= 5) {
                    console.log("Access token expired but refresh token is valid. Refreshing access token.")
                    
                    axios({
                        method: 'post',
                        url: this.state.endpoints.refreshJWT,
                        data: this.state.jwt.refresh
                    }).then(response => {
                        this.commit('updateTokens', response.data)
                    }).catch(error => {
                        console.log(error)
                        alert("Error refreshing access token...please re-login.")
                        router.push('login')
                    })
                } 
                
                // If unable to refresh access token, prompt user to re-login.
                else {
					alert("Authentication token expired, please re-login.")
					router.push('login')
				}
            }
            else {
                alert("No authentication token found, please login.")
				router.push('login')
            }
        },
        
        // Update user info
        updateUserBackend(context, payload){

            // Patch user model
            axios({
                method: 'patch',
                url: `${this.state.endpoints.baseAPI}/users/${payload.userId}/`,
                data: {
                    username: payload.username,
                    first_name: payload.firstName,
                    last_name: payload.lastName,
                    email: payload.email,
                },
                headers: {
                    authorization: `Bearer ${this.state.jwt.access}`
                }
            })
            .then(response => {
                console.log(response)

                this.commit('updateUserInfoOnly', response.data)
            })
            .catch(error => console.log(error))
            
            // Patch manager model
            axios({
                method: 'patch',
                url: `${this.state.endpoints.baseAPI}/managers/${payload.userId}/`,
                data: {
                    full_name: payload.fullName,
                    dark_mode_enabled: payload.darkModeEnabled,
                },
                headers: {
                    authorization: `Bearer ${this.state.jwt.access}`
                }
            })
            .then(response => {
                console.log(response)
                this.commit('updateManagerInfoOnly', response.data)
            })
            .catch(error => console.log(error))
        },
        
        // Sets a timer for logging the user out
        setLogoutTimer(context, expirationTime){
            setTimeout(() => {
				context.dispatch('logout')
			}, expirationTime)
        },
        
        // Checks local storage for token to auto login
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

			// With valid token, get user id from backend
            axios({
                method: 'get',
                url: `${this.state.endpoints.baseURL}/auth/users/me/`,
                headers: {
					authorization: `Bearer ${token}`
				}
            }).then(response => {
                // Get Manager/User info
                let userId = response.data.id
                console.log(`Autologin: user id ${userId} obtained.`)
                return axios({
                    method: 'get',
                    url: `${this.state.endpoints.baseAPI}/managers/${userId}`,
                    headers: {
                        authorization: `Bearer ${token}`
                    }
                })
            })
            // Once all Manager/User information obtained, commit mutations to store
            .then(response => {

                // Mutate user information
                this.commit('updateUserInfoOnly', response.data.user)
                this.commit('updateManagerInfoOnly', response.data)
                this.state.isAuthenticated = true
                this.dispatch('loadOrganization')
                router.push('home')
            })
            // Catch errors
            .catch(error => {
                console.log(error)
            })
        },

        // To set the user's organization after initial login
        setUserOrganization(context, orgId){
            this.commit('setUserOrganization', orgId)
            this.dispatch('loadOrganization')
        },

        // Load all Organization's information
        loadOrganization(){
            // Get all information on the organization from backend
            axios({
                method: 'get',
                url: `${this.getters.endpoints.baseAPI}/organizationsall/${this.getters.user.organization}`,
                headers: {
                    authorization: `Bearer ${this.getters.accessToken}`
                }
            })
            .then(response => this.commit('setOrganization', response.data))
            .catch(error => console.log(error))
        }

    },    // end Vuex actions
    modules: {

    },    // end Vuex modules
})
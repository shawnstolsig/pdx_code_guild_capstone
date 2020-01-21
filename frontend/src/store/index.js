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
    jwt: localStorage.getItem('t'),
    endpoints: {
      obtainJWT: 'http://0.0.0.0:8000/api/v1/token/obtain',
      refreshJWT: 'http://0.0.0.0:8000/api/v1/token/refresh'
    }
  },

  mutations: {
    updateToken(state, newToken) {
      localStorage.setItem('t', newToken);
      state.jwt = newToken;
    },
    removeToken(state) {
      localStorage.removeItem('t');
      state.jwt = null;
    }
  },

  actions: {
    obtainToken(username, password) {
      const payload = {
        username: username,
        password: password
      }

      axios.post(this.state.endpoints.obtainJWT, payload)
      .then((response) => {
          this.commit('updateToken', response.data.token);
        })
        .catch((error) => {
          console.log(error);
        })
    },
    refreshToken() {
      const payload = {
        token: this.state.jwt
      }

      axios.post(this.state.endpoints.refreshJWT, payload)
      .then((response) => {
          this.commit('updateToken', response.data.token)
        })
        .catch((error) => {
          console.log(error)
        })
      },
    inspectToken() {
      const token = this.state.jwt;
      if (token) {
        const decoded = jwt_decode(token);
        const exp = decoded.exp
        const orig_iat = decoded.orig_iat
        
        if (exp - (Date.now() / 1000) < 1800 && (Date.now() / 1000) - orig_iat < 628200) {
          this.dispatch('refreshToken')
        } else if (exp - (Date.now() / 1000) < 1800) {
          // DO NOTHING, DO NOT REFRESH   
          alert("token inspected, no issues")
        } else {
          // PROMPT USER TO RE-LOGIN
          // THIS ELSE CLAUSE COVERS THEN CONDITION WHERE A TOKEN IS EXPIRED
          alert("token inspection failed (expired), please login again!")
        }
      }
    }
  },
  
  modules: {

  }
})
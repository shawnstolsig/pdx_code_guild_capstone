<template>
  <div class="jwt-test">
    <v-container fluid>
      <h1>JSON Web Token Test</h1>
      <input v-model="username" placeholder="username here..." />
      <input v-model="password" placeholder="password here..." />
      <v-btn @click="getToken">Get token from Django backend</v-btn>
      <v-btn @click="deleteToken">Remove token from Vue frontend</v-btn>
      <h3>Access token:</h3>
      <p>{{access}}</p>
      <h3>Refresh token:</h3>
      <p>{{refresh}}</p>
      <v-btn @click="inspectToken">Inspect token</v-btn>
      <v-btn @click="refreshToken">Refresh token</v-btn>
      <v-btn @click="testAPI">Test Protected Django API</v-btn>
    </v-container>
  </div>
</template>

<script>
import axios from 'axios'

export default {
  name: "jwtTest",
  components: {},
  data() {
    return {
      username: null,
      password: null
    };
  },
  methods: {
    getToken() {
      // call state obtain token here
      const payload = {
        username: this.username,
        password: this.password
      };
      this.$store.dispatch("obtainToken", payload);
	},
	refreshToken(){
		this.$store.dispatch("refreshToken");
	},
    inspectToken() {
      this.$store.dispatch("inspectToken");
    },
    deleteToken() {
      this.$store.dispatch("deleteToken");
	},
	testAPI() {
		axios({
			method: 'get',
			url: 'http://localhost:8000/api/v1/hello',
			headers: {
				authorization: `Bearer ${this.access}`
			}
		}).then(response => alert(response.data.message))
		.catch((error) => {
			alert("Error with request...not authenticated");
			console.log(error);
		})
	}
  },
  computed: {
    access() {
      return this.$store.state.jwt_access;
    },
    refresh() {
      return this.$store.state.jwt_refresh;
    }
  }
};
</script>

<template>
  <div class="home">
    <h1>JWT Test</h1>
    <input v-model="username" placeholder='username here...'/>
    <input v-model="password" placeholder='password here...'/>
    <v-btn @click="getToken">Click to get token from Django backend</v-btn>
    <p>{{token}}</p>
  </div>
</template>

<script>

export default {
  name: 'home',
  components: {

  },
  data(){
    return{
      token: null,
      username: null,
      password: null
    }
  },
  methods: {
    getToken(){
      // call state obtain token here
    }
  },

}
</script>

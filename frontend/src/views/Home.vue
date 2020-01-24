<template>
  <div class="home">
    <h1>Home page</h1>
  </div>
</template>

<script>

export default {
  name: 'home',
  components: {}, 
  mounted(){
    this.$vuetify.theme.dark = this.$store.getters.user.darkModeEnabled
  }
}
</script>

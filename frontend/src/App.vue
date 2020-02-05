<template>
  <v-app :style="{background: $vuetify.theme.themes[theme].background}">
    <Navbar/>
    <v-content >
      <router-view></router-view>
    </v-content>
  </v-app>
</template>

<script>
import Navbar from '@/components/Navbar'

export default {
	name: 'App',

	components: {
		Navbar
	},

	data: () => ({
		//
	}),

	created(){
		this.$store.dispatch('tryAutoLogin')
	},

	computed:{
			theme(){
				return (this.$vuetify.theme.dark) ? 'dark' : 'light'
			}
	}
};
</script>

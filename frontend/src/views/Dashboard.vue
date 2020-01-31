<template>
	<v-container fluid class="fill-height">
			<FloatingCard v-for="node in workspace.workspace_nodes" :key="node.id" :nodeProp="node"></FloatingCard>
			<FloatingButton />		
	</v-container>
</template>

<script>
import FloatingButton from '@/components/workspace/FloatingButton.vue'
import FloatingCard from '@/components/workspace/FloatingCard.vue'
import axios from 'axios'

export default {
	name: 'dashboard',
	components: {
		FloatingButton,
		FloatingCard,
	}, 

	data(){
		return {

		}
	},    // end data


	methods: {

	},    // end methods


	computed: {
		org(){
			return this.$store.getters.organization
		},
		rules(){
				return this.$store.getters.formRules
		},
		workspace(){
			return this.$store.getters.workspace
		},
	},     // end computed

	mounted(){

		// set light/dark mode
		this.$vuetify.theme.dark = this.$store.getters.user.darkModeEnabled

		// load the first workspace if none is loaded
		if(this.$store.getters.user.preferredWorkspaceKey == undefined){
			// load workspace data
			this.$store.dispatch('loadWorkspace', {index: 0})
		} 
		
		// load user's preferred workspace (which is the same as the last one they visited)
		else {
			// this.$store.dispatch('loadWorkspace', {key: this.$store.getters.workspace.id})
			this.$store.dispatch('loadWorkspace', {key: this.$store.getters.user.preferredWorkspaceKey})
		}

	},		// end of mounted

	destroyed(){
		// update state with preferred workspace dashboard
		this.$store.dispatch('updateStoreWorkspace', this.$store.getters.workspace.id)

		// store last visited workspace
		axios({
			method: 'patch',
			url: `${this.$store.getters.endpoints.baseAPI}/managers/${this.$store.getters.user.userId}/`,
			data: {
				preferred_workspace_key: this.$store.getters.workspace.id
			},
			headers: {
				authorization: `Bearer ${this.$store.getters.accessToken}`
			},
		})
		.then(response => {
			console.log("Stored preferred user workspace: ")
			console.log(response)
		})
		.catch(error => {console.log(error)})



		this.$store.dispatch('dismountWorkspace')
	}, 		// end of destroyed
	     
}
</script>

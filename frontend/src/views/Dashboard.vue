<template>
	<v-container fluid class="fill-height">
			<FloatingCard v-for="node in workspace.workspace_nodes" :key="node.id" :nodeProp="node"></FloatingCard>
			<FloatingButton />		
	</v-container>
</template>

<script>
import FloatingButton from '@/components/workspace/FloatingButton.vue'
import FloatingCard from '@/components/workspace/FloatingCard.vue'

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
		if(this.$store.getters.workspace.id == undefined){
			console.log("should be here for no workspace loaded")
			// load workspace data
			this.$store.dispatch('loadWorkspace', {index: 0})
		} 
		// reload the same workspace if previously loaded
		else {
			this.$store.dispatch('loadWorkspace', {key: this.$store.getters.workspace.id})
		}
	}     // end mounted
}
</script>

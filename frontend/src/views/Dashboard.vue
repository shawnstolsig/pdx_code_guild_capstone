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
			// testNode: {
			// 	name: "Station 2-1",
			// 	draggable: true,
			// 	x: 300,
			// 	y: 500,
			// 	role: {
			// 		name: 'Grading',
			// 		color: 'blue',
			// 	},
			// 	worker: {
			// 		full_name: "Joe Dirt",
			// 		cohort: {
			// 			name: "DA1",
			// 			color: "red",
			// 		}
			// 	},
			// }
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

		// load workspace data
		this.$store.dispatch('loadWorkspace', 1)
	}     // end mounted
}
</script>

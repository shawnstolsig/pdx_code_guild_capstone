<template>
	<v-container fluid class="fill-height">
			<FloatingCard x="100" y="200" :node="testNode"></FloatingCard>
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
			testNode: {
				name: "Station 2-1",
				role: {
					name: 'Grading',
					color: 'blue',
				},
				worker: {
					full_name: "Joe Dirt",
					cohort: {
						name: "DA1",
						color: "red",
					}
				},
			}
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
	},     // end computed


	mounted(){
		this.$vuetify.theme.dark = this.$store.getters.user.darkModeEnabled
	}     // end mounted
}
</script>

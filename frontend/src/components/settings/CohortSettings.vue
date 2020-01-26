<template>
    <v-card>
        <v-card-title>
            Cohorts
        </v-card-title>
        <v-card-text>
            <v-list>

                <v-list-item v-for="cohort in org.org_cohorts" :key="cohort.id">
                    <v-list-item-content>
                        <v-list-item-title>{{cohort.name}}</v-list-item-title>
                    </v-list-item-content>
                </v-list-item>
                <v-list-item v-if="org.org_cohorts.length == 0">
                    <v-list-item-content>
                        <v-list-item-title class="grey--text">(none)</v-list-item-title>
                    </v-list-item-content>
                </v-list-item>


            </v-list>
        </v-card-text>
        <v-card-actions>
            <!-- Dialog for adding Cohort -->
            <v-dialog v-model="cohortDialog" max-width="500">
                <template v-slot:activator="{ on }">
                    <v-btn v-on="on">Add</v-btn>
                </template>
                <v-card class="pa-3">
                    <v-card-title>Create New Cohort</v-card-title>
                    <v-card-subtitle class="mt-1">Please type in a name and description for your cohort.</v-card-subtitle>
                    <v-form v-model="cohortCreateFormValidity" ref="cohortCreateForm">
                        <v-card-text>
                                <v-text-field
                                    v-model="newCohort.name"
                                    :rules="rules.name"
                                    type="text"
                                    label="Name"
                                    required
                                ></v-text-field>
                                <v-textarea
                                    solo
                                    v-model="newCohort.description"
                                    :rules="rules.description"
                                    label="Description"
                                    required
                                ></v-textarea>
                        </v-card-text>
                        <v-card-actions>
                                <v-btn @click.prevent="addCohort" :disabled="!cohortCreateFormValidity" class="my-3 mr-3">Add</v-btn>  
                        </v-card-actions>
                    </v-form>
                </v-card>
            </v-dialog>

        </v-card-actions>
    </v-card>
</template>

<script>
import axios from 'axios'

export default {
	data: () => ({
		// Cohort create form/dialog vars
		cohortDialog: false,
		cohortCreateFormValidity: false,
		newCohort: {
			name: '',
			description: '',
		},
	}),     // end data

	methods: {
		// Create a department on button press from Organization Settings tab
		addCohort(){
			console.log("creating cohort")
			axios({
				method: 'post',
				url: `${this.$store.getters.endpoints.baseAPI}/cohorts/`,
				data: {
					name: this.newCohort.name,
					description: this.newCohort.description,
					organization: this.$store.getters.organization.id
				},
				headers: {
					authorization: `Bearer ${this.$store.getters.accessToken}`
				},
			})
			.then(response => {
				console.log(response)
				// reload organization
				this.$store.dispatch('loadOrganization')
				this.cohortDialog = false
			})
			.catch(error => {console.log(error)})
		},
	},      /// end methods	

	computed: {			
		org(){
			return this.$store.getters.organization
        },
        rules(){
            return this.$store.getters.formRules
        },
	},		// end computed

	created() {
	},		// end mounted
}
</script>
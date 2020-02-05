<template>
    <!-- Cohort settings is subcomponent of OrgSettings -->
    <v-card>
        <v-card-title>
            Cohorts
        </v-card-title>
        <v-card-text>

            <!-- List of exisiting cohorts -->
            <v-list>
                <v-list-item-group v-model="selectedCohort">
                    <v-list-item v-for="cohort in org.org_cohorts" :key="cohort.id">
                        <v-list-item-content>
                            <v-list-item-title>{{cohort.name}}</v-list-item-title>
                        </v-list-item-content>
                        <v-list-item-action>
                            <v-chip :color="cohort.color" label></v-chip>
                        </v-list-item-action>
                    </v-list-item>
                </v-list-item-group>
                <v-list-item v-if="org.org_cohorts.length == 0">
                    <v-list-item-content>
                        <v-list-item-title class="grey--text">(none)</v-list-item-title>
                    </v-list-item-content>
                </v-list-item>


            </v-list>
        
        </v-card-text>
        <v-card-actions>

            <!-- Dialog for adding Cohort -->
            <v-dialog v-model="cohortCreateDialog" max-width="500">
                <template v-slot:activator="{ on }">
                    <v-btn color="primary" v-on="on">Add</v-btn>
                </template>
                <v-card class="pa-3">
                    <v-card-title>Create New Cohort</v-card-title>
                    <v-card-subtitle class="mt-1">Please type in a name and description for your cohort.</v-card-subtitle>
                    <v-form v-model="cohortCreateFormValidity" ref="cohortCreateForm">
                        <v-card-text>
                            <v-container>
                                <v-row>
                                    <v-col cols="6">
                                        <v-text-field
                                            v-model="newCohort.name"
                                            :rules="rules.name"
                                            type="text"
                                            label="Name"
                                            required
                                        ></v-text-field>
                                    </v-col>
                                    <v-col cols="6">
                                        <v-menu top nudge-bottom="105" nudge-left="16" :close-on-content-click="false">
                                            <template v-slot:activator="{ on }">
                                                <v-chip v-on="on" :color="newCohort.color" x-large label>Color...</v-chip>
                                            </template>
                                            <v-card>
                                                <v-card-text class="pa-0">
                                                    <v-color-picker v-model="newCohort.color" hide-inputs hide-mode-switch show-swatches />
                                                </v-card-text>
                                                </v-card>
                                        </v-menu>
                                    </v-col>
                                </v-row>
                                <v-row>
                                    <v-col cols="12">
                                        <v-textarea
                                            solo
                                            v-model="newCohort.description"
                                            :rules="rules.description"
                                            label="Description"
                                            required
                                        ></v-textarea>
                                    </v-col>
                                </v-row>
                            </v-container>
                        </v-card-text>
                        <v-card-actions>
                            <v-spacer></v-spacer>
                            <v-btn 
                                @click.prevent="cohortCreateDialog = false" 
                                color="error"
                                text 
                                class="my-3 mr-3"
                                >Cancel
                            </v-btn>  
                            <v-btn 
                                @click.prevent="addCohort" 
                                :disabled="!cohortCreateFormValidity"
                                color="success"
                                text 
                                class="my-3 mr-3"
                                >Add
                            </v-btn>  
                        </v-card-actions>
                    </v-form>
                </v-card>
            </v-dialog>

            <!-- Dialog for deleting Cohort -->
            <v-dialog v-model="cohortDeleteDialog" max-width="500" v-if="selectedCohort >= 0">
                <template v-slot:activator="{ on }">
                    <v-btn v-on="on">Delete</v-btn>
                </template>
                <v-card class="pa-3">
                    <v-card-title>Delete Cohort?</v-card-title>
                    <v-card-subtitle class="mt-1">Are you sure you want to delete this cohort?</v-card-subtitle>
                    <v-card-actions>
                            <v-btn @click="deleteCohort" class="my-3 mr-3">Yes</v-btn>  
                            <v-btn @click="cohortDeleteDialog = false" class="my-3 mr-3">No</v-btn>  
                    </v-card-actions>
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
        cohortCreateDialog: false,
        cohortDeleteDialog: false,
        cohortCreateFormValidity: false,
        selectedCohort: undefined,
		newCohort: {
			name: '',
            description: '',
            color: '#add8e6',
		},
	}),     // end data

	methods: {

		// Create a department on button press from Organization Settings tab
		addCohort(){

            // Trim whitespace
            this.newCohort.name = this.newCohort.name.trim()

            // Check to make sure there isn't already a department with that name
            for (let i = 0; i < this.org.org_cohorts.length; i++){
                if(this.newCohort.name == this.org.org_cohorts[i].name){
                    alert("Organization already has a cohort with that name.\n Please pick a new cohort name.")
                    return
                }
            }

            // Write cohort to db
			axios({
				method: 'post',
				url: `${this.$store.getters.endpoints.baseAPI}/cohorts/`,
				data: {
					name: this.newCohort.name,
					description: this.newCohort.description,
                    organization: this.$store.getters.organization.id,
                    color: this.newCohort.color,
				},
				headers: {
					authorization: `Bearer ${this.$store.getters.accessToken}`
				},
			})
			.then(response => {
				console.log(response)
				// reload organization
				this.$store.dispatch('loadOrganization')
                this.cohortCreateDialog = false
                this.newCohort = {
                    name: '',
                    description: '',
                    color: '#add8e6',
                }
			})
			.catch(error => {console.log(error)})
        },
        
        // Delete a Cohort
        deleteCohort(){

            // Look up dept id.  Names must be unique when created, so looking up by name is reliable.
            let cohortId = this.org.org_cohorts[this.selectedCohort].id

            // Delete cohort in db
            axios({
                method: 'delete',
                url: `${this.$store.getters.endpoints.baseAPI}/cohorts/${cohortId}`,
                headers: {
                    authorization: `Bearer ${this.$store.getters.accessToken}`
                },
            })
            .then(response => {
                console.log(response)
                this.$store.dispatch('loadOrganization')
                this.selectedCohort = undefined
                this.cohortDeleteDialog = false
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
}
</script>
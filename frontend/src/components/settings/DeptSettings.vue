<template>
    <v-card>
        <v-card-title>
            Departments
        </v-card-title>
        <v-card-text>
            <v-list>
                <v-list-item v-for="department in org.org_departments" :key="department.id">
                    <v-list-item-content>
                        <v-list-item-title>{{department.name}}</v-list-item-title>
                    </v-list-item-content>
                </v-list-item>
                <v-list-item v-if="org.org_departments.length == 0">
                    <v-list-item-content>
                        <v-list-item-title class="grey--text">(none)</v-list-item-title>
                    </v-list-item-content>
                </v-list-item>
            </v-list>
        </v-card-text>
        <v-card-actions>
            <!-- Dialog for adding Department -->
            <v-dialog v-model="deptDialog" max-width="500">
                <template v-slot:activator="{ on }">
                    <v-btn v-on="on">Add</v-btn>
                </template>
                <v-card class="pa-3">
                    <v-card-title>Create New Department</v-card-title>
                    <v-card-subtitle class="mt-1">Please type in a name and description for your department.</v-card-subtitle>
                    <v-form v-model="deptCreateFormValidity" ref="deptCreateForm">
                        <v-card-text>
                                <v-text-field
                                    v-model="newDept.name"
                                    :rules="rules.name"
                                    type="text"
                                    label="Name"
                                    required
                                ></v-text-field>
                                <v-textarea
                                    solo
                                    v-model="newDept.description"
                                    :rules="rules.description"
                                    label="Description"
                                    required
                                ></v-textarea>
                        </v-card-text>
                        <v-card-actions>
                                <v-btn @click.prevent="addDepartment" :disabled="!deptCreateFormValidity" class="my-3 mr-3">Add</v-btn>  
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
		// Dept create form/dialog vars
		deptDialog: false,
		deptCreateFormValidity: false,
		newDept: {
			name: '',
			description: '',
		},
	}),     // end data

	methods: {

		// Create a department on button press from Organization Settings tab
		addDepartment(){
			console.log("creating dept")
			axios({
				method: 'post',
				url: `${this.$store.getters.endpoints.baseAPI}/departments/`,
				data: {
					name: this.newDept.name,
					description: this.newDept.description,
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
				this.deptDialog = false
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

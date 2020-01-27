<template>
    <v-card>
        <v-card-title>
            Departments
        </v-card-title>
        <v-card-text>
            <v-list >
                <v-list-item-group v-model="selectedDept">
                    <v-list-item v-for="department in org.org_departments" :key="department.id">
                        <v-list-item-content>
                            <v-list-item-title>{{department.name}}</v-list-item-title>
                        </v-list-item-content>
                    </v-list-item>
                </v-list-item-group>
                <v-list-item v-if="org.org_departments.length == 0">
                    <v-list-item-content>
                        <v-list-item-title class="grey--text">(none)</v-list-item-title>
                    </v-list-item-content>
                </v-list-item>
            </v-list>
        </v-card-text>
        <v-card-actions>
            <!-- Dialog for adding Department -->
            <v-dialog v-model="deptCreateDialog" max-width="500">
                <template v-slot:activator="{ on }">
                    <v-btn color="primary" v-on="on">Add</v-btn>
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
                            <v-spacer></v-spacer>
                            <v-btn 
                                @click.prevent="deptCreateDialog = false" 
                                color="error"
                                text 
                                class="my-3 mr-3"
                                >Cancel
                            </v-btn>  
                            <v-btn 
                                @click.prevent="addDepartment" 
                                :disabled="!deptCreateFormValidity" 
                                class="my-3 mr-3"
                                color="success"
                                text 
                                >Add
                            </v-btn>  
                        </v-card-actions>
                    </v-form>
                </v-card>
            </v-dialog>
            <!-- Dialog for deleting Department -->
            <v-dialog v-model="deptDeleteDialog" max-width="500" v-if="selectedDept >= 0">
                <template v-slot:activator="{ on }">
                    <v-btn v-on="on">Delete</v-btn>
                </template>
                <v-card class="pa-3">
                    <v-card-title>Delete Department?</v-card-title>
                    <v-card-subtitle class="mt-1">Are you sure you want to delete this department?</v-card-subtitle>
                    <v-card-actions>
                            <v-btn @click="deleteDepartment" class="my-3 mr-3">Yes</v-btn>  
                            <v-btn @click="deptDeleteDialog = false" class="my-3 mr-3">No</v-btn>  
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
		// Dept create form/dialog vars
        deptCreateDialog: false,
        deptDeleteDialog: false,
        deptCreateFormValidity: false,
        selectedDept: undefined,
		newDept: {
			name: '',
			description: '',
		},
	}),     // end data

	methods: {

		// Create a department on button press from Organization Settings tab
		addDepartment(){

            // Trim whitespace
            this.newDept.name = this.newDept.name.trim()

            // Check to make sure there isn't already a department with that name
            for (let i = 0; i < this.org.org_departments.length; i++){
                if(this.newDept.name == this.org.org_departments[i].name){
                    alert("Organization already has a department with that name.\n Please pick a new department name.")
                    return
                }
            }

            console.log("Creating department.")
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
                this.deptCreateDialog = false
                this.newDept = {
                    name: '',
                    description: '',
                }
            })
            .catch(error => {console.log(error)})
        },
        
        // Delete a department
        deleteDepartment(){
            
            // Look up dept id.  Names must be unique when created, so looking up by name is reliable.
            let deptId = this.org.org_departments[this.selectedDept].id
  
            console.log("deleting dept")
            axios({
                method: 'delete',
                url: `${this.$store.getters.endpoints.baseAPI}/departments/${deptId}`,
                headers: {
                    authorization: `Bearer ${this.$store.getters.accessToken}`
                },
            })
            .then(response => {
                console.log(response)
                this.$store.dispatch('loadOrganization')
                this.selectedDept = undefined
                this.deptDeleteDialog = false
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
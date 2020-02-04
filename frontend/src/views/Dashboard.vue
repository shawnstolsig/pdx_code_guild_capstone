<template>
	<v-container class="fill-height" fluid color='red'>
		<FloatingZone v-for="zone in workspace.workspace_zones" :key="'zone'+zone.id" :zoneProp="zone"></FloatingZone>
		<FloatingCard v-for="node in workspace.workspace_nodes" :key="'node'+node.id" :nodeProp="node"></FloatingCard>
		<FloatingButton />		

				<!-- Create workspace dialog -->
		<v-dialog v-model="createWorkspaceDialog" max-width="500px" persistent>
			<v-card>
				<v-card-title>
					Create a workspace
				</v-card-title>
				<v-card-text>
					<v-container>
						<v-form v-model="createWorkspaceFormValid">
							<v-row>
								<v-col cols="6">
									<v-text-field 
										v-model="newWorkspace.name" 
										label="Name"
										:rules="rules.name"
										required
									></v-text-field>
								</v-col>
								<v-col cols="6">
									<v-select 
										:items="departments" 
										label="Department" 
										v-model="newWorkspace.department"
										required
									></v-select>
								</v-col>
							</v-row>
							<v-row>
								<v-col cols="12">
									<v-textarea
										solo
										v-model="newWorkspace.description"
										:rules="rules.description"
										label="Description"
										required
									></v-textarea>
								</v-col>
							</v-row>
						</v-form>
					</v-container>
				</v-card-text>
				<v-card-actions>
					<v-spacer></v-spacer>
					<v-btn 
						color="error" 
						text 
						@click="redirectToSettings"
					>Cancel</v-btn>
					<v-btn 
						color="success" 
						text 
						:disabled="!(createWorkspaceFormValid && !!newWorkspace.department)" 
						@click="createWorkspace"
					>Save</v-btn>
				</v-card-actions>
			</v-card>
		</v-dialog>

	</v-container>
</template>

<script>
import FloatingButton from '@/components/workspace/FloatingButton.vue'
import FloatingCard from '@/components/workspace/FloatingCard.vue'
import FloatingZone from '@/components/workspace/FloatingZone.vue'

import axios from 'axios'
// import VueDraggableResizable from 'vue-draggable-resizable'

export default {
	name: 'dashboard',
	components: {
		FloatingButton,
		FloatingCard,
		FloatingZone,
		// VueDraggableResizable,
		
	}, 

	data(){
		return {
			// for creating workspace
			createWorkspaceDialog: false,
			createWorkspaceFormValid: false,
			newWorkspace: {
				name: '',
				description: '',
				department: '',
			},
		}
	},    // end data


	methods: {
		createWorkspace(){
            // get department id from string that's been selected
            let deptId;
            for(let dept of this.$store.getters.organization.org_departments){
                if(dept.name == this.newWorkspace.department){
                    deptId = dept.id
                }
            }
            // post new workspace to db
            axios({
                method: 'post',
                url: `${this.$store.getters.endpoints.baseAPI}/workspaces/`,
                data: {
                    name: this.newWorkspace.name,
                    description: this.newWorkspace.description,
                    department: deptId,
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
                
                // automatically reload workspace 
                setTimeout(() => {
                    this.$store.dispatch('loadWorkspace', {key: response.data.id})
                }, 300)
    
                // reset newWorkspace (mainly for the form)
                this.newWorkspace = {
                    name: '',
                    description: '',
                    department: '',
				}
				
				// close dialog
				this.createWorkspaceDialog = false
            })
            .catch(error => {console.log(error)})
		},
		// Send to settings if they cancel out of creating workspace
		redirectToSettings(){
			this.$router.push({name: "settings"})
		},
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
		departments(){
            let returnArray = []
            this.$store.getters.organization.org_departments.map(x => returnArray.push(x.name))
            return returnArray
        },
	},     // end computed

	mounted(){

		// set light/dark mode
		this.$vuetify.theme.dark = this.$store.getters.user.darkModeEnabled

		// check to see if no workspaces exist
		if(this.$store.getters.organization.org_workspaces.length == 0){
			this.createWorkspaceDialog = true
		}

		// load the first workspace if none is loaded
		if(this.$store.getters.user.preferredWorkspaceKey == undefined){
			// load workspace data
			this.$store.dispatch('loadWorkspace', {index: 0})
		} 
		
		// load user's preferred workspace (which is the same as the last one they visited)
		else {
			// this.$store.dispatch('loadWorkspace', {key: this.$store.getters.workspace.id})
			// console.log(`LOADING WORKSPACE ${this.$store.getters.user.preferredWorkspaceKey}`)
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

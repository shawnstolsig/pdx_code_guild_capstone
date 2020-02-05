<template>
    <v-container class="fill-height" fluid>

        <!-- This is the floating button/speed dial on the dashboard -->
        <v-speed-dial
            v-model="fab"
            bottom
            right

            direction="top"
            transition="slide-y-reverse-transition"
            >
            <template v-slot:activator>
                <v-btn v-model="fab" color="#FF0000" dark fab>
                    <v-icon v-if="fab">mdi-close</v-icon>
                    <v-icon v-else>dashboard</v-icon>
                </v-btn>
            </template>

            <!-- Below are the five buttons that slide out of speed dial, with tooltips -->
            <v-tooltip right>
                <template v-slot:activator="{ on }">
                    <v-btn fab dark small color="#ff7f00" v-on="on" @click="createNodeDialog = true">
                        <v-icon>mdi-pencil</v-icon>
                    </v-btn>
                </template>
                <span>Create Workstation</span>
            </v-tooltip>

            <v-tooltip right>
                <template v-slot:activator="{ on }">
                    <v-btn fab dark small color="#228b22" v-on="on" @click="createZoneDialog = true">
                        <v-icon>tab_unselected</v-icon>
                    </v-btn>
                </template>
                <span>Create Zone</span>
            </v-tooltip>

            <v-tooltip right>
                <template v-slot:activator="{ on }">
                    <v-btn fab dark small color="#0000FF"  v-on="on" @click="navDrawer = !navDrawer">
                        <v-icon>vertical_split</v-icon>
                    </v-btn>
                </template>
                <span>Toggle Sidebar</span>
            </v-tooltip>

            <v-tooltip right>
                <template v-slot:activator="{ on }">
                    <v-btn fab dark small color="#4B0082" v-on="on" @click="changeWorkspaceDialog = true">
                        <v-icon>view_carousel</v-icon>
                    </v-btn>
                </template>
                <span>Change Workspace</span>
            </v-tooltip>

            <v-tooltip right>
                <template v-slot:activator="{ on }">
                    <v-btn fab dark small color="#9400D3" v-on="on" @click="createWorkspaceDialog = true">
                        <v-icon>mdi-plus</v-icon>
                    </v-btn>
                </template>
                <span>Create Workspace</span>
            </v-tooltip>

        </v-speed-dial>

        <!-- Change workspace dialog -->
        <v-dialog v-model="changeWorkspaceDialog" max-width="500px">
            <v-card>
                <v-card-title>
                    Please select workspace
                </v-card-title>
                <v-card-text>
                    <v-chip 
                        v-for="(workspace, index) in org.org_workspaces" 
                        :key="workspace.id" 
                        @click="switchWorkspace(index)"
                        class='ma-2'
                        :color="workspace.id == currentWorkspaceId ? 'light-green' : 'grey lighten-2'"
                        >
                        <v-avatar left>{{index+1}}</v-avatar>{{workspace.name}}<br>
                    </v-chip>
                
                </v-card-text>
            </v-card>
        </v-dialog>
        
        <!-- Create workspace dialog -->
        <v-dialog v-model="createWorkspaceDialog" max-width="500px">
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
                        @click="createWorkspaceDialog = false"
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

        <!-- Create node dialog -->
        <v-dialog v-model="createNodeDialog" max-width="500px">
            <v-card>
                <v-card-title>
                    Create a workstation
                </v-card-title>
                <v-card-text>
                    <v-container>
                        <v-form v-model="createNodeFormValid">
                            <v-row>
                                <v-col cols="6">
                                    <v-text-field 
                                        v-model="newNode.name" 
                                        label="Name"
                                        :rules="rules.workstationName"
                                        required
                                    ></v-text-field>
                                </v-col>
                                <v-col cols="6">
                                    <v-select 
                                        :items="roles" 
                                        label="Role" 
                                        v-model="newNode.role"
                                        required
                                    ></v-select>
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
                        @click="createNodeDialog = false"
                    >Cancel</v-btn>
                    <v-btn 
                        color="success" 
                        text 
                        :disabled="!(createNodeFormValid && !!newNode.role)" 
                        @click="createNode"
                    >Save</v-btn>
                </v-card-actions>
            </v-card>
        </v-dialog>

        <!-- Create zone dialog -->
        <v-dialog v-model="createZoneDialog" max-width="500px">
            <v-card>
                <v-card-title>
                    Create a zone
                </v-card-title>
                <v-card-text>
                    <v-container>
                        <v-form v-model="createZoneFormValid">
                            <v-row>
                                <v-col cols="6">
                                    <v-text-field 
                                        v-model="newZone.name" 
                                        label="Name"
                                        :rules="rules.workstationName"
                                        required
                                    ></v-text-field>
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
                        @click="createZoneDialog = false"
                    >Cancel</v-btn>
                    <v-btn 
                        color="success" 
                        text 
                        :disabled="!(createZoneFormValid)" 
                        @click="createZone"
                    >Save</v-btn>
                </v-card-actions>
            </v-card>
        </v-dialog>

        <!-- Workforce navigation drawer -->
		<v-navigation-drawer
			v-model="navDrawer"
			app
			clipped
			right
			>
			<v-list>
                <v-list-item>
                    <v-list-item-title class="title">
                        Unassigned Workers
                    </v-list-item-title>
                </v-list-item>
                <v-divider></v-divider>
                <!-- Cohorts Nested List -->
                <v-list-group
                    prepend-icon="group"
                >
                    <template v-slot:activator>
                    <v-list-item-title>Cohorts</v-list-item-title>
                    </template>

                    <v-list-group
                    no-action
                    sub-group
                    v-for="cohort in org.org_cohorts"
                    :key="cohort.id"
                    >
                        <template v-slot:activator>
                            <v-list-item-content>
                            <v-list-item-title>{{`${cohort.name} (${cohortUnassigned(cohort.id).length})`}}</v-list-item-title>
                            </v-list-item-content>
                        </template>

                        <v-list-item
                            v-for="worker in cohortUnassigned(cohort.id)"
                            :key="worker.id"
                            link
                        >
                            <v-list-item-title v-text="worker.full_name"></v-list-item-title>
                            <!-- <v-list-item-icon>
                            <v-icon v-text="admin[1]"></v-icon>
                            </v-list-item-icon> -->
                        </v-list-item>
                    </v-list-group>

                </v-list-group>
                
                <!-- Roles Nested List -->
                <v-list-group
                    prepend-icon="transfer_within_a_station"
                >
                    <template v-slot:activator>
                    <v-list-item-title>Roles</v-list-item-title>
                    </template>

                    <v-list-group
                    sub-group
                    no-action
                    v-for="role in org.org_roles"
                    :key="role.id"
                    >
                        <template v-slot:activator>
                            <v-list-item-content>
                            <v-list-item-title>{{`${role.name} (${roleUnassigned(role).length})`}}</v-list-item-title>
                            </v-list-item-content>
                        </template>
                        <v-list-item
                            v-for="worker in roleUnassigned(role)"
                            :key="worker.id"
                            
                        >
                            <v-list-item-title v-text="worker.full_name"></v-list-item-title>
                            <!-- <v-list-item-action>
                            <v-icon v-text="crud[1]"></v-icon>
                            </v-list-item-action> -->
                        </v-list-item>
                    </v-list-group>
                </v-list-group>
                <v-divider></v-divider>

                <v-list-group
                    multiple
                    >
                    <template v-slot:activator>
                        <v-list-item-content>
                            <v-list-item-title class="title">Active Cohorts</v-list-item-title>
                        </v-list-item-content>
                    </template>

                    <v-list-item
                        v-for="cohort in org.org_cohorts"
                        :key="cohort.id"
                    
                    >

                        <v-list-item-action>
                            <v-checkbox
                            v-model="cohort.is_active"
                            color="primary"
                            @click="toggleCohort(cohort)"
                            ></v-checkbox>
                        </v-list-item-action>
                        <v-list-item-content>
                            <v-list-item-title>{{`${cohort.name}`}}</v-list-item-title>
                        </v-list-item-content>
                    
                        <v-list-item-icon>
                            <v-chip :color="cohort.color" label class="py-0"></v-chip>
                        </v-list-item-icon>
                    </v-list-item>
                </v-list-group>
                <v-divider></v-divider>

                <!-- Placeholder for adding "auto fill" button -->
                <!-- <v-list-item>
                        <v-btn color='success' @click="" center>
                            Fill Workstations
                        </v-btn>
                </v-list-item>
                <v-divider></v-divider> -->

                <v-list-item>
                        <v-btn color='error' @click="clearWorkspaceNodes">
                            Clear Workstations
                        </v-btn>
                </v-list-item>
			</v-list>
		</v-navigation-drawer>

    </v-container>
</template>
<script>
import axios from 'axios'
export default {

    data: () => ({
		fab: false,
        // for changing workspace
        changeWorkspaceDialog: false,
        // for creating workspace
        createWorkspaceDialog: false,
        createWorkspaceFormValid: false,
        newWorkspace: {
            name: '',
            description: '',
            department: '',
        },
        // for creating node
        createNodeDialog: false,
        createNodeFormValid: false,
        newNode: {
            name: '',
            role: '',
        },
        // for creating zone
        createZoneDialog: false,
        createZoneFormValid: false,
        newZone: {
            name: '',
        },
        // for nav drawer
        navDrawer: true,
        activeCohorts: [1,2],
    }),		// end of data

    methods: {

        // creates a node/workstation.
        createNode(){
            // get role id from string that's been selected
            let roleId;
            for(let role of this.$store.getters.organization.org_roles){
                if(role.name == this.newNode.role){
                    roleId = role.id
                    console.log(`role id is ${roleId}`)
                }
            }
            // post new db to db
            axios({
                method: 'post',
                url: `${this.$store.getters.endpoints.baseAPI}/nodecreate/`,
                data: {
                    name: this.newNode.name,
                    role: roleId,
                    organization: this.$store.getters.organization.id,
                    workspace: this.$store.getters.workspace.id,
                    department: this.$store.getters.workspace.department,
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
                    this.$store.dispatch('loadWorkspace', {key: this.$store.getters.workspace.id})
                }, 300)
    
                // reset newWorkspace (mainly for the form)
                this.newNode = {
                    name: '',
                    role: '',
                }

            })
            .catch(error => {console.log(error)})

            this.createNodeDialog = false
        },

        // creates a zone
        createZone(){

            // post new db to db
            axios({
                method: 'post',
                url: `${this.$store.getters.endpoints.baseAPI}/zones/`,
                data: {
                    name: this.newZone.name,
                    organization: this.$store.getters.organization.id,
                    workspace: this.$store.getters.workspace.id,
                    department: this.$store.getters.workspace.department,
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
                    this.$store.dispatch('loadWorkspace', {key: this.$store.getters.workspace.id})
                }, 300)
    
                // reset newWorkspace (mainly for the form)
                this.newZone = {
                    name: '',
                }

            })
            .catch(error => {console.log(error)})

            this.createZoneDialog = false
        },

        // switches between created workspaces
        switchWorkspace(workspaceIndex){
            this.$store.dispatch('loadWorkspace', {index: workspaceIndex})
            this.changeWorkspaceDialog = false
        },

        // creates a new workspace when floating button clicked
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
                    this.$store.dispatch('loadWorkspace', {key: this.$store.getters.workspace.id})
                }, 300)
    
                // reset newWorkspace (mainly for the form)
                this.newWorkspace = {
                    name: '',
                    description: '',
                    department: '',
                }

            })
            .catch(error => {console.log(error)})

            // close dialog
            this.createWorkspaceDialog = false
        },

        // returns list of unassigned workers by cohort
        cohortUnassigned(cohortId){
            // get cohort workers
            let returnArr = [];
            this.$store.getters.organization.org_workers.map(x => {
                if(x.worker_node == null && x.cohort == cohortId){
                    returnArr.push(x)
                }
            })
            return returnArr
        },

        // returns a list of unassigned workers by role (which are filtered by active cohorts)
        roleUnassigned(role){
            // get cohort workers
            let returnArr = [];
            this.$store.getters.organization.org_workers.map(x => {
                if(x.worker_node == null 
                    && (role.worker_ids.indexOf(x.id) != -1)
                    && this.isCohortActive(x.cohort)){
                    returnArr.push(x)
                }
            })
            return returnArr
        },

        // clears all workstations in active workspace
        clearWorkspaceNodes(){
            // abort if they user doesn't confirm
            if(!confirm(`Are you sure you want to clear all ${this.$store.getters.workspace.name} workstations?`)){
                return 
            }
            // iterate through all workstations
            for(let ws of this.$store.getters.workspace.workspace_nodes){
                // only patch if ws worker is not null
                if(ws.worker){
                    axios({
                        method: 'patch',
                        url: `${this.$store.getters.endpoints.baseAPI}/nodecreate/${ws.id}/`,
                        data: {
                            worker: null,
                        },
                        headers: {
                            authorization: `Bearer ${this.$store.getters.accessToken}`
                    },
                    })
                    .then(response => {
                        console.log(`Removing worker from node ${ws.name}`)
                        console.log(response)
                        // update this node's state
                        ws.worker = null

                    })
                    .catch(error => {console.log(error)})
                }
            }

            // after a one second timeout, update workspace
            setTimeout(() => {
        
                // reload workspace to update store 
                this.$store.dispatch('loadOrganization')
                this.$store.dispatch('loadWorkspace', {key: this.$store.getters.workspace.id})
            }, 1000)
            
        },

        // activates/deactivates a cohort
        toggleCohort(cohort){
            axios({
                method: 'patch',
                url: `${this.$store.getters.endpoints.baseAPI}/cohorts/${cohort.id}/`,
                data: {
                    is_active: !cohort.is_active
                },
                headers: {
                    authorization: `Bearer ${this.$store.getters.accessToken}`
            },
            })
            .then(response => {
                console.log(`Toggled ${cohort.name}. is_active: ${response.data.is_active}`)
                console.log(response)
                // after a one second timeout, update workspace
                setTimeout(() => {
                    // reload workspace to update store 
                    this.$store.dispatch('loadOrganization')
                }, 300)

            })
            .catch(error => {console.log(error)})
        },

        // when provided a cohort id, returns true/false if cohort is active
        isCohortActive(cohortId){
            for(let cohort of this.$store.getters.organization.org_cohorts){
                if(cohort.id == cohortId){
                    return cohort.is_active
                }
            }
        },

	},		// end methods

	computed: {
		org(){
			return this.$store.getters.organization
		},
		rules(){
			return this.$store.getters.formRules
        },
        departments(){
            let returnArray = []
            this.$store.getters.organization.org_departments.map(x => returnArray.push(x.name))
            return returnArray
        },
        roles(){
            let returnArray = []
            this.$store.getters.organization.org_roles.map(x => returnArray.push(x.name))
            return returnArray
        },
        currentWorkspaceId(){
            return this.$store.getters.workspace.id
        },
	},     // end computed
}
</script>
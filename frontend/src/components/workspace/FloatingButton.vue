<template>
    <div>
        <v-speed-dial
            v-model="fab"
           
            direction="top"
            transition="slide-y-reverse-transition"
            >
            <template v-slot:activator>
                <v-btn v-model="fab" color="blue darken-2" dark fab>
                    <v-icon v-if="fab">mdi-close</v-icon>
                    <v-icon v-else>dashboard</v-icon>
                </v-btn>
            </template>

            <v-tooltip right>
                <template v-slot:activator="{ on }">
                    <v-btn fab dark small color="green" v-on="on" @click="createNodeDialog = true">
                        <v-icon>mdi-pencil</v-icon>
                    </v-btn>
                </template>
                <span>Create Workstation</span>
            </v-tooltip>

            <!-- <v-tooltip right>
                <template v-slot:activator="{ on }">
                    <v-btn fab dark small color="indigo" v-on="on" @click="saveWorkspace">
                        <v-icon>save</v-icon>
                    </v-btn>
                </template>
                <span>Save Workspace</span>
            </v-tooltip> -->

            <v-tooltip right>
                <template v-slot:activator="{ on }">
                    <v-btn fab dark small color="red" v-on="on" @click="changeWorkspaceDialog = true">
                        <v-icon>view_carousel</v-icon>
                    </v-btn>
                </template>
                <span>Change Workspace</span>
            </v-tooltip>

            <v-tooltip right>
                <template v-slot:activator="{ on }">
                    <v-btn fab dark small color="orange" v-on="on" @click="createWorkspaceDialog = true">
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
        
        <!-- Change workspace dialog -->
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
                                        :rules="rules.name"
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

    </div>
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

    }),		// end data
    components: {

    },

    methods: {
        createNode(){
            // get department id from string that's been selected
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
        switchWorkspace(workspaceIndex){
            this.$store.dispatch('loadWorkspace', {index: workspaceIndex})
            this.changeWorkspaceDialog = false
        },
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
		saveWorkspace(){
			alert("implement ability to save workspace")
        },

	},		// end methods
	
	mounted(){
	},		// end mounted

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
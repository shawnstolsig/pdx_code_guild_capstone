<template>
    <v-container>
        <v-row>
            <v-col cols="12">

                <!-- Data table for showing all roles in org -->
                <v-data-table
                    :headers="headers"
                    :items="compiledRoleList"
                    :items-per-page="10"
                    :search="search"
                    sort-by="department"
                    class="elevation-3"
                >
                    <!-- Overwrite the top slot with CRUD -->
                    <template v-slot:top>
                        <v-toolbar flat>
                            <v-toolbar-title>
                                Roles
                            </v-toolbar-title>
                                <v-spacer></v-spacer>
                                <v-text-field
                                    v-model="search"
                                    append-icon="search"
                                    label="Search"
                                    single-line
                                    hide-details
                                ></v-text-field>

                                <v-spacer></v-spacer>

                                <!-- CRUD dialog, with "New" button -->
                                <v-dialog v-model="newRoleDialog" max-width="500px">
                                    <template v-slot:activator="{ on }">
                                        <v-btn color="primary" dark class="mb-2" v-on="on">New</v-btn>
                                    </template>
                                    <v-card>
                                        <v-card-title>
                                            <span class="headline">{{ formTitle }}</span>
                                        </v-card-title>

                                        <v-card-text>
                                            <v-container>
                                                <v-form v-model="createRoleValidity">
                                                    <v-row>
                                                        <v-col cols="12" sm="6">
                                                            <v-text-field 
                                                                v-model="editedItem.name" 
                                                                label="Name"
                                                                :rules="rules.name"
                                                                required
                                                            ></v-text-field>
                                                        </v-col>
                                                        <v-col cols="12" sm="6">
                                                            <v-select 
                                                                :items="departments" 
                                                                label="Department" 
                                                                v-model="editedItem.department"
                                                                required
                                                            ></v-select>
                                                        </v-col>
                                                    </v-row>
                                                    <v-row>
                                                        <v-col cols="12" sm="6">
                                                            <v-text-field 
                                                                v-model="editedItem.rate" 
                                                                label="Rate"
                                                                type='number'
                                                                required
                                                            ></v-text-field>
                                                        </v-col>
                                                        <v-spacer></v-spacer>
                                                        <v-col cols="12" sm="4">
                                                            <v-menu top nudge-bottom="105" nudge-left="16" :close-on-content-click="false">
                                                                <template v-slot:activator="{ on }">
                                                                    <v-chip v-on="on" :color="editedItem.color" x-large label>Color...</v-chip>
                                                                </template>
                                                                <v-card>
                                                                    <v-card-text class="pa-0">
                                                                        <v-color-picker v-model="editedItem.color" hide-inputs hide-mode-switch show-swatches />
                                                                    </v-card-text>
                                                                 </v-card>
                                                            </v-menu>
                                                        </v-col>
                                                        
                                                    </v-row>
                                                    <v-row>    
                                                        <v-col cols="12" >
                                                            <v-textarea 
                                                                v-model="editedItem.description" 
                                                                label="Description"
                                                                :rules="rules.description"
                                                                required
                                                                solo
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
                                                @click="close"
                                            >Cancel</v-btn>
                                            <v-btn 
                                                color="success" 
                                                text 
                                                :disabled="!formValid" 
                                                @click="saveRole"
                                            >Save</v-btn>
                                        </v-card-actions>
                                    </v-card>
                                </v-dialog>

                                 <!-- Dialog for setting worker roles -->
                                <v-dialog v-model="employeeRolesDialog" max-width="500px">
                                    <v-card>

                                        <v-card-title>
                                            Employee Roles
                                        </v-card-title>

                                        <v-card-subtitle>
                                            Add/remove employee's roles.
                                        </v-card-subtitle>

                                        <v-card-text>
                                            <v-list
                                                subheader
                                                two-line
                                                flat
                                            >
                                        
                                                <v-list-item-group
                                                v-model="selectedWorkers"
                                                multiple
                                                >
                                                <v-list-item v-for="worker in allWorkers" :key="worker.id">
                                                    <template v-slot:default="{ active, toggle }">
                                                    <v-list-item-action>
                                                        <v-checkbox
                                                        v-model="active"
                                                        color="primary"
                                                        @click="toggle"
                                                        ></v-checkbox>
                                                    </v-list-item-action>
                                        
                                                    <v-list-item-content>
                                                        <v-list-item-title>{{worker.full_name}}</v-list-item-title>
                                                    </v-list-item-content>
                                                    </template>
                                                </v-list-item>
                                        
                                                <v-list-item v-if="allWorkers.length == 0">
                                                    Please add employees to your organization.
                                                </v-list-item>

                                                </v-list-item-group>
                                            </v-list>
                                        </v-card-text>

                                        <v-card-actions>
                                            <v-spacer></v-spacer>
                                            <v-btn 
                                                color="error" 
                                                text 
                                                @click="employeeRolesDialog = false"
                                            >Cancel</v-btn>
                                            <v-btn 
                                                color="success" 
                                                text 
                                                @click="saveEmployeeRoles"
                                            >Save</v-btn>
                                        </v-card-actions>
                                    </v-card>
                                </v-dialog>
                        
                        </v-toolbar>
                    </template>

                    <!-- Custom item.action slot for having additional CRUD icon buttons-->
                    <template v-slot:item.action="{ item }">
                        <v-icon
                            small
                            class="mr-2"
                            @click="viewWorkers(item)"
                            >people
                        </v-icon>
                        <v-icon
                            small
                            class="mr-2"
                            @click="editItem(item)"
                            >edit
                        </v-icon>
                        <v-icon
                            small
                            @click="deleteItem(item)"
                            >delete
                        </v-icon>
                    </template>
                
                    <!-- Custom item.value slot for the color -->
                    <template v-slot:item.color="{ item }">
                        <v-chip :color="item.color" label> </v-chip>
                    </template>
    
                </v-data-table>
            </v-col>
        </v-row>
    </v-container>
</template>

<script>
import axios from 'axios'
export default {
    data: () => ({
        // for role CRUD operations
        newRoleDialog: false,
        createRoleValidity: false,
        headers: [
            {
                text: 'Name',
                sortable: true,
                value: 'name',
            },
            {
                text: 'Color',
                sortable: false,
                value: 'color',
            },
            {
                text: 'Department',
                sortable: true,
                value: 'department',
            },
            {
                text: 'Rate',
                sortable: true,
                value: 'rate',
            },
            {
                text: 'Employee Count',
                sortable: true,
                value: 'count',
            },
            { 
                text: 'Actions', 
                value: 'action', 
                sortable: false 
            },
        ],
        search: '',
        compiledRoleList: [],
        deptListObj: {},
        editedIndex: -1,
        editedItem: {
            id: '',
            name: '',
            department: '',
            rate: '',
            count: '',
            description: '',
            workerArray: [],
            color: ''
        },
        defaultItem: {
            id: '',
            name: '',
            department: '',
            rate: '',
            count: '',
            description: '',
            workerArray: [],
            color: ''
        },
        // for adding/removing employee roles
        employeeRolesDialog: false,
        qualifiedWorkerArray: [],
        selectedWorkers: [],
        selectedRole: undefined

    }),     // end of data

    computed: {
        formTitle () {
            return this.editedIndex === -1 ? 'New Role' : 'Edit Role Details'
        },
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
        formValid(){
            return this.createRoleValidity && !!this.editedItem.department
        },
        allWorkers(){
            return this.$store.getters.organization.org_workers
        },
    },      // end of computed

    watch: {
        // runs close() when dialog closes
        newRoleDialog (val) {
            val || this.close()
        },
    },      // end of watch

    // loads roles into data table
    created () {
        this.initialize()
    },      // end of created

    methods: {
        // loads roles into data table
        initialize () {
            // create array for displaying in list.  
            // Clear slate
            this.compiledRoleList = []
            this.deptListObj = {}

            // Store id/dept name pairs
            this.$store.getters.organization.org_departments.map(x => this.deptListObj[x.id] = x.name)

            // Create compiled role list
            this.$store.getters.organization.org_roles.map(x => {
                this.compiledRoleList.push(
                {
                    id: x.id,
                    name: x.name,
                    department: this.deptListObj[x.department],
                    rate: x.rate ? x.rate : '-',
                    count: x.worker_ids.length ? x.worker_ids.length : 0,
                    description: x.description,
                    workerArray: x.worker_ids,
                    color: x.color

                })
            })
        },     

        // loads existing role information into form if editing
        editItem (item) {
            this.editedIndex = this.compiledRoleList.indexOf(item)
            this.editedItem = Object.assign({}, item)
            this.newRoleDialog = true
        },

        // deletes role when trash button clicked
        deleteItem (item) {
            if(confirm('Are you sure you want to delete this item?')){
                axios({
                    method: 'delete',
                    url: `${this.$store.getters.endpoints.baseAPI}/roles/${item.id}`,
                    headers: {
                        authorization: `Bearer ${this.$store.getters.accessToken}`
                    },
                })
                .then(response => {
                    console.log(response)
                    this.$store.dispatch('loadOrganization')
                    setTimeout(() => {
                        this.initialize()
                    }, 300)
                    
                })
                .catch(error => {console.log(error)})
            } 
        },

        // reloads org and roles data table infromation whenever role dialog is closed
        close () {
            this.newRoleDialog = false

            setTimeout(() => {
                this.editedItem = Object.assign({}, this.defaultItem)
                this.editedIndex = -1
                this.$store.dispatch('loadOrganization')
            }, 300)

            setTimeout(() => {
                this.initialize()
            }, 600)
        },

        // updates db with role information (for both creation and editing)
        saveRole () {
            // Check to make sure token is valid
            this.$store.dispatch('verifyLogin')
            
            // get department and cohort ID's from the strings passed in by the dialog's selects
            let deptId;
            for(let dept of this.$store.getters.organization.org_departments){
                if(dept.name == this.editedItem.department){
                    deptId = dept.id
                }
            }
            // If role is edited, make axios patch
            if (this.editedIndex > -1) {
                // axios patch call
                axios({
                    method: 'patch',
                    url: `${this.$store.getters.endpoints.baseAPI}/roles/${this.compiledRoleList[this.editedIndex].id}/`,
                    data: {
                        name: this.editedItem.name,
                        description: this.editedItem.description,
                        rate: (this.editedItem.rate == '-') ? undefined : this.editedItem.rate,
                        organization: this.$store.getters.organization.id,
                        department: deptId,
                        worker_ids: this.editedItem.workerArray,
                        color: this.editedItem.color
                    },
                    headers: {
                        authorization: `Bearer ${this.$store.getters.accessToken}`
                    },
                })
                .then(response => {
                    console.log(response)
                    this.$store.dispatch('loadOrganization')
                    setTimeout(() => {
                        this.initialize()
                    }, 300)
                    
                })
                .catch(error => {console.log(error)})

            }
            // If role is created, make axios post 
            else {
                console.log("this.editedItem.rate")
                console.log(typeof this.editedItem.rate)
                // axios post call
                axios({
                    method: 'post',
                    url: `${this.$store.getters.endpoints.baseAPI}/roles/`,
                    data: {
                        name: this.editedItem.name,
                        description: this.editedItem.description,
                        rate: this.editedItem.rate ? this.editedItem.rate : null,
                        organization: this.$store.getters.organization.id,
                        department: deptId,
                        worker_ids: [],
                        color: this.editedItem.color
                    },
                    headers: {
                        authorization: `Bearer ${this.$store.getters.accessToken}`
                    },
                })
                .then(response => {
                    console.log(response)
                    this.$store.dispatch('loadOrganization')
                    
                })
                .catch(error => {console.log(error)})
            }
            this.close()
        },

        // loads worker arrays with workers who are qualified in a particular role
        viewWorkers (item) {
            // reset arrays
            this.qualifiedWorkerArray = []          // used for track those who are qualified in role
            this.selectedWorkers = []               // used for rendering workers and tracking changes
            this.selectedRole = item
            
            // get array of worker pk that are qualified in role
            for(let role of this.$store.getters.organization.org_roles){
                if (role.id == item.id){
                    this.qualifiedWorkerArray = role.worker_ids
                }
            }
            
            // create array of all workers for displaying in the list
            for(let i = 0; i < this.$store.getters.organization.org_workers.length; i++){
                let worker = this.$store.getters.organization.org_workers[i]
                if(this.qualifiedWorkerArray.indexOf(worker.id) != -1){
                    this.selectedWorkers.push(i)
                }
             }
            
            // open dialog
            this.employeeRolesDialog = true
        },

        // Save employee roles
        saveEmployeeRoles(){
            // get ids of workers in selectedWorkers
            let workerIds = []
            let workers = this.$store.getters.organization.org_workers
            this.selectedWorkers.map(x => workerIds.push(workers[x].id))

            // axios patch call
            axios({
                method: 'patch',
                url: `${this.$store.getters.endpoints.baseAPI}/roles/${this.selectedRole.id}/`,
                data: {
                    worker_ids: workerIds
                },
                headers: {
                    authorization: `Bearer ${this.$store.getters.accessToken}`
                },
            })
            .then(response => {
                console.log(response)
                this.$store.dispatch('loadOrganization')
                setTimeout(() => {
                    this.initialize()
                }, 300)
                
            })
            .catch(error => {console.log(error)})

            // reset dialog and item to be edited
            this.selectedRole = undefined
            this.employeeRolesDialog = false
        }
        
    },      // end of methods
}
</script>
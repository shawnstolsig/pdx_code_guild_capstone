<template>
    <v-container>
        <v-row>
            <v-col cols="12">
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
                            
                                <!-- <v-divider class="mx-4" inset vertical></v-divider> -->

                                <v-spacer></v-spacer>

                                <!-- CRUD dialog -->
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
                                                        <v-col cols="12" sm="6" md="4">
                                                            <v-text-field 
                                                                v-model="editedItem.name" 
                                                                label="Name"
                                                                :rules="rules.name"
                                                                required
                                                            ></v-text-field>
                                                        </v-col>
                                                        <v-col cols="12" sm="6" md="4">
                                                            <v-select 
                                                                :items="departments" 
                                                                label="Department" 
                                                                v-model="editedItem.department"
                                                                required
                                                            ></v-select>
                                                        </v-col>
                                                        <v-col cols="12" sm="6" md="4">
                                                            <v-text-field 
                                                                v-model="editedItem.rate" 
                                                                label="Rate"
                                                                type='number'
                                                                required
                                                            ></v-text-field>
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
                                                @click="save"
                                            >Save</v-btn>
                                        </v-card-actions>
                                    </v-card>
                                </v-dialog>
                        </v-toolbar>
                    </template>

                    <!-- Custom item.action slot -->
                    <template v-slot:item.action="{ item }">
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

                    <!-- Custom no-data slot -->
                    <!-- <template v-slot:no-data>
                        <v-btn color="primary" @click="initialize">Reset</v-btn>
                        <v-spacer></v-spacer>
                        <v-subheader>No data...please add employees.</v-subheader>
                        <v-spacer></v-spacer>
                    </template> -->
                
                </v-data-table>
            </v-col>

            <!-- <v-col cols="4">
                <v-card>
                    <v-list
                        flat
                        dense
                        >
                        <v-header>Workers Trained in Role</v-header>

                        <v-list-item-group
                            v-model="settings"
                            multiple
                        >
                            <v-list-item v-for="worker in org.org_workers" :key="worker.id">
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

                            <v-list-item v-if="org.org_workers.length == 0">
                                <v-list-item-content>
                                    <v-list-item-title class="grey--text">(none)</v-list-item-title>
                                </v-list-item-content>
                            </v-list-item>

                        </v-list-item-group>
                    </v-list>
                </v-card>
            </v-col> -->
        </v-row>
    </v-container>
</template>

<script>
import axios from 'axios'
export default {
    data: () => ({
        newRoleDialog: false,
        headers: [
            {
                text: 'Name',
                sortable: true,
                value: 'name',
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
        createRoleValidity: false,
        editedIndex: -1,
        editedItem: {
            id: '',
            name: '',
            department: '',
            rate: '',
            count: '',
            workerArray: []
        },
        defaultItem: {
            id: '',
            name: '',
            department: '',
            rate: '',
            count: '',
            workerArray: []
        },
    }),

    computed: {
        formTitle () {
            return this.editedIndex === -1 ? 'New Item' : 'Edit Item'
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
    },      // end of computed

    watch: {
        newRoleDialog (val) {
            val || this.close()
        },
    },      // end of watch

    created () {
        this.initialize()
    },      // end of created

    methods: {
        initialize () {
            // create array for displaying in list.  
            // Clear slate
            this.compiledRoleList = []
            this.deptListObj = {}

            // Store id/dept name pairs
            this.$store.getters.organization.org_departments.map(x => this.deptListObj[x.id] = x.name)

            // Create compiled role list
            this.$store.getters.organization.org_roles.map(x => {
                console.log(`pushing role ${x}`)
                this.compiledRoleList.push(
                {
                    id: x.id,
                    name: x.name,
                    department: this.deptListObj[x.department],
                    rate: x.rate,
                    count: x.worker_ids.count ? x.worker_ids.count : 0,
                    workerArray: x.worker_ids
                })
            })
        },      // end of initialize

        editItem (item) {
            alert("need to implement edit role" + item)
            // this.editedIndex = this.roleList.indexOf(item)
            // this.editedItem = Object.assign({}, item)
            // this.newRoleDialog = true
        },

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

        close () {
            this.newRoleDialog = false

            setTimeout(() => {
                this.editedItem = Object.assign({}, this.defaultItem)
                this.editedIndex = -1
                this.initialize()
            }, 300)
        },

        save () {
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
                // Object.assign(this.roleList[this.editedIndex], this.editedItem)
                let rolePk = this.roleList[this.editedIndex].id
                axios({
                    method: 'patch',
                    url: `${this.$store.getters.endpoints.baseAPI}/roles/${rolePk}/`,
                    data: {
                        name: this.editedItem.name,
                        description: this.editedItem.description,
                        rate: this.editedItem.rate,
                        organization: this.$store.getters.organization.id,
                        department: deptId,
                        worker_ids: this.editedItem.workerArray
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
            // If role is created, make axios post 
            else {
                // axios post call
                axios({
                    method: 'post',
                    url: `${this.$store.getters.endpoints.baseAPI}/roles/`,
                    data: {
                        name: this.editedItem.name,
                        description: this.editedItem.description,
                        rate: this.editedItem.rate,
                        organization: this.$store.getters.organization.id,
                        department: deptId,
                        worker_ids: []
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
    },      // end of methods
}
</script>
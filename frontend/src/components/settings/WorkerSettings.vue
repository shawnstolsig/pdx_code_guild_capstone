<template>
    <v-data-table
        :headers="headers"
        :items="workerList"
        :items-per-page="10"
        :search="search"
        sort-by="lastName"
        class="elevation-3"
    >
        <!-- Overwrite the top slot with CRUD -->
        <template v-slot:top>
            <v-toolbar flat>
                <v-toolbar-title>
                    Employees
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
                    <v-dialog v-model="dialog" max-width="500px">
                        <template v-slot:activator="{ on }">
                            <v-btn color="primary" dark class="mb-2" v-on="on">New</v-btn>
                        </template>
                        <v-card>
                            <v-card-title>
                                <span class="headline">{{ formTitle }}</span>
                            </v-card-title>

                            <v-card-text>
                                <v-container>
                                    <v-form v-model="createWorkerValidity">
                                        <v-row>
                                            <v-col cols="12" sm="6" md="4">
                                                <v-text-field 
                                                    v-model="editedItem.firstName" 
                                                    label="First name"
                                                    :rules="rules.name"
                                                    required
                                                ></v-text-field>
                                            </v-col>
                                            <v-col cols="12" sm="6" md="4">
                                                <v-text-field 
                                                    v-model="editedItem.lastName" 
                                                    label="Last name"
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
                                                <v-select 
                                                    :items="cohorts" 
                                                    label="Cohort" 
                                                    v-model="editedItem.cohort"
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
</template>

<script>
import axios from 'axios'
export default {
    data: () => ({
        dialog: false,
        headers: [
            {
                text: 'First Name',
                sortable: true,
                value: 'firstName',
            },
            {
                text: 'Last Name',
                sortable: true,
                value: 'lastName',
            },
            {
                text: 'Department',
                sortable: true,
                value: 'department',
            },
            {
                text: 'Cohort',
                sortable: true,
                value: 'cohort',
            },
            { 
                text: 'Actions', 
                value: 'action', 
                sortable: false 
            },
        ],
        search: '',
        workerList: [],
        createWorkerValidity: false,
        editedIndex: -1,
        editedItem: {
            firstName: '',
            lastName: '',
            department: '',
            cohort: '',
        },
        defaultItem: {
            firstName: '',
            lastName: '',
            department: '',
            cohort: '',
        },
    }),

    computed: {
        formTitle () {
            return this.editedIndex === -1 ? 'New Employee' : 'Edit Employee Details'
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
        cohorts(){
            let returnArray = []
            this.$store.getters.organization.org_cohorts.map(x => returnArray.push(x.name))
            return returnArray
        },
        formValid(){
            return this.createWorkerValidity && !!this.editedItem.department && !!this.editedItem.cohort
        },
    },      // end of computed

    watch: {
        dialog (val) {
            val || this.close()
        },
    },      // end of watch

    created () {
        this.initialize()
    },      // end of created

    methods: {
        initialize () {
            // create array for displaying in list.  
            // Only needs firstName, lastName, Dept (as string), Cohort(as string)
            let org = this.$store.getters.organization
            this.workerList = []
            let deptPairs = {}
            let cohortPairs = {}
            org.org_departments.map(x => deptPairs[x.id] = x.name)
            org.org_cohorts.map(x => cohortPairs[x.id] = x.name)
            for(let worker of org.org_workers){
                this.workerList.push({
                    id: worker.id,
                    firstName: worker.first_name,
                    lastName: worker.last_name,
                    department: deptPairs[worker.department],
                    cohort: cohortPairs[worker.cohort],
                })
            }
        },      // end of initialize

        editItem (item) {
            this.editedIndex = this.workerList.indexOf(item)
            this.editedItem = Object.assign({}, item)
            this.dialog = true
        },

        deleteItem (item) {
            if(confirm('Are you sure you want to delete this item?')){
                axios({
                    method: 'delete',
                    url: `${this.$store.getters.endpoints.baseAPI}/workers/${item.id}`,
                    headers: {
                        authorization: `Bearer ${this.$store.getters.accessToken}`
                    },
                })
                .then(response => {
                    console.log(response)
                    this.$store.dispatch('loadOrganization')
                    setTimeout(() => {
                        this.initialize()
                    }, 500)
                    
                })
                .catch(error => {console.log(error)})
            } 
        },

        close () {
            this.dialog = false
            setTimeout(() => {
                this.editedItem = Object.assign({}, this.defaultItem)
                this.editedIndex = -1
                this.initialize()
            }, 500)

        },

        save () {
            // Check to make sure token is valid
            this.$store.dispatch('verifyLogin')
            
            // get department and cohort ID's from the strings passed in by the dialog's selects
            let deptId;
            let cohortId;
            for(let dept of this.$store.getters.organization.org_departments){
                if(dept.name == this.editedItem.department){
                    deptId = dept.id
                }
            }
            for(let cohort of this.$store.getters.organization.org_cohorts){
                if(cohort.name == this.editedItem.cohort){
                    cohortId = cohort.id
                }
            }
            // If worker is edited, make axios patch
            if (this.editedIndex > -1) {
                // axios patch call
                // Object.assign(this.workerList[this.editedIndex], this.editedItem)
                let workerPk = this.workerList[this.editedIndex].id
                axios({
                    method: 'patch',
                    url: `${this.$store.getters.endpoints.baseAPI}/workers/${workerPk}/`,
                    data: {
                        first_name: this.editedItem.firstName,
                        last_name: this.editedItem.lastName,
                        full_name: `${this.editedItem.firstName} ${this.editedItem.lastName}`,
                        organization: this.$store.getters.organization.id,
                        department: deptId,
                        cohort: cohortId,
                    },
                    headers: {
                        authorization: `Bearer ${this.$store.getters.accessToken}`
                    },
                })
                .then(response => {
                    console.log(response)
                    this.$store.dispatch('loadOrganization')
                    this.close()
                })
                .catch(error => {console.log(error)})

            }
            // If worker is created, make axios post 
            else {
                // axios post call
                axios({
                    method: 'post',
                    url: `${this.$store.getters.endpoints.baseAPI}/workers/`,
                    data: {
                        first_name: this.editedItem.firstName,
                        last_name: this.editedItem.lastName,
                        full_name: `${this.editedItem.firstName} ${this.editedItem.lastName}`,
                        organization: this.$store.getters.organization.id,
                        department: deptId,
                        cohort: cohortId,
                        worker_node: null,
                    },
                    headers: {
                        authorization: `Bearer ${this.$store.getters.accessToken}`
                    },
                })
                .then(response => {
                    console.log(response)
                    this.$store.dispatch('loadOrganization')
                    this.close()
                })
                .catch(error => {console.log(error)})
            }
            
        },
    },      // end of methods
}
</script>
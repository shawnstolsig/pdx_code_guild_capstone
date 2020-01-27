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
            <v-toolbar flat color="white">
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
                                    <v-row>
                                        <v-col cols="12" sm="6" md="4">
                                            <v-text-field v-model="editedItem.firstName" label="First name"></v-text-field>
                                        </v-col>
                                        <v-col cols="12" sm="6" md="4">
                                            <v-text-field v-model="editedItem.lastName" label="Last name"></v-text-field>
                                        </v-col>
                                        <v-col cols="12" sm="6" md="4">
                                            <v-select :items="departments" label="Department" v-model="editedItem.department"></v-select>
                                        </v-col>
                                        <v-col cols="12" sm="6" md="4">
                                            <v-select :items="cohorts" label="Department" v-model="editedItem.cohort"></v-select>
                                        </v-col>
                                    </v-row>
                                </v-container>
                            </v-card-text>

                            <v-card-actions>
                                <v-spacer></v-spacer>
                                <v-btn color="blue darken-1" text @click="close">Cancel</v-btn>
                                <v-btn color="blue darken-1" text @click="save">Save</v-btn>
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
            >
                edit
            </v-icon>
            <v-icon
                small
                @click="deleteItem(item)"
            >
                delete
            </v-icon>
        </template>

        <!-- Custom no-data slot -->
        <template v-slot:no-data>
            <v-btn color="primary" @click="initialize">Reset</v-btn>
        </template>
    
    </v-data-table>
</template>

<script>
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
        ],
        search: '',
        workerList: [],
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
        cohorts(){
            let returnArray = []
            this.$store.getters.organization.org_cohorts.map(x => returnArray.push(x.name))
            return returnArray
        }
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
            this.workerList = this.$store.getters.organization.org_workers
        },      // end of initialize

        editItem (item) {
            this.editedIndex = this.workerList.indexOf(item)
            this.editedItem = Object.assign({}, item)
            this.dialog = true
        },

        deleteItem (item) {
            const index = this.workerList.indexOf(item)
            confirm('Are you sure you want to delete this item?') && this.workerList.splice(index, 1)
        },

        close () {
            this.dialog = false
            setTimeout(() => {
                this.editedItem = Object.assign({}, this.defaultItem)
                this.editedIndex = -1
            }, 300)
        },

        save () {
            if (this.editedIndex > -1) {
                Object.assign(this.workerList[this.editedIndex], this.editedItem)
            } else {
                this.workerList.push(this.editedItem)
            }
            this.close()
        },
    },      // end of methods
}
</script>
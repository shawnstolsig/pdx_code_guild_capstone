<template>
    <v-container>
        <v-card class="mt-5">
            <v-row>
                <v-spacer></v-spacer>
                <v-col cols="12" md="6" class="pb-0 mt-5">
                    <v-card-title class="display-1 pb-0">Scan badge:</v-card-title>
                </v-col>
                <v-spacer></v-spacer>
            </v-row>

            <v-row>
                <v-spacer></v-spacer>
                <v-col cols="12" md="6" class="pb-0">
                        <v-card-text class="py-0">
                            <v-text-field 
                                v-model="input" 
                                solo 
                                clearable
                                autofocus
                            ></v-text-field>
                        </v-card-text>
                </v-col>
                <v-spacer></v-spacer>
            </v-row>

            <v-row >
                <v-spacer></v-spacer>
                <v-col cols="12" md="6">
                        <v-card-text class="py-0">
                            <v-text-field 
                                v-model="message" 
                                solo 
                                flat
                                
                            ></v-text-field>
                        </v-card-text>
                </v-col>
                <v-spacer></v-spacer>
            </v-row>
            
            <v-row>
                <v-spacer></v-spacer>
                <v-col cols="12" md="6" class="pb-0">
                    <v-card-title class="display-1 pb-0">Assignment:</v-card-title>
                </v-col>
                <v-spacer></v-spacer>
            </v-row>
            <v-row>
                <v-spacer></v-spacer>
                <v-col cols="12" md="6" class="py-0">
                    <v-card-text>
                            <v-text-field 
                                outlined
                                v-model="department"
                                label="Department"
                                readonly
                            ></v-text-field>
                    </v-card-text>
                </v-col>
                <v-spacer></v-spacer>
            </v-row>
            <v-row>
                <v-spacer></v-spacer>
                <v-col cols="12" md="6" class="py-0">
                    <v-card-text>
                            <v-text-field 
                                outlined
                                v-model="area"
                                label="Area"
                                readonly
                            ></v-text-field>
                    </v-card-text>
                </v-col>
                <v-spacer></v-spacer>
            </v-row>
            <v-row>
                <v-spacer></v-spacer>
                <v-col cols="12" md="6" class="py-0">
                    <v-card-text>
                            <v-text-field 
                                outlined
                                v-model="workstation"
                                label="Workstation"
                                readonly
                            ></v-text-field>
                    </v-card-text>
                </v-col>
                <v-spacer></v-spacer>
            </v-row>
            <v-row>
                <v-spacer></v-spacer>
                <v-col cols="12" md="6" class="py-0">
                    <v-card-text>
                        <v-text-field 
                            outlined
                            v-model="role"
                            label="Role"
                            readonly
                        ></v-text-field>
                    </v-card-text>
                </v-col>
                <v-spacer></v-spacer>
            </v-row>
        </v-card>
    </v-container>
</template>

<script>
export default {
    data(){
        return {
            message: '',
            input: '',
            workstation: '',
            department: '',
            role: '',
            area: '',
        }
    },      // end data
    methods: {
        showWorkstation(){

        }
    },      // end methods
    watch: {
        input(value){
            // clear out data if input value is zero
            if(value=='' || !value){
                this.message = ''
                this.workstation = ''
                this.department = ''
                this.role = ''
                this.area = ''
            } 
            // process input...
            else {
                for(let worker of this.$store.getters.organization.org_workers){

                    // if worker is found in db
                    if(worker.full_name == value){
                        this.message = ''

                        // if worker is not assigned
                        if(worker.worker_node == null){
                            this.message = "Unassigned, please see your manager."
                        }
                        // if worker is assigned
                        else {
                            // set workstation
                            this.workstation = worker.worker_node.name

                            // set department
                            for(let dept of this.$store.getters.organization.org_departments){
                                if(dept.id == worker.department){
                                    this.department = dept.name
                                }
                            }
                            // set work area
                            for(let a of this.$store.getters.organization.org_workspaces){
                                if(a.id == worker.worker_node.workspace){
                                    this.area = a.name
                                }
                            }
                            // set role
                            for(let r of this.$store.getters.organization.org_roles){
                                if(r.id == worker.worker_node.role){
                                    this.role = r.name
                                }
                            }
                        }

                        break
                    } 
                    // if worker is not found in db
                    else {
                        this.message = 'Badge not recognized, please see HR.'
                        this.workstation = ''
                        this.department = ''
                        this.role = ''
                        this.area = ''
                    }        
                    // clear input field for next employee
                    setTimeout(() => {
                        this.input = ''
                    }, 5000)
                    
                }
            }
        }
    },      // end watch
    computed: {
        org(){
            return this.$store.getters.organization
        },
    },      // end computed
}
</script>
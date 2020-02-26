<template>

   <v-card>
       <v-card-title>Generate Shift Assignments</v-card-title>
       <v-card-text>
           <v-container>
               <v-row>
                   <v-col cols="6">
                        <v-text-field 
                            outlined
                            v-model="workspaceDept"
                            label="Department"
                            readonly
                        ></v-text-field>
                   </v-col>
                   <v-col cols="6">
                        <v-text-field 
                            outlined
                            v-model="workspaceName"
                            label="Workspace"
                            readonly
                        ></v-text-field>
                   </v-col>
               </v-row>

               <v-row align="center"> 
                   <v-col cols="12">
                       <v-select
                       v-model="selectedCohorts"
                        :items="org.org_cohorts"
                        :item-text="cohortText"
                        multiple
                        chips
                        label="Cohorts"
                        return-object
                       ></v-select>
                   </v-col>
               </v-row>
               <v-row align="center"> 
                   <v-col cols="12">
                       <v-select
                        v-model="selectedNodes"
                        :items="workspace.workspace_nodes"
                        :item-text="nodeText"
                        multiple
                        chips
                        label="Workstations"
                        return-object
                       >
                                <template v-slot:selection="{ item, index }">
                                    <v-chip v-if="index === 0">
                                    <span>{{ item.name }}</span>
                                    </v-chip>
                                    <span
                                    v-if="index === 1"
                                    class="grey--text caption"
                                    >(+{{ selectedNodes.length - 1 }} others)</span>
                                </template>
                       </v-select>
                   </v-col>
               </v-row>


           </v-container>

       </v-card-text>
       <v-card-actions>
            <v-spacer></v-spacer>
            <v-btn 
                color="error" 
                text 
                @click="$emit('close-autofill')"
            >Cancel</v-btn>
            <v-btn 
                color="success" 
                text 
                @click="generateAssignments"
            >Generate</v-btn>
       </v-card-actions>
   </v-card>
</template>

<script>

// import axios from 'axios'
export default {
   
    props: {
        
    },

    data(){
		return {
            selectedNodes: undefined,
            selectedCohorts: undefined,
		}
	},    // end data

    methods: {

        // function for formatting cohort names in v-select
        cohortText(item){
            return item.name
        },

        // node names for v-select
        nodeText(item){
            return `${item.name} (${item.role.name})` 
        },
        
        // generate shift assignments
        generateAssignments(){
            this.$emit('close-autofill')
        },

	},    // end methods

    computed: {
        org(){
            return this.$store.getters.organization
        },
        workspace(){
            return this.$store.getters.workspace
        },
        rules(){
            return this.$store.getters.formRules
        },
        workspaceDept(){
            for(let dept of this.$store.getters.organization.org_departments){
                if(dept.id == this.$store.getters.workspace.department){
                    return dept.name
                }
            }
            return "Dept not found"
        },
        workspaceName(){
            return this.$store.getters.workspace.name
        },

    },  // end computed

    // set up initial lists for active cohorts and nodes
    mounted(){
        let activeCohortList = []
        let activeNodeList = []

        for (let cohort of this.$store.getters.organization.org_cohorts){
            if(cohort.is_active){
                activeCohortList.push(cohort)
            }
        }
        for (let node of this.$store.getters.workspace.workspace_nodes){
            if(node.is_active){
                activeNodeList.push(node)
            }
        }

        this.selectedCohorts = activeCohortList
        this.selectedNodes = activeNodeList
    },  // end mounted
}
</script>

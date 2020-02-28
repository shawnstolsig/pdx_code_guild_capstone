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
        
        // generate shift assignments (main function for autofill)
        generateAssignments(){

            // get an arrray of available (active and in select cohorts) employees
            let workerArray = this.getAvailableWorkersArray()

            // given list of available workers, add a difficulty rating to each selected node and sort by rating 
            this.addRatingToSelectedNodesAndSort(workerArray)

            // at this point, all nodes are in an array sorted by rating, from most to least difficult to fill
            // also, workerArray contains all workers who are active and on shift 

            console.log("workerArray:")
            console.log(workerArray)
            console.log("selectedNodes")
            console.log(this.selectedNodes)

            // ---------------------------- auto fill process ----------------------------
            // look at first node in node list
            for(let node of this.selectedNodes){

                // create array of worker objects who are trained in role and are available
                let roleWorkers = []

                for(let workerId of node.role.worker_ids){
                    for(let w of this.$store.getters.organization.org_workers){
                        if(workerId == w.id && workerArray.map(x => x.id).includes(w.id)){
                            roleWorkers.push(w)
                        }
                    }
                }
                
                // check to see if there are no available roleWorkers
                if(roleWorkers.length == 0){
                    alert(`There are no available workers in role ${node.role.name} for workstation ${node.name}.`)
                    break
                } else {

                    // order alphabetically by last
                    // roleWorkers.sort(function(a, b) {
                    //     var nameA = a.last_name.toUpperCase(); // ignore upper and lowercase
                    //     var nameB = b.last_name.toUpperCase(); // ignore upper and lowercase
                    //     if (nameA < nameB) {
                    //         return -1;
                    //     }
                    //     if (nameA > nameB) {
                    //         return 1;
                    //     }

                    //     // names must be equal
                    //     return 0;
                    // });

                    // randomly assign employee from list
                    let randomWorker = roleWorkers[Math.floor(Math.random()*roleWorkers.length)]
                    console.log(`${randomWorker.full_name} selected for node.name`)
                    
                }
            }


            // remove assigned employee from available employee lists for all roles
            // remove node from list of nodes to be filled (reverse order? adjust i--?)
            // recaculate difficulty for each role
            // reorder node list based on updated  
            // repeat last 5 steps

            // reset arrays
            this.selectedNodes = null
            this.selectedCohorts = null


            // close dialog
            this.$emit('close-autofill')
        },

        // helper functions for generateAssignments: ------------------------------------------------------
        getAvailableWorkersArray(){
            let returnArr = []
            // create a list of available (in cohort and active) employees
            for(let worker of this.$store.getters.organization.org_workers){
                if(this.selectedCohorts.map(x => x.id).includes(worker.cohort) && worker.is_active){
                    returnArr.push(worker)
                }
            }
            return returnArr
        },
        addRatingToSelectedNodesAndSort(workerArray){

            // declare starting object literal 
            let rolesObj = {}

            // iterate through all nodes being filled and store number of employees needed
            for(let node of this.selectedNodes){
                if(rolesObj[node.role.id] == undefined){
                    rolesObj[node.role.id] = {
                        name: node.role.name,
                        worker_ids: node.role.worker_ids,
                        count: 1,
                    }
                }
                else{
                    rolesObj[node.role.id].count++
                }
            }

            // create a rating of how hard each node will be to staff.  # workers available / # workers needed (lower is harder, below one is impossible)
            // determine rating for each role:
            for(let role in rolesObj){

                // counter for available employees with role
                let availableCount = 0

                // iterate through all available employees, increment counter if employee is in worker_ids
                for(let worker of workerArray){
                    if(rolesObj[role].worker_ids.includes(worker.id)){
                        availableCount++;
                    }
                }

                // add rating key/value pair
                // edge case: nobody is trained, set raiting to 0
                if(rolesObj[role].count == 0 ) {
                    rolesObj[role].rating = 0
                } 
                else {
                    rolesObj[role].rating = availableCount / rolesObj[role].count
                }

            }
            
            // put all nodes in list, order each node by rating:
            // add rating to all selectedNodes
            for(let node of this.selectedNodes){
                node.rating = rolesObj[node.role.id].rating
            }

            // sort lowest to highest by 
            this.selectedNodes.sort(function(a,b){
                return a.rating - b.rating
            })
        },
        assignWorker(){

        },
        // ------------------------------------------------------------------------------------------------

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


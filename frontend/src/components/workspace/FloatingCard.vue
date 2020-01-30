<template>
    <VueDraggableResizable 
        :w="node.width" :h="node.height" 
        @dragging="onDrag" 
        @resizing="onResize" 
        @dragstop="onDragStop" 
        :parent="true" 
        :draggable="node.draggable" 
        :x="node.x" :y="node.y">
        <v-card>
            <v-toolbar dense short :color="node.role.color">
                <v-toolbar-title>
                    {{node.name}}
                </v-toolbar-title>
                <v-spacer></v-spacer>
                <v-btn icon @click="toggleLock">
                    <v-icon>{{node.draggable ? 'lock_open' : 'lock'}}</v-icon>
                </v-btn>

                <!-- Popup menu for each workstation -->
                <v-menu
                    v-model="cardMenu"
                    bottom
                    left
                    transition="scale-transition"
                    origin="top right"
                    >
                    <template v-slot:activator="{ on }">
                        <v-btn icon v-on="on">
                            <v-icon>mdi-dots-vertical</v-icon>
                        </v-btn>
                    </template>

                    <v-card>
                        <v-list>
                            <v-list-item>
                                <v-list-item-avatar :color="node.role.color">
                                    
                                </v-list-item-avatar>

                                <v-list-item-content>
                                    <v-list-item-title>{{node.name}}</v-list-item-title>
                                    <v-list-item-subtitle>{{node.role.name}}</v-list-item-subtitle>
                                </v-list-item-content>

                                <v-list-item-action>
                                    <v-btn icon @click="cardMenu = false">
                                        <v-icon>mdi-close-circle</v-icon>
                                    </v-btn>
                                </v-list-item-action>
                            </v-list-item>
                        </v-list>

                        <v-divider></v-divider>

                        <v-list>
                            <v-list-item @click="addWorkerStart">
                                <v-list-item-action>
                                    <v-icon>add_circle</v-icon>
                                </v-list-item-action>
                                <v-list-item-subtitle>Add worker...</v-list-item-subtitle>
                            </v-list-item>
                            <v-list-item @click="removeWorker">
                                <v-list-item-action>
                                    <v-icon>remove_circle_outline</v-icon>
                                </v-list-item-action>
                                <v-list-item-subtitle>Remove worker</v-list-item-subtitle>
                            </v-list-item>
                            <v-list-item @click="swapWorker">
                                <v-list-item-action>
                                    <v-icon>compare_arrows</v-icon>
                                </v-list-item-action>
                                <v-list-item-subtitle>Swap worker...</v-list-item-subtitle>
                            </v-list-item>
                            <v-list-item @click="editWorkstation">
                                <v-list-item-action>
                                    <v-icon>settings</v-icon>
                                </v-list-item-action>
                                <v-list-item-subtitle>Configure workstation...</v-list-item-subtitle>
                            </v-list-item>
                        </v-list>
                    </v-card>
                </v-menu>
            </v-toolbar>

            <v-card-text>
                <v-list dense>
                    <!-- if no assigned worker, leave empty -->
                    <v-list-item v-if="!node.worker">
                        <v-list-item-title>No employee assigned</v-list-item-title>
                        {{node.role.name}}
                    </v-list-item>

                    <!-- if worker assigned, load name/cohort/colors -->
                    <v-list-item v-if="node.worker">
                        <v-list-item-avatar :color="node.worker.cohort.color"></v-list-item-avatar>
                        <v-list-item-content>
                            <v-list-item-title>
                                <strong>{{node.role.name}}</strong>
                            </v-list-item-title>
                            <v-list-item-subtitle>
                                {{node.worker.full_name}}
                            </v-list-item-subtitle>   
                        </v-list-item-content>
                        <v-list-item-icon>
                            
                        </v-list-item-icon>
                    </v-list-item>
                </v-list>
            </v-card-text>

            <!----------------------------------------------------- Dialogs:  ------------------------------------->
            <!-- Add worker to workerstation dialog -->
            <v-dialog v-model="addWorkerDialog" max-width="500px">
                <v-card>
                    <v-list v-if="qualifiedWorkers.length > 0">
                        <v-list-item  v-for="worker in qualifiedWorkers" :key="worker.id" @click="addWorkerEnd(worker)">
                            {{worker.full_name}}
                        </v-list-item>
                    </v-list>
                    <v-card-title v-if="qualifiedWorkers.length == 0">No employees available for this role.</v-card-title>
                </v-card>
            </v-dialog>
        </v-card>
    </VueDraggableResizable>
</template>


<script>
import VueDraggableResizable from 'vue-draggable-resizable'
import axios from 'axios'
export default {
    components: {
        VueDraggableResizable
    },
    
    props: {
        nodeProp: Object,
    },

    data(){
		return {
            // properties of card
			width: 300,
            height: 150,
            cardMenu: false,
            node: this.nodeProp,
            // dialog: add worker
            addWorkerDialog: false,
            qualifiedWorkers: [],
		}
	},    // end data

    methods: {
		onResize: function (x, y, width, height) {
			this.x = x
			this.y = y
			this.width = width
			this.height = height
		},
		onDrag: function (x, y) {
            // give to the card on the spot
            this.x = x
            this.y = y
        },
        onDragStop(x,y){
            // write new position to db
            axios({
                method: 'patch',
                url: `${this.$store.getters.endpoints.baseAPI}/nodes/${this.node.id}/`,
                data: {
                    x: x,
                    y: y
                },
                headers: {
                    authorization: `Bearer ${this.$store.getters.accessToken}`
                },
            })
            .then(response => {
                console.log("Position written to db")
                console.log(response)
            })
            .catch(error => {console.log(error)})
        },
        toggleLock(){
            // toggle draggable
            this.node.draggable = !this.node.draggable

            // write status to db
            axios({
                method: 'patch',
                url: `${this.$store.getters.endpoints.baseAPI}/nodes/${this.node.id}/`,
                data: {
                    draggable: this.node.draggable
                },
                headers: {
                    authorization: `Bearer ${this.$store.getters.accessToken}`
                },
            })
            .then(response => {
                console.log("draggable toggled")
                console.log(response)
            })
            .catch(error => {console.log(error)})
        },
        editWorkstation(){
            alert("need editWorkstation implementation")
        },
        removeWorker(){
            axios({
                method: 'patch',
                url: `${this.$store.getters.endpoints.baseAPI}/nodecreate/${this.node.id}/`,
                data: {
                    worker: null,
                },
                headers: {
                    authorization: `Bearer ${this.$store.getters.accessToken}`
            },
            })
            .then(response => {
                console.log("Removing worker from node:")
                console.log(response)
                // update unassignedWorkers in store
                this.$store.dispatch('updateUnassignedWorkers', {remove: this.node.worker})
                // update this node's state
                this.node.worker = null
            })
            .catch(error => {console.log(error)})
        },

        // INITIALIZE UNASSIGNEDWORKERS?  In loadOrganization?

        // Or modify models/serializers so that you can see the related name field for what role each worker is in 

        addWorkerStart(){
            // get list of qualified, available workers for role
            this.$store.getters.organization.org_workers.map(x => {
                if(this.node.role.worker_ids.indexOf(x.id) != -1 && this.$store.getters.unassignedWorkers.indexOf(x)){
                    this.qualifiedWorkers.push(x)
                }
            })
            // show dialog
            this.addWorkerDialog = true
        },
        addWorkerEnd(worker){
            
            // update state
            this.node.worker = worker

            // update backend
            axios({
                method: 'patch',
                url: `${this.$store.getters.endpoints.baseAPI}/nodecreate/${this.node.id}/`,
                data: {
                    worker: worker.id
                },
                headers: {
                    authorization: `Bearer ${this.$store.getters.accessToken}`
            },
            })
            .then(response => {
                "Adding worker to "
                console.log(response)
            })
            .catch(error => {console.log(error)})

            // close dialog (which will trigger watch and reset qualifiedWorkers)
            this.addWorkerDialog = false
        },
        swapWorker(){
            alert("need swap worker implementation")
        },
	},    // end methods

    computed: {
        org(){
            return this.$store.getters.organization
        },
        rules(){
                return this.$store.getters.formRules
        },
    },

    watch: {

        // empty qualifiedWorkers whenever dialog closes
        addWorkerDialog (val){
            if(!val){
                this.qualifiedWorkers = []
            }
        }
    }
}
</script>
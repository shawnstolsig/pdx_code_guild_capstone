<template>

    <!-- A draggable, resizable, and transparent card representing a zone -->
    <VueDraggableResizable 
        :w="zone.width" :h="zone.height" 
        @dragging="onDrag" 
        @resizing="onResize" 
        @dragstop="onDragStop" 
        @resizestop="onResizestop"
        class-name="my-zone"
        :parent="false" 
        :draggable="zone.draggable" 
        :resizable="zone.draggable"
        :x="zone.x" :y="zone.y"
        :z="zone.z">
        <v-card color="transparent" :width="zone.width" :height="zone.height" flat>
            
            <!-- Transparent card toolbar for node name/menu-->
            <v-toolbar dense short flat color="transparent">
                
                <v-toolbar-title class="font-weight-bold">
                    <span>  
                        <!-- Popup menu for each workstation -->
                        <v-menu
                            v-model="zoneMenu"
                            bottom
                            right
                            transition="scale-transition"
                            origin="top left"
                            >
                            <template v-slot:activator="{ on }">
                                <v-btn icon v-on="on">
                                    <v-icon>more_vert</v-icon>
                                </v-btn>
                            </template>

                            <v-card >
                                <v-list>
                                    <v-list-item>

                                        <v-list-item-content>
                                            <v-list-item-title>{{zone.name}}</v-list-item-title>
                                        </v-list-item-content>

                                        <v-list-item-action>
                                            <v-btn icon @click="zoneMenu = false">
                                                <v-icon>mdi-close-circle</v-icon>
                                            </v-btn>
                                        </v-list-item-action>
                                    </v-list-item>
                                </v-list>

                                <v-divider></v-divider>

                                <v-list>
                                    <v-list-item @click="toggleLock">
                                        <v-list-item-action>
                                            <v-icon>{{zone.draggable ? 'lock' : 'lock_open'}}</v-icon>
                                        </v-list-item-action>
                                        <v-list-item-subtitle v-if="zone.draggable">Lock Zone</v-list-item-subtitle>
                                        <v-list-item-subtitle v-if="!zone.draggable">Unlock Zone</v-list-item-subtitle>
                                    </v-list-item>
                                    <v-list-item @click="deleteZone">
                                        <v-list-item-action>
                                            <v-icon>delete</v-icon>
                                        </v-list-item-action>
                                        <v-list-item-subtitle>Delete Zone</v-list-item-subtitle>
                                    </v-list-item>
                                </v-list>
                            </v-card>
                        </v-menu>
                    </span>
                    {{zone.name}}
                </v-toolbar-title>
            </v-toolbar>
        </v-card>
    </VueDraggableResizable>
</template>
<script>
import VueDraggableResizable from 'vue-draggable-resizable'
import 'vue-draggable-resizable/dist/VueDraggableResizable.css'
import axios from 'axios'
export default {
    components: {
        VueDraggableResizable
    },
    
    props: {
        zoneProp: Object
    },

    data(){
		return {
            // properties of zone
            zone: this.zoneProp,
            zoneMenu: false,
		}
	},    // end data

    methods: {

        // called when zone is resized.  it will update the zone based on the resize action.
    	onResize: function (x, y, width, height) {
			this.zone.x = x
			this.zone.y = y
			this.zone.width = width
			this.zone.height = height
        },
        
        // called when zone is dragged.  it will update zone based on drag action
		onDrag: function (x, y) {
            // give to the card on the spot
            this.zone.x = x
            this.zone.y = y
        },

        // called when zone stops being dragged.  writes new position to db
        onDragStop(x,y){
            // write new position to db
            axios({
                method: 'patch',
                url: `${this.$store.getters.endpoints.baseAPI}/zones/${this.zone.id}/`,
                data: {
                    x: x,
                    y: y
                },
                headers: {
                    authorization: `Bearer ${this.$store.getters.accessToken}`
                },
            })
            .then(response => {
                console.log("Zone position written to db")
                console.log(response)
            })
            .catch(error => {console.log(error)})
            console.log("implement zone dragstop" + x + y)
        },

        // called when zone stops being resized.   writes new position to db
        onResizestop(x,y,width,height){
            // write new position to db
            axios({
                method: 'patch',
                url: `${this.$store.getters.endpoints.baseAPI}/zones/${this.zone.id}/`,
                data: {
                    x: x,
                    y: y,
                    width: width,
                    height: height
                },
                headers: {
                    authorization: `Bearer ${this.$store.getters.accessToken}`
                },
            })
            .then(response => {
                console.log("Zone position written to db after resize")
                console.log(response)
            })
            .catch(error => {console.log(error)})
        },

        // toggles draggable/resizable state of zone
        toggleLock(){
            // toggle draggable
            this.zone.draggable = !this.zone.draggable

            // write status to db
            axios({
                method: 'patch',
                url: `${this.$store.getters.endpoints.baseAPI}/zones/${this.zone.id}/`,
                data: {
                    draggable: this.zone.draggable
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

        // deletes zone from workspace and updates org/workspace
        deleteZone(){
            if(confirm(`Are you sure you want to delete ${this.zone.name}?`)){
                console.log("deleting zone now")
                
                axios({
                    method: 'delete',
                    url: `${this.$store.getters.endpoints.baseAPI}/zones/${this.zone.id}/`,
                    headers: {
                        authorization: `Bearer ${this.$store.getters.accessToken}`
                },
                })
                .then(response => {
                    console.log("Zone deleted")
                    console.log(response)

                     // update...this is a bit of a heavy-handed approach since it causes whole workspace to flicker
                    let wsPk = this.$store.getters.workspace.id
                    this.$store.dispatch('dismountWorkspace')

                    // update backend/store 
                    this.$store.dispatch('loadOrganization')
                    this.$store.dispatch('loadWorkspace', {key: wsPk})
                })
                .catch(error => {console.log(error)})
            }
        },

	},    // end methods

    computed: {
        org(){
            return this.$store.getters.organization
        },
        rules(){
                return this.$store.getters.formRules
        },
    },  // end computed
}
</script>

<style>

/* Puts a solid black border around all zones */
.my-zone {
    border: solid black 3px 
}

</style>
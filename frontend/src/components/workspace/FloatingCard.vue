<template>
    <VueDraggableResizable :w="node.width" :h="node.height" @dragging="onDrag" @resizing="onResize" @dragstop="onDragStop" :parent="true" :draggable="node.draggable" :x="node.x" :y="node.y">
        <v-card>
            <v-toolbar dense short :color="node.role.color">
                <v-toolbar-title>
                    {{node.name}}
                </v-toolbar-title>
                <v-spacer></v-spacer>
                <v-btn icon @click="node.draggable = !node.draggable">
                    <v-icon>{{node.draggable ? 'lock_open' : 'lock'}}</v-icon>
                </v-btn>
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
                            <v-list-item-avatar color="node.role.">
                    
                            </v-list-item-avatar>
                            <v-list-item-content>
                                <v-list-item-title>John Leider</v-list-item-title>
                                <v-list-item-subtitle>john@vuetifyjs.com</v-list-item-subtitle>
                            </v-list-item-content>

                            <v-list-item-action>
                                <v-btn icon @click="cardMenu = false">
                                    <v-icon>mdi-close-circle</v-icon>
                                </v-btn>
                            </v-list-item-action>
                            </v-list-item>

                        </v-list>

                        <v-list>
                            <v-list-item @click="() => {}">
                            <v-list-item-action>
                                <v-icon>mdi-briefcase</v-icon>
                            </v-list-item-action>
                            <v-list-item-subtitle>john@gmail.com</v-list-item-subtitle>
                            </v-list-item>
                        </v-list>
                    </v-card>
                </v-menu>
            </v-toolbar>

            <v-card-text>
                <v-list dense>
                    <v-list-item>
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
                            <v-menu
                                v-model="moveMenu"
                                
                                right
                                transition="scale-transition"
                                origin="top left"
                                >
                                <template v-slot:activator="{ on }">
                                    <v-btn icon v-on="on">
                                        <v-icon large>compare_arrows</v-icon>
                                    </v-btn>
                                </template>

                                <v-card>
                                    <v-list>

                                        <v-list-item>
                                        <v-list-item-avatar color="node.role.">
                                
                                        </v-list-item-avatar>
                                        <v-list-item-content>
                                            <v-list-item-title>John Leider</v-list-item-title>
                                            <v-list-item-subtitle>john@vuetifyjs.com</v-list-item-subtitle>
                                        </v-list-item-content>

                                        <v-list-item-action>
                                            <v-btn icon @click="moveMenu = false">
                                                <v-icon>mdi-close-circle</v-icon>
                                            </v-btn>
                                        </v-list-item-action>
                                        </v-list-item>

                                    </v-list>

                                    <v-list>
                                        <v-list-item @click="() => {}">
                                        <v-list-item-action>
                                            <v-icon >mdi-briefcase</v-icon>
                                        </v-list-item-action>
                                        <v-list-item-subtitle>john@gmail.com</v-list-item-subtitle>
                                        </v-list-item>
                                    </v-list>
                                </v-card>
                            </v-menu>
                        </v-list-item-icon>
                    </v-list-item>
                </v-list>
               
            </v-card-text>
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
			width: 300,
            height: 150,
            cardMenu: false,
            moveMenu: false,
            node: this.nodeProp,
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
                setTimeout(() => {
                    this.$store.dispatch('loadWorkspace', 1)
                }, 300)
            })
            .catch(error => {console.log(error)})
        }
	},    // end methods

    computed: {
        org(){
            return this.$store.getters.organization
        },
        rules(){
                return this.$store.getters.formRules
        },
    }
}
</script>
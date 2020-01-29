<template>
    <VueDraggableResizable  @dragging="onDrag" @resizing="onResize" :parent="true" >
        <v-card :color="node.role.color">
            <v-toolbar dense color="node.role.color">
                <v-toolbar-title>
                    {{node.name}}
                </v-toolbar-title>
            </v-toolbar>

            <v-card-text>
                <strong>{{node.role.name}}</strong>
                <br>
                {{node.worker.full_name}}
            </v-card-text>
            <v-card-actions>
            <v-menu
                v-model="menu"
                bottom
                right
                transition="scale-transition"
                origin="top left"
                >
                <template v-slot:activator="{ on }">
                    <v-btn fab v-on="on" >
                        <v-icon>
                            mdi-plus
                        </v-icon>
                    </v-btn>
                </template>

                <v-card width="300">
                    <v-list dark>

                        <v-list-item>
                        <v-list-item-avatar color="node.role.">
                
                        </v-list-item-avatar>
                        <v-list-item-content>
                            <v-list-item-title>John Leider</v-list-item-title>
                            <v-list-item-subtitle>john@vuetifyjs.com</v-list-item-subtitle>
                        </v-list-item-content>

                        <v-list-item-action>
                            <v-btn
                            icon
                            @click="menu = false"
                            >
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
            </v-card-actions>
        </v-card>
       


        <!-- <v-card color="#F44336">
            <v-card-title>
                {{node.name}} {{node.role}}
            </v-card-title>
            <v-card-text>
                <v-chip label>
                    {{node.worker.name}}
                </v-chip>
            </v-card-text>
            <v-card-actions>
                X: {{ x }} Y: {{ y }} W: {{ width }} H: {{ height }}
            </v-card-actions>
        </v-card> -->


    </VueDraggableResizable>
</template>


<script>
import VueDraggableResizable from 'vue-draggable-resizable'
export default {
    components: {
        VueDraggableResizable
    },
    
    props: {
        x: Number,
        y: Number,
        node: Object,
    },

    data(){
		return {
			width: 600,
            height: 150,
            menu: false,
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
			this.x = x
			this.y = y
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
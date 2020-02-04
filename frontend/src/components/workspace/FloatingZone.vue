<template>
    <VueDraggableResizable 
        :w="zone.width" :h="zone.height" 
        @dragging="onDrag" 
        @resizing="onResize" 
        @dragstop="onDragStop" 
        :parent="false" 
        :draggable="zone.draggable" 
        :resizeable="zone.draggable"
        :x="zone.x" :y="zone.y"
        :z="zone.z">
        <div style="border: solid;">
                inside div
        </div>
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
        zoneProp: Object
    },

    data(){
		return {
            // properties of zone
            zone: this.zoneProp,
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
            // axios({
            //     method: 'patch',
            //     url: `${this.$store.getters.endpoints.baseAPI}/nodes/${this.node.id}/`,
            //     data: {
            //         x: x,
            //         y: y
            //     },
            //     headers: {
            //         authorization: `Bearer ${this.$store.getters.accessToken}`
            //     },
            // })
            // .then(response => {
            //     console.log("Position written to db")
            //     console.log(response)
            // })
            // .catch(error => {console.log(error)})
            console.log("implement zone dragstop" + x + y)
        },
        toggleLock(){
            // toggle draggable
            this.node.draggable = !this.node.draggable

            // write status to db
            axios({
                method: 'patch',
                url: `${this.$store.getters.endpoints.baseAPI}/nodes/${this.zone.id}/`,
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
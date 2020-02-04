<template>
    <VueDraggableResizable 
        :w="zone.width" :h="zone.height" 
        @dragging="onDrag" 
        @resizing="onResize" 
        @dragstop="onDragStop" 
        @activated="onActivated"
        @resizestop="onResizestop"
        class-name="my-zone"
        :parent="false" 
        :draggable="zone.draggable" 
        :x="zone.x" :y="zone.y"
        :z="zone.z">
        <div>
                {{zone.name}}
        </div>
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
		}
	},    // end data

    methods: {
		onResize: function (x, y, width, height) {
			this.zone.x = x
			this.zone.y = y
			this.zone.width = width
			this.zone.height = height
		},
		onDrag: function (x, y) {
            // give to the card on the spot
            this.zone.x = x
            this.zone.y = y
        },
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
        onActivated(){
            console.log('activated')
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

    mounted(){
        
    },  // end mounted

}
</script>

<style>

.my-zone {
    border: solid red 3px 
}


</style>
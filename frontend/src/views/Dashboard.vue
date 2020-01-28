<template>
	<v-container fluid class="fill-height">
		<!-- <div style="height: 500px; width: 500px; border: 1px solid red; position: relative;"> -->
			<VueDraggableResizable :w="100" :h="100" @dragging="onDrag" @resizing="onResize" :parent="true">
				<p>Hello! I'm a flexible component. You can drag me around and you can resize me.<br>
					X: {{ x }} / Y: {{ y }} - Width: {{ width }} / Height: {{ height }}</p>
			</VueDraggableResizable>
		<!-- </div> -->
			<FloatingButton />		
	</v-container>
</template>

<script>
import FloatingButton from '@/components/workspace/FloatingButton.vue'
import VueDraggableResizable from 'vue-draggable-resizable'

export default {
	name: 'dashboard',
	components: {
		FloatingButton,
		VueDraggableResizable,
	}, 


	data(){
		return {
			width: 0,
			height: 0,
			x: 0,
			y: 0,
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
	},     // end computed


	mounted(){
		this.$vuetify.theme.dark = this.$store.getters.user.darkModeEnabled
	}     // end mounted
}
</script>

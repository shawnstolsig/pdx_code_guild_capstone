<template>
    <v-speed-dial
        v-model="fab"
        bottom
        right
        direction="top"
        transition="slide-y-reverse-transition"
        >
        <template v-slot:activator>
            <v-btn v-model="fab" color="blue darken-2" dark fab>
                <v-icon v-if="fab">mdi-close</v-icon>
                <v-icon v-else>dashboard</v-icon>
            </v-btn>
        </template>

		<v-tooltip right>
			<template v-slot:activator="{ on }">
				<v-btn fab dark small color="green" v-on="on" @click="createNode">
					<v-icon>mdi-pencil</v-icon>
				</v-btn>
			</template>
			<span>Create Workstation</span>
		</v-tooltip>

		<v-tooltip right>
			<template v-slot:activator="{ on }">
				<v-btn fab dark small color="indigo" v-on="on" @click="saveWorkspace">
					<v-icon>save</v-icon>
				</v-btn>
			</template>
			<span>Save Workspace</span>
		</v-tooltip>

		<v-tooltip right>
			<template v-slot:activator="{ on }">
				<v-btn fab dark small color="red" v-on="on" @click="changeWorkspace">
					<v-icon>view_carousel</v-icon>
				</v-btn>
			</template>
			<span>Change Workspace</span>
		</v-tooltip>
    </v-speed-dial>
</template>
<script>
  export default {
    data: () => ({
		workingNodeList: [],
		fab: false,
	  	createNodeDialog: false,

    }),		// end data

    methods: {
		createNode(){

			this.createNodeDialog = true
		},
		saveWorkspace(){
			alert("implement ability to save workspace")
		},
		changeWorkspace(){
			alert("implement ability to change workspace")
		},
	},		// end methods
	
	mounted(){
		this.workingNodeList = this.$store.getters.organization.org_workspaces[0]
	},		// end mounted

	computed: {
		org(){
			return this.$store.getters.organization
		},
		rules(){
				return this.$store.getters.formRules
		},
	},     // end computed


  }
</script>
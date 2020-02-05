<template>

    <!-- Subcomponent of Settings.  This is a dialog that forces user to link account with an Organization -->
    <v-dialog v-model="popupFlag" persistent max-width="500px">

        <!-- If linking to existing org... -->
        <v-card v-if="!createMode" class="pa-3">
            <v-card-title>Select Organization</v-card-title>
            <v-card-subtitle class="mt-1">Please input your organization code before proceeding.</v-card-subtitle>
            <v-form v-model="selectFormValid" ref="orgSelectForm">
                <v-card-text>
                    <v-text-field
                        v-model="orgCode"
                        :rules="rules.code"
                        v-mask="codeMask"
                        type="text"
                        label="Organization Code"
                        required
                    ></v-text-field>
                </v-card-text>
                <v-card-actions>
                        <v-btn @click.prevent="selectOrg" :disabled="!selectFormValid" class="my-3 mr-3">Select</v-btn>  
                        <v-btn @click.prevent="createMode = true">Create new Organization</v-btn>
                </v-card-actions>
            </v-form>
        </v-card>

        <!-- If creating new org... -->
        <v-card v-if="createMode" class="pa-3">
            <v-card-title>Create New Organization</v-card-title>
            <v-card-subtitle class="mt-1">Please type in a name and description for your organization.</v-card-subtitle>
            <v-form v-model="createFormValid" ref="orgCreateForm">
                <v-card-text>
                        <v-text-field
                            v-model="orgName"
                            :rules="rules.name"
                            type="text"
                            v-mask=""
                            label="Name"
                            required
                        ></v-text-field>
                        <v-textarea
                            solo
                            v-model="orgDescription"
                            :rules="rules.description"
                            label="Description"
                            required
                        ></v-textarea>
                </v-card-text>
                <v-card-actions>
                        <v-btn @click.prevent="createOrg" :disabled="!createFormValid" class="my-3 mr-3">Create</v-btn>  
                        <v-btn @click.prevent="createMode = false">Back</v-btn>
                </v-card-actions>
            </v-form>
        </v-card>

    </v-dialog>
</template>

<script>
import axios from 'axios'
import {mask} from 'vue-the-mask'

export default {
    data(){
        return {
            popupFlag: '',
            selectFormValid: false,
            createFormValid: false,
            createMode: false,
            orgCode: '',
            orgName: '',
            orgId: '',
            organizations: '',
            orgDescription: '',
            // this is the format for a uuid4
            codeMask: 'XXXXXXXX-XXXX-XXXX-XXXX-XXXXXXXXXXXX',
        }
    },      // end data

    // for uuid mask
    directives: {mask},

    methods: {

        // For selecting an existing org and linking it to user's account
        selectOrg(){

            // if org id is not set (if user is not coming from org creation)
            if(!this.orgId){
                // using input code, find pk of organization
                for(let i=0; i < this.organizations.length; i++){
                    let thisOrg = this.organizations[i].code
                    if(thisOrg == this.orgCode){
                        this.orgId = this.organizations[i].id
                    }
                }
                if(!this.orgId){
                    alert("Organization not found, please re-enter code.")
                    return
                } 
            }

            if(this.selectFormValid || this.createFormValid){
                // Patch the user's organization with selected org
                axios({
                    method: 'patch',
                    url: `${this.$store.getters.endpoints.baseAPI}/managers/${this.$store.getters.user.userId}/`,
                    data: {
                        organization: this.orgId
                    },
                    headers: {
                        authorization: `Bearer ${this.$store.getters.accessToken}`
                    }
                })
                .then(response => {
                    console.log(response)
                    this.$store.dispatch('setUserOrganization', this.orgId)
                    this.popupFlag = false
                })
                .catch(error => {
                    console.log("Could not patch User's organization.  Error:")
                    console.log(error)
                })
            }
        },

        // For creating a new org and linking it to the user's account
        createOrg(){
            if(this.createFormValid){
                // Create a new organization, post to db
                axios({
                    method: 'post',
                    url: `${this.$store.getters.endpoints.baseAPI}/organizations/`,
                    data: {
                        name: this.orgName,
                        description: this.orgDescription,
                    },
                    headers: {
                        authorization: `Bearer ${this.$store.getters.accessToken}`
                    }
                })
                .then(response => {
                    console.log(response)
                    this.orgId = response.data.id
                    alert(`${this.orgName} created!`)
                    this.selectOrg()
                })
                .catch(error => {
                    console.log("Could not patch User's organization.  Error:")
                    console.log(error)
                })
            }
        }
    },      // end methods

    computed: {			
		org(){
			return this.$store.getters.organization
        },
        rules(){
            return this.$store.getters.formRules
        },
	},		// end computed

    // figure out of if popup should be shown
    created(){
        // set flag
        this.popupFlag = !this.$store.getters.user.organization

        // get list of Organization IDs and UUIDs
        axios({
            method: 'get',
            url: `${this.$store.getters.endpoints.baseAPI}/organizationsuuid/`,
            headers: {
                authorization: `Bearer ${this.$store.getters.accessToken}`
            }
        })
        .then(response => this.organizations = response.data)
        .catch(error => console.log(error))
    }       // end created
}
</script>
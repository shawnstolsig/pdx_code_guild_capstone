<template>
    <v-dialog v-model="popupFlag" persistent max-width="500px">
        <v-card v-if="!createMode" class="pa-3">
            <v-card-title>Select Organization</v-card-title>
            <v-card-subtitle class="mt-1">Please input your organization code before proceeding.</v-card-subtitle>
            <v-form v-model="selectFormValid" ref="orgSelectForm">
                <v-card-text>
                    <v-text-field
                        v-model="orgCode"
                        :rules="validationRules.code"
                        v-mask="codeMask"
                        type="text"
                        label="Organization Code"
                        required
                    ></v-text-field>
                </v-card-text>
                <v-card-actions>
                        <v-btn @click.prevent="selectOrg" :disabled="!selectFormValid" class="my-3 mr-3">Select</v-btn>  
                        <v-btn @click.prevent="createMode = true">Create new Organization...</v-btn>
                </v-card-actions>
            </v-form>
        </v-card>
        <v-card v-if="createMode" class="pa-3">
            <v-card-title>Create New Organization</v-card-title>
            <v-card-subtitle class="mt-1">Please type in a name and description for your organization.</v-card-subtitle>
            <v-form v-model="createFormValid" ref="orgCreateForm">
                <v-card-text>
                        <v-text-field
                            v-model="orgName"
                            :rules="validationRules.name"
                            type="text"
                            v-mask=""
                            label="Name"
                            required
                        ></v-text-field>
                        <v-textarea
                            solo
                            v-model="orgDescription"
                            :rules="validationRules.description"
                            label="Description"
                            required
                        ></v-textarea>
                </v-card-text>
                <v-card-actions>
                        <v-btn @click.prevent="createOrg" :disabled="!createFormValid" class="my-3 mr-3">Create</v-btn>  
                        <v-btn @click.prevent="createMode = false">Back...</v-btn>
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
            codeMask: 'XXXXXXXX-XXXX-XXXX-XXXX-XXXXXXXXXXXX',
            validationRules:{
                code: [ v => !!v || 'Please input Organization code.' ],
                name: [
                    v => !!v || 'Name is required.',
                    v => (v && v.length) <= 30 || 'Name must be less than 30 characters.',
                    v => (v && v.length) >= 3 || 'Name must be at least 3 characters.',
                ],
                description: [
                    v => !!v || 'Description is required.',
                    v => (v && v.length) >= 3 || 'Name must be at least 3 characters.',
                ],
            }
        }
    },
    directives: {mask},
    methods: {
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
        createOrg(){
            if(this.createFormValid){
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
                // Set org as user's org
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
    },
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
    }
}
</script>
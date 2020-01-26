<template>
    <v-dialog v-model="popupFlag" persistent max-width="500px">
        <v-card class="pa-3">
            <v-card-title>Create New Cohort</v-card-title>
            <v-card-subtitle class="mt-1">Please type in a name and description for your cohort.</v-card-subtitle>
            <v-form v-model="createFormValid" ref="cohortCreateForm">
                <v-card-text>
                        <v-text-field
                            v-model="cohortName"
                            :rules="validationRules.name"
                            type="text"
                            label="Name"
                            required
                        ></v-text-field>
                        <v-textarea
                            solo
                            v-model="cohortDescription"
                            :rules="validationRules.description"
                            label="Description"
                            required
                        ></v-textarea>
                </v-card-text>
                <v-card-actions>
                        <v-btn @click.prevent="createCohort" :disabled="!createFormValid" class="my-3 mr-3">Create</v-btn>  
                        <v-btn @click.prevent="disablePopup">Back</v-btn>
                </v-card-actions>
            </v-form>
        </v-card>
    </v-dialog>
</template>

<script>
import axios from 'axios'

export default {
    props: {
        popupFlag: Boolean
    },
    data(){
        return {
            popupFlag: '',
            createFormValid: false,
            cohortName: '',
            cohortDescription: '',
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
    },      // End Data
    methods: {
        createCohort(){

        },
        disablePopup(){
            console.log("disabling popup")
            this.popupFlag = false;
        }
    },      // End Methods
    created(){

    }       // End Created()
}
</script>
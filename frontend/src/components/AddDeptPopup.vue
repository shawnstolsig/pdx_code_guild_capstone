<template>
    <v-row justify="center">
        <v-dialog v-model="dialog" persistent max-width="500">
            <template v-slot:activator="{ on }">
                <v-btn color="primary" dark v-on="on">Open Dialog</v-btn>
            </template>
            <v-card class="pa-3">
                <v-card-title>Create New Department</v-card-title>
                <v-card-subtitle class="mt-1">Please type in a name and description for your department.</v-card-subtitle>
                <v-form v-model="createFormValid" ref="deptCreateForm">
                    <v-card-text>
                            <v-text-field
                                v-model="deptName"
                                :rules="validationRules.name"
                                type="text"
                                label="Name"
                                required
                            ></v-text-field>
                            <v-textarea
                                solo
                                v-model="deptDescription"
                                :rules="validationRules.description"
                                label="Description"
                                required
                            ></v-textarea>
                    </v-card-text>
                    <v-card-actions>
                            <v-btn @click.prevent="createDept" :disabled="!createFormValid" class="my-3 mr-3">Create</v-btn>  
                    </v-card-actions>
                </v-form>
            </v-card>
        </v-dialog>
    </v-row>
</template>

<script>
import axios from 'axios'

export default {
    prop: {
        value: Boolean
    }
    data(){
        return {
            createFormValid: false,
            deptName: '',
            deptDescription: '',
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
        createDept(){

        },
    },      // End Methods
    created(){

    }       // End Created()
}
</script>
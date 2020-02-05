<template>
    <v-container>

        <!-- Start of Account Form, prepopulated with user's data -->
        <v-form v-model="accountFormValidity" ref='accountForm' dense>
            <v-row>
                <v-col cols="12" md="6">
                <v-text-field
                    v-model="account.username"
                    :rules="rules.name"
                    :counter="30"
                    type="text"
                    label="Username"
                    required
                ></v-text-field>
                </v-col>
            </v-row>
            <v-row>
                <v-col cols="12" md="6">
                <v-text-field
                    v-model="account.firstName"
                    :rules="rules.name"
                    :counter="30"
                    type="text"
                    label="First name"
                    required
                ></v-text-field>
                </v-col>
            </v-row>
            <v-row>
                <v-col cols="12" md="6">
                <v-text-field
                    v-model="account.lastName"
                    :rules="rules.name"
                    :counter="30"
                    type="text"
                    label="Last name"
                    required
                ></v-text-field>
                </v-col>
            </v-row>
            <v-row>
                <v-col cols="12" md="6">
                <v-text-field
                    v-model="account.email"
                    :rules="rules.email"
                    type="email"
                    label="E-mail"
                    required
                ></v-text-field>
                </v-col>
            </v-row>
            <v-row>
                <v-col cols="12" md="6">
                    <v-text-field 
                    disabled
                    v-model="org.code"
                    outlined
                    :label="org.name + ' Organization Code'"
                    >
                    </v-text-field>
                </v-col>
            </v-row>
            <v-row>
                <v-card flat>
                    <v-card-text>
                        <v-switch v-model="$vuetify.theme.dark" primary	label="Dark Mode"/>
                    </v-card-text>
                </v-card>
            </v-row>
            <v-row>
                <v-btn 
                class="mx-5" 
                @click.prevent="saveAccountSettings" 
                type="submit" 
                :disabled="!accountFormValidity"
                color="success"
                >Save
                </v-btn>
            </v-row>

        </v-form>
    </v-container>
</template>

<script>

export default {
	data: () => ({
		// Account form vars
		accountFormValidity: false, 
		account: {
			username: "",
			firstName: "",
			lastName: "",
			email: "",
		}, 
	}),     // end data

	methods: {

		// Save account settings based on input to the Account Settings tab
		saveAccountSettings(){
            // Only submit update if form is valid
			if (this.$refs.accountForm.validate()){
				const payload = {
					userId: this.$store.getters.user.userId,
					username: this.account.username,
					firstName: this.account.firstName,
					lastName: this.account.lastName,
					fullName: `${this.account.firstName} ${this.account.lastName}`,
					email: this.account.email,
					darkModeEnabled: this.$vuetify.theme.dark,
				}
				this.$store.dispatch('updateUserBackend', payload)
			} else {
				alert('Invalid form input.')
			}
		},
	},      /// end methods	

	computed: {			
		validOrg(){
			return !!this.$store.getters.user.organization
		},
		org(){
			return this.$store.getters.organization
        },
        rules(){
            return this.$store.getters.formRules
        },
	},		// end computed

    // pre-load user's info into form
	mounted() {

		let user = this.$store.getters.user
		this.account.username = user.username
		this.account.email = user.email
		// note that for form model to work correctly, must be empty string...not undefined/null
		this.account.firstName = (user.firstName === undefined) ? "" : user.firstName
		this.account.lastName = (user.firstName === undefined) ? "" : user.lastName
	},		// end mounted
}
</script>
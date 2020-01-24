<template>
  <v-card>
		<v-toolbar flat dark color="primary">
			<v-toolbar-title>Settings</v-toolbar-title>
		</v-toolbar>
		<v-tabs>
			<v-tab v-for="link in links" :key="link.text">
				<v-icon left>{{link.icon}}</v-icon>
				{{link.text}}
			</v-tab>

			<v-tab-item> <!-- Start of Account -->
				<v-form v-model="formValidity" ref='accountForm' dense>
					<v-container>
						<v-row>
							<v-col cols="12" md="6">
							<v-text-field
								v-model="account.username"
								:rules="validationRules.name"
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
								:rules="validationRules.name"
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
								:rules="validationRules.name"
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
								:rules="validationRules.email"
								type="email"
								label="E-mail"
								required
							></v-text-field>
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
							:disabled="!formValidity"
							>
								Save
							</v-btn>
						</v-row>

					</v-container>
				</v-form>
			</v-tab-item>  <!-- End of Account -->

			
			<v-tab-item>	<!-- Start of Department -->
				<v-card flat>
					<v-card-text>

					</v-card-text>
				</v-card>
			</v-tab-item>	<!-- End of Department -->
		</v-tabs>
	</v-card>
</template>


<script>

export default {
	name: 'settings',

	data: () => ({
		links: [
			{text: 'Account', icon: 'mdi-account'},
			{text: 'Department', icon: 'business'},
		],
		account: {
			username: "",
			firstName: "",
			lastName: "",
			email: "",
		}, 
		formValidity: false, 
		validationRules: {
			name: [
				v => !!v || 'Name is required.',
				v => (v && v.length) <= 30 || 'Name must be less than 30 characters.',
				v => (v && v.length) >= 3 || 'Name must be at least 3 characters.',
			],
			email: [
				v => !!v || 'E-mail is required.',
				// v => /.+@.+/.test(v) || 'E-mail must be valid.',
				v => (v && v.indexOf("@") !== 0) || 'Email should have username.',
				v => (v && !!v.includes("@")) || 'Email should have @ sybol.',
				v => (v && v.indexOf(".") - v.indexOf('@') > 1)|| 'Email should have have domain.',
				v => (v && !!v.indexOf(".")) || 'Email should have have domain.',
				v => (v && v.indexOf('.') <= v.length - 3) || 'Email should contain a valid domain extension.'
			],
		},
	}),     // end data

	methods: {
		saveAccountSettings(){
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

	},		// end computed
	mounted() {
    	this.$vuetify.theme.dark = this.$store.getters.user.darkModeEnabled
		let user = this.$store.getters.user
		console.log("populating settings with user info:")
		console.log(user)
		this.account.username = user.username
		this.account.email = user.email
		// note that for form model to work correctly, must be empty string...not undefined/null
		this.account.firstName = (user.firstName === undefined) ? "" : user.firstName
		this.account.lastName = (user.firstName === undefined) ? "" : user.lastName
	},		// end mounted
}
</script>
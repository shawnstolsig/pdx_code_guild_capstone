<template>
  <v-card>
		<v-toolbar flat dark color="primary">
			<v-toolbar-title>Settings</v-toolbar-title>
		</v-toolbar>
		<v-tabs>
		<v-tab>
			<v-icon left>mdi-account</v-icon>
			Account
		</v-tab>
		<v-tab>
			<v-icon left>business_center</v-icon>
			Manager
		</v-tab>
		<v-tab>
			<v-icon left>business</v-icon>
			Department
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

      <v-tab-item>
        <v-card flat>
          <v-card-text>

          </v-card-text>
        </v-card>
      </v-tab-item>
      <v-tab-item>
        <v-card flat>
          <v-card-text>

          </v-card-text>
        </v-card>
      </v-tab-item>
    </v-tabs>
  </v-card>
</template>


<script>
import axios from "axios";

export default {
	name: 'settings',

	data: () => ({
		links: [
			{text: 'User Settings', action: '', icon: 'account_box'},
			{text: 'Department Settings', action: '', icon: 'group'},
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
				
				// update User model
				alert("Patching User Model")
				axios({
					method: 'patch',
					url: `${this.$store.getters.endpoints.baseAPI}/users/${this.$store.getters.userInfo.userId}/`,
					data: {
						username: this.account.username,
						first_name: this.account.firstName,
						last_name: this.account.lastName,
						email: this.account.email,
					},
					headers: {
						authorization: `Bearer ${this.$store.getters.accessToken}`
					}
				}).then(response => {
					console.log(response)
				})

				// update Manager model
				alert("Patching Manager Model")
				axios({
					method: 'patch',
					url: `${this.$store.getters.endpoints.baseAPI}/managers/${this.$store.getters.userInfo.userId}/`,
					data: {
						full_name: `${this.account.firstName} ${this.account.lastName}`,
						darkModeEnabled: this.$vuetify.theme.dark,
					},
					headers: {
						authorization: `Bearer ${this.$store.getters.accessToken}`
					}
				}).then(response => {
					console.log(response)
				})

				// update auth user
				let userInfo = this.$store.getters.userInfo
				const payload = {
					authUser: {
						userId: userInfo.userId,
						username: this.account.username,
						lastLogin: userInfo.last_login,
						firstName: this.account.first_name,
						lastName: this.account.last_name,
						isActive: userInfo.is_active,
						dateJoined: userInfo.date_joined,
						email: this.account.email,
						darkModeEnabled: this.account.darkModeEnabled,
					},
					isAuthenticated: true,
				}
				this.$store.dispatch('updateAuthUser', payload)
			} else {
				alert('Invalid form input.')
			}
		},
	},      /// end methods	

	computed: {			

	},		// end computed
	
	created() {
		let userInfo = this.$store.getters.userInfo
		this.account.username = userInfo.username
		this.account.email = userInfo.email
		// note that for form model to work correctly, must be empty string...not undefined/null
		this.account.firstName = (userInfo.firstName === undefined) ? "" : userInfo.firstName
		this.account.lastName = (userInfo.firstName === undefined) ? "" : userInfo.lastName
	},		// end created
}
</script>
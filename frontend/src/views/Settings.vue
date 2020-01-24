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
					<v-btn 
					class="mx-5" 
					@click="saveAccountSettings" 
					type="submit" 
					:disabled="!formValidity"
					>
						Save
					</v-btn>
				</v-row>
				<v-row>
					<v-card flat>
						<v-card-text>
							<v-switch v-model="$vuetify.theme.dark" primary	label="Dark"/>
						</v-card-text>
					</v-card>
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
export default {
	name: 'settings',

	data: () => ({
		links: [
			{text: 'User Settings', action: '', icon: 'account_box'},
			{text: 'Department Settings', action: '', icon: 'group'},
		],
		account: {
			userId: 'test',
			username: 'test',
			firstName: 'test',
			lastName: 'test',
			email: 'test',
		}, 
		formValidity: false, 
		validationRules: {
			name: [
				v => !!v || 'Name is required.',
				v => v.length <= 30 || 'Name must be less than 30 characters.',
				v => v.length >= 3 || 'Name must be at least 3 characters.',
			],
			email: [
				v => !!v || 'E-mail is required.',
				// v => /.+@.+/.test(v) || 'E-mail must be valid.',
				v => v.indexOf("@") !== 0 || 'Email should have username.',
				v => !!v.includes("@") || 'Email should have @ sybol.',
				v => v.indexOf(".") - v.indexOf('@') > 1|| 'Email should have have domain.',
				v => !!v.indexOf(".") || 'Email should have have domain.',
				v => v.indexOf('.') <= v.length - 3 || 'Email should contain a valid domain extension.'
			],
		},
	}),     // end data

	methods: {
		saveAccountSettings(){
			if (this.$refs.accountForm.validate()){
				alert('form is valid')
			} else {
				alert('saving account settings')
			}

		},
	},      /// end methods	

	computed: {

	},		// end computed
	
	created() {
		this.account = this.$store.getters.userInfo
	},		// end created
}
</script>
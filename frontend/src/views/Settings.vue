<template>
	<v-container>
		<OrgPopup></OrgPopup>

		<v-toolbar flat dark color="primary">
			<v-toolbar-title>Settings</v-toolbar-title>
		</v-toolbar>
		<v-tabs>
			<v-tab v-for="link in links" :key="link.text">
				<v-icon left>{{link.icon}}</v-icon>
				{{link.text}}
			</v-tab>

			<v-tab-item>	<!-- Start of Organization Settings -->
				<v-container>
					<v-row v-if="!validOrg">
						<v-col cols="3">
							<v-card flat>
								<v-card-text>
									No organization selected.
								</v-card-text>
							</v-card>
						</v-col>
					</v-row>
					<!-- Department Card -->
					<v-row v-if="validOrg">
						<v-col cols="6">
							<v-card>
								<v-card-title>
									Departments
								</v-card-title>
								<v-card-text>
									<v-list>
									    <v-list-item v-for="department in org.org_departments" :key="department.id">
											<v-list-item-content>
												<v-list-item-title>{{department.name}}</v-list-item-title>
											</v-list-item-content>
										</v-list-item>
									    <v-list-item v-if="org.org_departments.length == 0">
											<v-list-item-content>
												<v-list-item-title class="grey--text">(none)</v-list-item-title>
											</v-list-item-content>
										</v-list-item>
									</v-list>
								</v-card-text>
								<v-card-actions>
									<!-- Dialog for adding Department -->
									<v-dialog v-model="deptDialog" max-width="500">
										<template v-slot:activator="{ on }">
											<v-btn v-on="on">Add</v-btn>
										</template>
										<v-card class="pa-3">
											<v-card-title>Create New Department</v-card-title>
											<v-card-subtitle class="mt-1">Please type in a name and description for your department.</v-card-subtitle>
											<v-form v-model="deptCreateFormValidity" ref="deptCreateForm">
												<v-card-text>
														<v-text-field
															v-model="newDept.name"
															:rules="validationRules.name"
															type="text"
															label="Name"
															required
														></v-text-field>
														<v-textarea
															solo
															v-model="newDept.description"
															:rules="validationRules.description"
															label="Description"
															required
														></v-textarea>
												</v-card-text>
												<v-card-actions>
														<v-btn @click.prevent="addDepartment" :disabled="!deptCreateFormValidity" class="my-3 mr-3">Add</v-btn>  
												</v-card-actions>
											</v-form>
										</v-card>
									</v-dialog>
								</v-card-actions>
							</v-card>
						</v-col>
						<!-- Cohort Card -->
						<v-col cols="6">
							<v-card>
								<v-card-title>
									Cohorts
								</v-card-title>
								<v-card-text>
									<v-list>

									    <v-list-item v-for="cohort in org.org_cohorts" :key="cohort.id">
											<v-list-item-content>
												<v-list-item-title>{{cohort.name}}</v-list-item-title>
											</v-list-item-content>
										</v-list-item>
									    <v-list-item v-if="org.org_cohorts.length == 0">
											<v-list-item-content>
												<v-list-item-title class="grey--text">(none)</v-list-item-title>
											</v-list-item-content>
										</v-list-item>


									</v-list>
								</v-card-text>
								<v-card-actions>
									<!-- Dialog for adding Cohort -->
									<v-dialog v-model="cohortDialog" max-width="500">
										<template v-slot:activator="{ on }">
											<v-btn v-on="on">Add</v-btn>
										</template>
										<v-card class="pa-3">
											<v-card-title>Create New Cohort</v-card-title>
											<v-card-subtitle class="mt-1">Please type in a name and description for your cohort.</v-card-subtitle>
											<v-form v-model="cohortCreateFormValidity" ref="cohortCreateForm">
												<v-card-text>
														<v-text-field
															v-model="newCohort.name"
															:rules="validationRules.name"
															type="text"
															label="Name"
															required
														></v-text-field>
														<v-textarea
															solo
															v-model="newCohort.description"
															:rules="validationRules.description"
															label="Description"
															required
														></v-textarea>
												</v-card-text>
												<v-card-actions>
														<v-btn @click.prevent="addCohort" :disabled="!cohortCreateFormValidity" class="my-3 mr-3">Add</v-btn>  
												</v-card-actions>
											</v-form>
										</v-card>
									</v-dialog>

								</v-card-actions>
							</v-card>
						</v-col>
					</v-row>
				</v-container>

			</v-tab-item>	<!-- End of Organization Settings -->
			
			<v-tab-item> <!-- Start of Account -->
				<v-form v-model="accountFormValidity" ref='accountForm' dense>
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
							:disabled="!accountFormValidity"
							color="success"
							>
								Save
							</v-btn>
						</v-row>

					</v-container>
				</v-form>
			</v-tab-item>  <!-- End of Account -->

		</v-tabs>
	</v-container>
</template>


<script>
import OrgPopup from '../components/OrgPopup'
import axios from 'axios'

export default {
	name: 'settings',
	components: { 
		OrgPopup, 
	},
	data: () => ({
		links: [
			{text: 'Organization', icon: 'business'},
			{text: 'Account', icon: 'mdi-account'},
		],
		// Account form vars
		accountFormValidity: false, 
		account: {
			username: "",
			firstName: "",
			lastName: "",
			email: "",
		}, 
		// Dept create form/dialog vars
		deptDialog: false,
		deptCreateFormValidity: false,
		newDept: {
			name: '',
			description: '',
		},
		// Cohort create form/dialog vars
		cohortDialog: false,
		cohortCreateFormValidity: false,
		newCohort: {
			name: '',
			description: '',
		},
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

		// Save account settings based on input to the Account Settings tab
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

		// Create a department on button press from Organization Settings tab
		addDepartment(){
			console.log("creating dept")
			axios({
				method: 'post',
				url: `${this.$store.getters.endpoints.baseAPI}/departments/`,
				data: {
					name: this.newDept.name,
					description: this.newDept.description,
					organization: this.$store.getters.organization.id
				},
				headers: {
					authorization: `Bearer ${this.$store.getters.accessToken}`
				},
			})
			.then(response => {
				console.log(response)
				// reload organization
				this.$store.dispatch('loadOrganization')
				this.deptDialog = false
			})
			.catch(error => {console.log(error)})
		},

		// Create a department on button press from Organization Settings tab
		addCohort(){
			console.log("creating cohort")
			axios({
				method: 'post',
				url: `${this.$store.getters.endpoints.baseAPI}/cohorts/`,
				data: {
					name: this.newCohort.name,
					description: this.newCohort.description,
					organization: this.$store.getters.organization.id
				},
				headers: {
					authorization: `Bearer ${this.$store.getters.accessToken}`
				},
			})
			.then(response => {
				console.log(response)
				// reload organization
				this.$store.dispatch('loadOrganization')
				this.cohortDialog = false
			})
			.catch(error => {console.log(error)})
		},
	},      /// end methods	

	computed: {			
		validOrg(){
			return !!this.$store.getters.user.organization
		},
		org(){
			return this.$store.getters.organization
		},
	},		// end computed

	created() {
		this.$vuetify.theme.dark = this.$store.getters.user.darkModeEnabled

		let user = this.$store.getters.user
		this.account.username = user.username
		this.account.email = user.email
		// note that for form model to work correctly, must be empty string...not undefined/null
		this.account.firstName = (user.firstName === undefined) ? "" : user.firstName
		this.account.lastName = (user.firstName === undefined) ? "" : user.lastName
	},		// end mounted
}
</script>

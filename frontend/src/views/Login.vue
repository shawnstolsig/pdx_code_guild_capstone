<template lang="html">
	<v-container class="fill-height" fluid>
		<v-row align="center" justify="center">
			<v-col cols="12" sm="8" md="4">

				<!-- Dialog box for logging in or registering -->
				<v-card class="elevation-12">

					<v-toolbar dark	flat>
                		<v-toolbar-title v-if="registrationMode">Register</v-toolbar-title>
                		<v-toolbar-title v-else>Login</v-toolbar-title>
                		<v-spacer/>
                	</v-toolbar>

					<v-card-text>
						<!-- User registration/login form.  Additional fields toggled by registrationMode -->
						<v-form dense v-model="formValidity" ref="registrationForm">
							<v-text-field
								v-if="!registrationMode"
								label="Username"
								name="username"
								prepend-icon="person"
								type="text"
								v-model="username"
							/>
							<v-text-field
								v-if="registrationMode"
								label="Username"
								name="username"
								prepend-icon="person"
								type="text"
								v-model="username"
								:rules="rules.name"
								counter="30"
							/>
							<v-text-field
								v-if="registrationMode"
								label="First Name"
								name="first_name"
								prepend-icon="person"
								type="text"
								v-model="firstName"
								:rules="rules.name"
								counter="30"
							/>
							<v-text-field
								v-if="registrationMode"
								label="Last Name"
								name="last_name"
								prepend-icon="person"
								type="text"
								v-model="lastName"
								:rules="rules.name"
								counter="30"
							/>
							<v-text-field
								v-if="registrationMode"
								label="Email"
								name="email"
								prepend-icon="email"
								type="text"
								v-model="email"
								:rules="rules.email"
							/>
							<v-text-field
								id="password"
								label="Password"
								name="password"
								prepend-icon="lock"
								:append-icon="showPassword ? 'mdi-eye' : 'mdi-eye-off'"
								v-model="password"
								:type="showPassword ? 'text' : 'password'"
								:rules="rules.password"
								@click:append="showPassword = !showPassword"
							/>
							<v-text-field
								v-if="registrationMode"
								id="password2"
								label="Re-enter Password"
								name="password2"
								prepend-icon="lock"
								:append-icon="showPassword2 ? 'mdi-eye' : 'mdi-eye-off'"
								v-model="password2"
								:type="showPassword2 ? 'text' : 'password'"
								:rules="password2Validation"
								@click:append="showPassword2 = !showPassword2"
							/>
							<v-checkbox label="Agree to terms and conditions" v-if="registrationMode" v-model="termsCheckbox" required></v-checkbox>
						</v-form>
					</v-card-text>			

              		<v-card-actions>
                		<v-btn color="primary" v-if="!registrationMode" @click="registrationMode = !registrationMode">Register</v-btn>
                		<v-btn color="primary" v-if="registrationMode" @click="registrationMode = !registrationMode">Back to login...</v-btn>
                		<v-spacer />
                		<v-btn color="success" v-if="!registrationMode" @click="login">Login</v-btn>
                		<v-btn color="success" v-if="registrationMode" @click="register" :disabled="!(formValidity && termsCheckbox)">Register</v-btn>
              		</v-card-actions>

				</v-card>
			</v-col> 
		</v-row>
	</v-container>
</template>

<script>

export default {
	name: 'login',
    data () {
        return {
            username: '',
			password: '',
			password2: '',
			firstName: '',
			lastName: '',
			email: '',
			showPassword: false,
			showPassword2: false,
			registrationMode: false,
			formValidity: false,
			termsCheckbox: false,
			// This is specified rule instead of the store so that there is easy access to this.password
			password2Validation:  [
				v => !!v || 'Password is required.',
				v => (v && v.length) >= 6 || 'Password must be at least 6 characters.',
				() => (this.password == this.password2) || 'Passwords must be the same.',
            ],
		}
	},		// end data
	
    methods: {

        // log user in
        login () {
            // create payload from user input 
            const payload = {
                username: this.username,
                password: this.password
            }

            // call API to obtain token and log in user
            this.$store.dispatch("login", payload);
		},

		// create new user 
		register(){
			const payload = {
				username: this.username,
				password: this.password2,
				firstName: this.firstName,
				lastName: this.lastName,
				fullName: `${this.firstName} ${this.lastName}`,
				email: this.email,
				darkModeEnabled: false,
			}

			this.$store.dispatch('register', payload)
		}
	},		// end methods

	computed: {
		baseUrl(){
			return this.$store.getters.endpoints.baseURL
		},
		rules(){
            return this.$store.getters.formRules
        },
	},		// end computed

	// set light mode as default
	mounted() {
		this.$vuetify.theme.dark = false
	}		// end mounted

}
</script>

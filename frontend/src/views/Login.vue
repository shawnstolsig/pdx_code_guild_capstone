<template lang="html">
	<v-container class="fill-height" fluid>
		<v-row align="center" justify="center">
			<v-col cols="12" sm="8" md="4">
				<v-card class="elevation-12">

					<v-toolbar dark	flat>
                		<v-toolbar-title v-if="registrationMode">Register</v-toolbar-title>
                		<v-toolbar-title v-else>Login</v-toolbar-title>
                		<v-spacer/>
                	</v-toolbar>

					<v-card-text>
						<v-form>
							<v-text-field
								label="Username"
								name="username"
								prepend-icon="person"
								type="text"
								v-model="username"
							/>
							<v-text-field
								v-if="registrationMode"
								label="First Name"
								name="first_name"
								prepend-icon="person"
								type="text"
								v-model="firstName"
							/>
							<v-text-field
								v-if="registrationMode"
								label="Last Name"
								name="last_name"
								prepend-icon="person"
								type="text"
								v-model="lastName"
							/>
							<v-text-field
								v-if="registrationMode"
								label="Email"
								name="email"
								prepend-icon="email"
								type="text"
								v-model="email"
							/>
							<v-text-field
								id="password"
								label="Password"
								name="password"
								prepend-icon="lock"
								:append-icon="showPassword ? 'mdi-eye' : 'mdi-eye-off'"
								v-model="password"
								:type="showPassword ? 'text' : 'password'"
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
								@click:append="showPassword2 = !showPassword2"
							/>
						</v-form>
					</v-card-text>			

              		<v-card-actions>
                		<!-- <v-btn color="primary" @click="register">Register</v-btn> -->
                		<v-btn color="primary" v-if="!registrationMode" @click="registrationMode = !registrationMode">Register</v-btn>
                		<v-btn color="primary" v-if="registrationMode" @click="registrationMode = !registrationMode">Back to login...</v-btn>
                		<v-spacer />
                		<v-btn color="success" v-if="!registrationMode" @click="authenticate">Login</v-btn>
                		<v-btn color="success" v-if="registrationMode" @click="register">Register</v-btn>
              		</v-card-actions>

				</v-card>
			</v-col> 
		</v-row>
	</v-container>
</template>

<script>
import axios from 'axios'
export default {
	name: 'login',
    data () {
        return {
            username: null,
			password: null,
			password2: null,
			firstName: null,
			lastName: null,
			email: null,
			showPassword: false,
			showPassword2: false,
			registrationMode: false
        }
    },
    methods: {

        // log user in
        authenticate () {

            // create payload from user input 
            const payload = {
                username: this.username,
                password: this.password
            }

            // call API to obtain token and log in user
            this.$store.dispatch("obtainToken", payload);
		},

		// create new user 
		register(){
			alert("trying to register")
			const payload = {
				username: this.username,
				password: this.password2,
				first_name: this.firstName,
				last_name: this.lastName,
				email: this.email,
			}
			axios({
				method: 'post',
				url: `${this.baseUrl}/users/`,
				params: payload,
			}).then(response => console.log(response))
		}
	},
	computed: {
		baseUrl(){
			return this.$store.state.endpoints.baseUrl
		}
	}
}
</script>

<style lang="css">
</style>
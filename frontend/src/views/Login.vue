<template lang="html">
	<v-container class="fill-height" fluid>
		<v-row align="center" justify="center">
			<v-col cols="12" sm="8" md="4">
				<v-card class="elevation-12">
					<v-toolbar dark	flat>
                		<v-toolbar-title>Login</v-toolbar-title>
                		<v-spacer/>
                	</v-toolbar>
					<v-card-text>
						<v-form>
							<v-text-field
								label="Username"
								name="login"
								prepend-icon="person"
								type="text"
								v-model="username"
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
						</v-form>
					</v-card-text>				
              		<v-card-actions>
                		<v-btn color="primary" @click="register">Register</v-btn>
                		<v-spacer />
                		<v-btn color="success" @click="authenticate">Login</v-btn>
              		</v-card-actions>
				</v-card>
			</v-col> 
		</v-row>
	</v-container>
</template>

<script>
// import axios from 'axios'
export default {
    name: 'login',
    data () {
        return {
            username: null,
			password: null,
			showPassword: false
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
			alert("trying to register!")
		}
    }
}
</script>

<style lang="css">
</style>
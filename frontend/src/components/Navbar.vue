<template>
    <nav>
        <v-app-bar flat app dark>
            
            <v-toolbar-title class="text-uppercase grey--text">
                <span class="font-weight-light text-lowercase">shift</span>
                <span>MANAGR</span>
            </v-toolbar-title>

            <v-spacer></v-spacer>

            <v-btn v-if="authenticated" text color="grey" to="/">
                <span>Dashboard</span>
                <v-icon right >home</v-icon>
            </v-btn>
            <v-btn text color="grey" to="/jwttest">
                <span>Test JWT</span>
                <v-icon right >lock</v-icon>
            </v-btn>
            <v-btn v-if="!authenticated" text color="grey" to="/login">
                <span>Sign In</span>
                <v-icon right >perm_identity</v-icon>
            </v-btn>
            <v-btn v-if="authenticated" text color="grey" @click="logOut">
                <span>Sign Out</span>
                <v-icon right >exit_to_app</v-icon>
            </v-btn>

        </v-app-bar>
    </nav>
</template>


<script>


export default {
    data(){
        return {
            links: []
        }
    },
    methods: {
        logOut(){
            this.$store.dispatch('deleteToken')
        }
    },
    computed: {
        authenticated(){
            return this.$store.state.isAuthenticated
        }
    }

}
</script>
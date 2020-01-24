<template>
    <nav>

        <v-app-bar app>
            
            <v-toolbar-title class="text-uppercase ">
                <span class="font-weight-light text-lowercase">shift</span>
                <span>MANAGR</span>
            </v-toolbar-title>

            <v-spacer></v-spacer>

            <v-btn v-if="authenticated" text to="/">
                <span>{{userInfo.username}}'s Dashboard</span>
                <v-icon right >home</v-icon>
            </v-btn>
            <v-btn v-if="authenticated" text to="/settings">
                <span>Settings</span>
                <v-icon right >settings</v-icon>
            </v-btn>
            <v-btn text to="/jwttest">
                <span>Test JWT</span>
                <v-icon right >lock</v-icon>
            </v-btn>
            <v-btn v-if="!authenticated" text to="/login">
                <span>Sign In / Register</span>
                <v-icon right >perm_identity</v-icon>
            </v-btn>
            <v-btn v-if="authenticated" text @click="logOut">
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
            primaryDrawer: {
                model: false,
            }
            // links: [
            //     { label: `${this.userInfo.username}'s Dashboard`, link: '/', icon: 'home', test: this.authenticated, action: null},
            //     { label: `Test JWT`, link: '/jwttest', icon: 'lock', test: true, action: null},
            //     { label: `Sign In / Register`, link: '/login', icon: 'perm_identity', test: !this.authenticated, action: null},
            //     { label: `Sign Out`, link: '/', icon: 'home', test: this.authenticated, action: 'logOut'},
            // ]
        }
    },
    methods: {
        logOut(){
            this.$store.dispatch('deleteToken')
        },
    },
    computed: {
        authenticated(){
            return this.$store.getters.isAuthenticated
        },
        userInfo(){
            return this.$store.getters.userInfo
        },
    }

}
</script>
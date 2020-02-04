<template>
    <nav>

        <v-app-bar app clipped-right>
            
            <v-toolbar-title class="text-uppercase ">
                <span class="font-weight-light text-lowercase">shift</span>
                <span>MANAGR</span>
            </v-toolbar-title>

            <v-spacer></v-spacer>
        
                <span v-if="authenticated && org.name && !workspace.name" color="primary" class="mr-2">
                    <v-chip color="primary" class="mr-2" label large>
                        {{ org.name }}
                    </v-chip>
                </span>
                <span v-if="authenticated && org.name && workspace.name" color="primary" class="mr-2">
                    <v-chip color="primary" class="mr-2" label large>
                        {{ org.name }}: {{workspace.name}}
                    </v-chip>
                </span>

            <v-toolbar-items v-if="!kioskMode">
                <v-btn v-if="authenticated" text to="/" class="mr-2">
                    <span>Dashboard</span>
                    <v-icon right >home</v-icon>
                </v-btn>
                <v-btn v-if="authenticated" text to="/settings" class="mr-2">
                    <span>Settings</span>
                    <v-icon right >settings</v-icon>
                </v-btn>
                <v-btn v-if="authenticated" text to="/kiosk" class="mr-2">
                    <span>Kiosk</span>
                    <v-icon right >desktop_windows</v-icon>
                </v-btn>
                <!-- <v-btn text to="/jwttest" class="mr-2">
                    <span>Test JWT</span>
                    <v-icon right >lock</v-icon>
                </v-btn> -->
                <v-btn v-if="!authenticated" text to="/login" class="mr-2">
                    <span>Sign In / Register</span>
                    <v-icon right >perm_identity</v-icon>
                </v-btn>
                <v-btn v-if="authenticated" text @click="logOut" class="mr-2">
                    <span>Sign Out</span>
                    <v-icon right >exit_to_app</v-icon>
            </v-btn>
            </v-toolbar-items>
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
            this.$store.dispatch('logout')
        },
    },
    computed: {
        authenticated(){
            return this.$store.getters.isAuthenticated
        },
        username(){
            return this.$store.getters.username
        },
        org(){
            return this.$store.getters.organization
        },
        workspace(){
            return this.$store.getters.workspace
        },
        kioskMode(){
            return this.$store.getters.kioskMode
        }
    }

}
</script>
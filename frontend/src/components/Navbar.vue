<template>
    <nav>

        <v-app-bar app clipped-right>
            
            <!-- Site logo/title -->
            <v-toolbar-title class="text-uppercase ">
                <span class="font-weight-light text-lowercase title">shift</span>
                <span class="primary--text title">MANAGR</span>
            </v-toolbar-title>

            <v-spacer></v-spacer>
        
                <!-- if there is an org and/or workspace, displays title on navbar -->
                <span v-if="authenticated && org.name && !workspace.name" color="primary" class="mr-2">
                    <v-chip color="primary" class="mr-2 title" label large>
                        {{ org.name }}
                    </v-chip>
                </span>
                <span v-if="authenticated && org.name && workspace.name" color="primary" class="mr-2">
                    <v-chip color="primary" class="mr-2 title" label large>
                        {{ org.name }}: {{workspace.name}}
                    </v-chip>
                </span>

            <!-- Toolbar buttons.  Visibility varies depending on if user is authenticated -->
            <v-toolbar-items v-if="!kioskMode">
                <v-btn v-if="authenticated" text to="/" class="mr-2">
                    <span>Dashboard</span>
                    <v-icon right >home</v-icon>
                </v-btn>
                <v-btn v-if="authenticated" text to="/kiosk" class="mr-2">
                    <span>Kiosk</span>
                    <v-icon right >desktop_windows</v-icon>
                </v-btn>
                <v-btn v-if="authenticated" text to="/settings" class="mr-2">
                    <span>Settings</span>
                    <v-icon right >settings</v-icon>
                </v-btn>

                <v-btn v-if="!authenticated" text to="/login" class="mr-2">
                    <span>Sign In / Register</span>
                    <v-icon right >perm_identity</v-icon>
                </v-btn>
                <v-btn v-if="authenticated" text @click="logOut" class="mr-2">
                    <span>Sign Out</span>
                    <v-icon right >exit_to_app</v-icon>
                </v-btn>

                <!-- this is a link to a testing page for JWT authentication -->
                <!-- <v-btn text to="/jwttest" class="mr-2">
                    <span>Test JWT</span>
                    <v-icon right >lock</v-icon>
                </v-btn> -->

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
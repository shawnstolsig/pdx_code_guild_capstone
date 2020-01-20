<template>
    <nav>
        <v-app-bar flat app dark>

            <v-toolbar-title class="text-uppercase grey--text">
                <span class="font-weight-light text-lowercase">shift</span>
                <span>MANAGR</span>
            </v-toolbar-title>

            <v-spacer></v-spacer>

            <v-btn text color="grey">
                <span>Sign In</span>
                <v-icon right >perm_identity</v-icon>
            </v-btn>
            <v-btn text color="grey">
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

    },

}
</script>
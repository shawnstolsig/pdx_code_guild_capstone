<template>
    <v-container>
        <!-- Start of Organization Settings -->
        <v-row v-if="!validOrg">
            <v-col cols="3">
                <v-card flat>
                    <v-card-text>
                        No organization selected.
                    </v-card-text>
                </v-card>
            </v-col>
        </v-row>

        <v-row v-if="validOrg">
            <!-- Department Card -->
            <v-col cols="6">
                <DeptSettings />
            </v-col>
            <!-- Cohort Card -->
            <v-col cols="6">
                <CohortSettings />
            </v-col>
        </v-row>
        <v-row v-if="validOrg">
            <!-- Roles card -->
            <v-col cols="12">
                <RoleSettings />
            </v-col>
        </v-row>
    </v-container><!-- End of Organization Settings -->
</template>

<script>
import DeptSettings from '@/components/settings/DeptSettings'
import CohortSettings from '@/components/settings/CohortSettings'
import RoleSettings from '@/components/settings/RoleSettings'

export default {

    components: {
        DeptSettings,
        CohortSettings,
        RoleSettings
    },
	data: () => ({

	}),     // end data

	methods: {

	},      /// end methods	

	computed: {			
		validOrg(){
			return !!this.$store.getters.user.organization
		},
		org(){
			return this.$store.getters.organization
		},
	},		// end computed

	mounted() {

	},		// end mounted
}
</script>
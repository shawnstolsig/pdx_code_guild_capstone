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
    		<v-tab-item>	
				<OrgSettings></OrgSettings>
			</v-tab-item>	
			<v-tab-item>	
				<AccountSettings></AccountSettings>
			</v-tab-item>

		</v-tabs>
	</v-container>
</template>


<script>
import OrgPopup from '@/components/settings/OrgPopup'
import OrgSettings from '@/components/settings/OrgSettings'
import AccountSettings from '@/components/settings/AccountSettings'


export default {
	name: 'settings',
	components: { 
		OrgPopup, 
		OrgSettings,
		AccountSettings,
	},
	data: () => ({
		links: [
			{text: 'Organization', icon: 'business'},
			{text: 'Account', icon: 'mdi-account'},
		],
	}),     // end data

	methods: {
	},      /// end methods	

	computed: {			
	},		// end computed

	mounted() {
		this.$vuetify.theme.dark = this.$store.getters.user.darkModeEnabled
	},		// end created
}
</script>

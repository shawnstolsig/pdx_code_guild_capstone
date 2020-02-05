<template>
	<v-container background="background">
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
				<WorkerSettings></WorkerSettings>
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
import WorkerSettings from '@/components/settings/WorkerSettings'


export default {
	name: 'settings',
	components: { 
		OrgPopup, 
		OrgSettings,
		AccountSettings,
		WorkerSettings,
	},
	data: () => ({
		links: [
			{text: 'Organization', icon: 'business'},
			{text: 'Employees', icon: 'people_alt'},
			{text: 'Account', icon: 'account_box'},
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

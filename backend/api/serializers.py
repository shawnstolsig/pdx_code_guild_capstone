from rest_framework import serializers
from django.contrib.auth.models import User
from org.models import Organization, Department, Cohort
from people.models import Manager

class OrganizationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Organization
        fields = ('name', 'description', 'date_created', 'date_updated')

class DepartmentSerializer(serializers.ModelSerializer):
    organization = OrganizationSerializer(read_only=True)   

    class Meta:
        model = Department
        fields = ('name', 'description', 'date_created', 'date_updated', 'organization')

class CohortSerializer(serializers.ModelSerializer):
    organization = OrganizationSerializer(read_only=True)
    class Meta:
        model = Cohort
        fields = ('code', 'description', 'date_created', 'date_updated', 'organization')

class UserSerializer(serializers.ModelSerializer):
    class Meta: 
        model = User
        fields = ('id', 'username', 'last_login', 'first_name', 'last_name', 'is_active', 'date_joined')

class ManagerSerializer(serializers.ModelSerializer):
    organization = OrganizationSerializer(read_only=True)
    department = DepartmentSerializer(read_only=True)
    user = UserSerializer(read_only=True)
    class Meta:
        model = Manager
        fields = ('full_name', 'date_created', 'date_updated', 'user', 'organization', 'department')



# Sample serializers:
# from data.models import Upgrade, Ship, Skill, Clan, Player, ShipInstance
# from clan_battles.models import Battle, ClanInstance, PlayerInstance

# class UserClanRosterSerializer(serializers.ModelSerializer):
#     roster = serializers.StringRelatedField(many=True)

#     class Meta:
#         model = Clan
#         # ommitted fields: player_user, player_ships, player_clan
#         fields = ('clan_wgid', 'clan_tag', 'clan_name', 'clan_members_count', 'clan_realm', 'clan_is_disbanded', 'roster')

# class ShipSerializer(serializers.ModelSerializer):
    
#     class Meta:
#         model = Ship
#         # omitted fields: ship_upgrades
#         fields = ('ship_wgid',
#         'ship_name',
#         'ship_class',
#         'ship_tier',
#         'ship_nation',
#         'ship_upgrades',
#         'ship_upgrade_slots')

# class UserShipsSerializer(serializers.ModelSerializer):
#     # player_fleet = serializers.StringRelatedField(many=False)
#     shipinstance_ship_name = ShipSerializer(read_only=True, source="shipinstance_ship")
#     class Meta:
#         model = ShipInstance
#         fields = ('shipinstance_main_battery_hits',
#         'shipinstance_main_battery_shots',
#         'shipinstance_xp',
#         'shipinstance_battles',
#         'shipinstance_torpedoes_hits',
#         'shipinstance_torpedoes_shots',
#         'shipinstance_wins',
#         'shipinstance_losses',
#         'shipinstance_damage_dealt',
#         'shipinstance_potential_damage',
#         'shipinstance_spotting_damage',
#         'shipinstance_ship_name')

from rest_framework import serializers









# Sample serializers:
# from data.models import Upgrade, Ship, Skill, Clan, Player, ShipInstance
# from clan_battles.models import Battle, ClanInstance, PlayerInstance
# class PlayerSerializer(serializers.ModelSerializer):
#     # clans = serializers.StringRelatedField(many=False)
#     class Meta:
#         model = Player
#         # ommitted fields: player_user, player_ships, player_clan
#         fields = ('player_wgid', 'player_nickname', 'player_clan_role', 'player_joined_at')

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

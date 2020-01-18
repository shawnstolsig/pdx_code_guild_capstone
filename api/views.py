from django.shortcuts import render
from rest_framework import viewsets














# from .serializers import PlayerSerializer, ShipSerializer, UserShipsSerializer
# from data.models import Upgrade, Ship, Skill, Clan, Player, ShipInstance

# # Create your views here.
# class PlayerViewSet(viewsets.ReadOnlyModelViewSet):
#     queryset = Player.objects.all()
#     serializer_class = PlayerSerializer

# class UserClanRosterViewset(viewsets.ReadOnlyModelViewSet):
#     # queryset = Clan.objects.all()
#     serializer_class = PlayerSerializer

#     # def get_serializer_context(self):
#     #     return {'request': self.request}

#     def get_queryset(self):
#         queryset = Clan.objects.get(clan_wgid=self.request.user.player.player_clan.clan_wgid).roster

#         return queryset

# class ShipsViewset(viewsets.ReadOnlyModelViewSet):
#     queryset = Ship.objects.all()
#     serializer_class = ShipSerializer

# class UserShipsViewset(viewsets.ReadOnlyModelViewSet):
#     serializer_class = UserShipsSerializer

#     def get_queryset(self):
        
#         queryset = ShipInstance.objects.filter(shipinstance_player = self.request.user.player)
#         return queryset
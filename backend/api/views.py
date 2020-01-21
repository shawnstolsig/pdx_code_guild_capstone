from django.shortcuts import render
from rest_framework import viewsets

from .serializers import OrganizationSerializer, DepartmentSerializer, CohortSerializer, ManagerSerializer
from org.models import Organization, Department, Cohort
from people.models import Manager, Worker, Role
from process.models import SVGElement, Workspace, Zone, Node, FlowpathWorkspace, FlowpathZone, FlowpathNode
from planning.models import Shift, Job

class OrganizationViewSet(viewsets.ModelViewSet):
    queryset = Organization.objects.all()
    serializer_class = OrganizationSerializer

class DepartmentViewSet(viewsets.ModelViewSet):
    serializer_class = DepartmentSerializer

    def get_queryset(self):
        queryset = Department.objects.all()
        
        # Optionally filter by Organization
        organization = self.request.query_params.get('organization', None)
        if organization is not None:
            queryset = queryset.filter(organization=organization)

        return queryset

class CohortViewSet(viewsets.ModelViewSet):
    serializer_class = CohortSerializer

    def get_queryset(self):
        queryset = Cohort.objects.all()

        # Optionally filter by Organization:
        organization = self.request.query_params.get('organization', None)
        if organization is not None:
            queryset = queryset.filter(organization=organization)

        return queryset

class ManagerViewSet(viewsets.ModelViewSet):
    serializer_class = ManagerSerializer
    # authentication_classes = 

    def get_queryset(self):
        queryset = Manager.objects.all()

        # Optionally filter by Organization:
        organization = self.request.query_params.get('organization', None)
        if organization is not None:
            queryset = queryset.filter(organization=organization)

        # Optionally filter by Department:
        department = self.request.query_params.get('department', None)
        if organization is not None:
            queryset = queryset.filter(department=department)

        return queryset


# for JWT authentication stuff
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

class HelloView(APIView):
    permission_classes = (IsAuthenticated, )

    def get(self, request):
        content = {'message': 'Hello World JWT!'}
        return Response(content)





# from data.models import Upgrade, Ship, Skill, Clan, Player, ShipInstance

# # Create your views here.

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
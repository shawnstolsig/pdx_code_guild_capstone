from django.shortcuts import render
from rest_framework import viewsets

from .serializers import OrganizationSerializer, DepartmentSerializer, CohortSerializer, ManagerSerializer, UserSerializer
from django.contrib.auth.models import User
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

class UserViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = UserSerializer
    queryset = User.objects.all()


# for JWT authentication stuff
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

class TestAuthenticationView(APIView):

    def get(self, request):
        content = {'message': 'Hello from your Django Backend!\n You have accessed an IsAuthenticated view.'}
        return Response(content)

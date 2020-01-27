from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.permissions import IsAuthenticated
from api.permissions import IsOwnerManagerOrReadOnly

from .serializers import OrganizationSerializer, OrganizationUUIDSerializer, OrganizationAllSerializer
from .serializers import DepartmentSerializer, CohortSerializer, ManagerSerializer, UserSerializer, WorkerSerializer
from django.contrib.auth.models import User
from org.models import Organization, Department, Cohort
from people.models import Manager, Worker, Role
from process.models import SVGElement, Workspace, Zone, Node, FlowpathWorkspace, FlowpathZone, FlowpathNode
from planning.models import Shift, Job

class OrganizationViewSet(viewsets.ModelViewSet):
    queryset = Organization.objects.all()
    serializer_class = OrganizationSerializer
    permission_classes = [IsAuthenticated]

class OrganizationUUIDViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Organization.objects.all()
    serializer_class = OrganizationUUIDSerializer
    permission_classes = [IsAuthenticated]

class OrganizationAllViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Organization.objects.all()
    serializer_class = OrganizationAllSerializer
    permission_classes = [IsAuthenticated]

class WorkerViewSet(viewsets.ModelViewSet):
    queryset = Worker.objects.all()
    serializer_class = WorkerSerializer
    permission_classes = [IsAuthenticated]

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
    permission_classes = [IsOwnerManagerOrReadOnly,IsAuthenticated]

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

# class ManagerListCreateView(ListCreateAPIView):
#     queryset = Manager.objects.all()
#     serializer_class = ManagerSerializer
#     permission_classes = [IsAuthenticated]

#     def perform_create(self, serializer):
#         user = self.request.user
#         print(f"perform create user is {user}")
#         serializer.save(user=user)

# class ManagerDetailView(RetrieveUpdateDestroyAPIView):
#     queryset = Manager.objects.all()
#     serializer_class = ManagerSerializer
#     permission_classes = [IsOwnerManagerOrReadOnly,IsAuthenticated]


# for JWT authentication stuff
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

class TestAuthenticationView(APIView):

    def get(self, request):
        content = {'message': 'Hello from your Django Backend!\n You have accessed an IsAuthenticated view.'}
        return Response(content)


class UserViewSet(viewsets.ModelViewSet):
    serializer_class = UserSerializer
    queryset = User.objects.all()
    permission_classes = [IsAuthenticated]

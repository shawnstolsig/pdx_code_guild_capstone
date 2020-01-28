from rest_framework import serializers
from django.contrib.auth.models import User
from org.models import Organization, Department, Cohort
from process.models import Workspace, Zone, Node, FlowpathWorkspace, FlowpathZone, FlowpathNode, SVGElement
from people.models import Manager, Worker, Role
from planning.models import Shift, Job
import uuid

# Base serializers for organization.models
class OrganizationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Organization
        fields = '__all__'

class DepartmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Department
        fields = '__all__'

class CohortSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cohort
        fields = '__all__'

# Base serializer for User
class UserSerializer(serializers.ModelSerializer):
    class Meta: 
        model = User
        fields = ('id', 'username', 'email', 'first_name', 'last_name')

# Base serializers for people.models
class ManagerSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    class Meta:
        model = Manager
        fields = ('id', 'full_name', 'date_created', 'date_updated', 'dark_mode_enabled', 'organization', 'department', 'user')

    # must modify update function for updating nested Department and/or Organization
    def update(self, instance, validated_data):
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance

class WorkerSerializer(serializers.ModelSerializer):
    class Meta: 
        model = Worker 
        fields = '__all__'

class RoleSerializer(serializers.ModelSerializer):
    # workers = WorkerSerializer(many=True, read_only=False)
    worker_ids = serializers.PrimaryKeyRelatedField(many=True, read_only=False, queryset=Worker.objects.all(), source="workers", allow_null=True)
    rate = serializers.IntegerField(allow_null=True, default='')
    class Meta: 
        model = Role 
        fields = ('id', 'name', 'description', 'rate', 'last_staffed', 'organization', 'department', 'date_created', 'date_updated', 'worker_ids')

    def update(self, instance, validated_data):

        for attr, value in validated_data.items():
            if str(attr) != 'workers':
                setattr(instance, attr, value)
            else:
                instance.workers.set(value)
        instance.save()
        return instance

# class RoleWithWorkersSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Role
#         fields

# Base serializers for process.models
class SVGElementSerializer(serializers.ModelSerializer):
    class Meta: 
        model = SVGElement
        fields = '__all__'
class WorkspaceSerializer(serializers.ModelSerializer):
    svg = SVGElementSerializer()
    class Meta:
        model = Workspace
        fields = '__all__'
class ZoneSerializer(serializers.ModelSerializer):
    svg = SVGElementSerializer()
    class Meta:
        model = Zone
        fields = '__all__'
class NodeSerializer(serializers.ModelSerializer):
    svg = SVGElementSerializer()
    class Meta:
        model = Node
        fields = '__all__'
class FlowpathWorkspaceSerializer(serializers.ModelSerializer):
    svg = SVGElementSerializer()
    class Meta:
        model = FlowpathWorkspace
        fields = '__all__'
class FlowpathZoneSerializer(serializers.ModelSerializer):
    svg = SVGElementSerializer()
    class Meta:
        model = FlowpathZone
        fields = '__all__'
class FlowpathNodeSerializer(serializers.ModelSerializer):
    svg = SVGElementSerializer()
    class Meta:
        model = FlowpathNode
        fields = '__all__'

# Base serializers for planning.models
class ShiftSerializer(serializers.ModelSerializer):
    class Meta:
        model = Shift 
        fields = '__all__'
class JobSerializer(serializers.ModelSerializer):
    class Meta:
        model = Job 
        fields = '__all__'

######################## Extended serializers for specific purposes ##################3


# Serializer for only returning id and code of each org, to prevent exposing all user orgs 
class OrganizationUUIDSerializer(serializers.ModelSerializer):
    class Meta:
        model = Organization
        fields = ('id', 'code')

# A giant nested serializer to load all Organization information.  Takes in parameter of Organization pk.
class OrganizationAllSerializer(serializers.ModelSerializer):
    # from org.models
    org_departments = DepartmentSerializer(many=True, read_only=True)
    org_cohorts = CohortSerializer(many=True, read_only=True)
    # from process.models
    org_workspaces = WorkspaceSerializer(many=True, read_only=True)
    org_zones = ZoneSerializer(many=True, read_only=True)
    org_nodes = NodeSerializer(many=True, read_only=True)
    org_workspace_flows = FlowpathWorkspaceSerializer(many=True, read_only=True)
    org_zone_flows = FlowpathZoneSerializer(many=True, read_only=True)
    org_node_flows = FlowpathNodeSerializer(many=True, read_only=True)
    # from people.models
    org_managers = ManagerSerializer(many=True, read_only=True)
    org_workers = WorkerSerializer(many=True, read_only=True)
    org_roles = RoleSerializer(many=True, read_only=True)
    # from planning.models
    org_shifts = ShiftSerializer(many=True, read_only=True)
    org_jobs = JobSerializer(many=True, read_only=True)

    class Meta:
        model = Organization
        fields = ('id', 'name', 'description', 'date_created', 'date_updated', 'code', 
                    'org_departments', 'org_cohorts',
                    'org_workspaces', 'org_zones', 'org_nodes', 'org_workspace_flows', 'org_zone_flows', 'org_node_flows',
                    'org_managers', 'org_workers', 'org_roles',
                    'org_shifts', 'org_jobs')
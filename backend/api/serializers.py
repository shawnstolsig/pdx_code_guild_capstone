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

# following example here: https://dev.to/lewiskori/user-registration-and-authorization-on-a-django-api-with-djoser-and-json-web-tokens-4kc7
class ManagerSerializer(serializers.ModelSerializer):
    # organization = OrganizationSerializer(read_only=True)
    # department = DepartmentSerializer(read_only=True)
    # user = UserSerializer(read_only=True)
    user = serializers.StringRelatedField(read_only=True)
    class Meta:
        model = Manager
        fields='__all__'
        # user currently removed
        # fields = ('full_name', 'date_created', 'date_updated', 'organization', 'department')

class UserSerializer(serializers.ModelSerializer):
    class Meta: 
        model = User
        fields = ('id', 'username', 'email', 'first_name', 'last_name')
from rest_framework import serializers
from django.contrib.auth.models import User
from org.models import Organization, Department, Cohort
from people.models import Manager
import uuid

class OrganizationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Organization
        fields = '__all__'

class OrganizationUUIDSerializer(serializers.ModelSerializer):
    class Meta:
        model = Organization
        fields = ('id', 'code')

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
        fields = ('id', 'username', 'email', 'first_name', 'last_name')
# following example here: https://dev.to/lewiskori/user-registration-and-authorization-on-a-django-api-with-djoser-and-json-web-tokens-4kc7
class ManagerSerializer(serializers.ModelSerializer):
    # department = DepartmentSerializer(read_only=True)
    # organization = OrganizationSerializer(read_only=False)
    user = UserSerializer(read_only=True)
    # user = serializers.StringRelatedField(read_only=True)
    class Meta:
        model = Manager
        # fields='__all__'
        # user currently removed
        fields = ('id', 'full_name', 'date_created', 'date_updated', 'dark_mode_enabled', 'organization', 'department', 'user')

    # must modify update function for updating nested Department and/or Organization
    def update(self, instance, validated_data):
        # instance.organization = validated_data.pop('organization')
        # instance.save()
        # return instance
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance
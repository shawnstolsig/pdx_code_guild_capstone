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

# class RegistrationSerializer(serializers.ModelSerializer):

#     # Ensure passwords are at least 8 characters long, no longer than 128
#     # characters, and can not be read by the client.
#     password = serializers.CharField(
#         max_length=128,
#         min_length=8,
#         write_only=True
#     )

#     class Meta:
#         model = User
#         # List all of the fields that could possibly be included in a request
#         # or response, including fields specified explicitly above.
#         fields = ['email', 'username', 'password', 'first_name', 'last_name']

#     def create(self, validated_data):
#         # Use the `create_user` method we wrote earlier to create a new user.
#         return User.objects.get_or_create(**validated_data)
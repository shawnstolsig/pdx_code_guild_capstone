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






# following example here: 
# https://medium.com/@apogiatzis/create-a-restful-api-with-users-and-jwt-authentication-using-django-1-11-drf-part-2-eb6fdcf71f45

# class ManagerSerializer(serializers.ModelSerializer):
#     # organization = OrganizationSerializer(read_only=True)
#     # department = DepartmentSerializer(read_only=True)
#     # user = UserSerializer(read_only=True)
#     class Meta:
#         model = Manager
#         # user currently removed
#         fields = ('full_name', 'date_created', 'date_updated', 'organization', 'department')

# class UserSerializer(serializers.ModelSerializer):
#     manager = ManagerSerializer(required=True)

#     class Meta: 
#         model = User
#         # not including last_login, date_joined, or is_active
#         fields = ('id', 'username', 'first_name', 'last_name', 'email', 'password', 'last_login', 'date_joined', 'is_active', 'manager')
#         extra_kwargs = {'password': {'write_only': True}}

#     def create(self, validated_data):
#         # manager_data = validated_data.pop('manager')
#         password = validated_data.pop('password')
#         user = User(**validated_data)
#         user.set_password(password)
#         user.save()
#         Manager.objects.get_or_create(user=user, full_name=f'{user.first_name} {user.last_name}')
#         return user
    
#     def update(self, instance, validated_data):
#         # manager_data = validated_data.pop('manager')
#         manager = instance.manager

#         instance.email = validated_data.get('email', instance.email)
#         instance.save()

#         manager.full_name = f"${validated_data.get('first_name')} {validated_data.get('last_name')}"
#         manager.save()

#         return instance



 

























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
from django.db import models
import uuid

# These models deal with defining the organization:
# Organization
# Department
# Cohort

class Organization(models.Model):
    """
    Organization helps groups together all information relevant to the User.  It represents the 
    business (or other organization) that the User is managing.  Users from the same Organization
    will have visibility on the same data. 
    """

    # attributes
    name = models.CharField(max_length=150)
    code = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    description = models.TextField(null=True)

    # relationships
    # (none as the Organization is the top-level model)
    # (all other models will CASCADE delete if the Organization is deleted)

    # timestamps
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

class Department(models.Model):
    """
    The Department is one level below the Organization.  The primary purpose of the
    Department is to (a) compartmentalize information so that only relevent data is presented 
    to each user and (b) assist with permissions (Managers will be able to view data from the 
    entire Organization but will only be able to edit data for their own Department).
    """

    # attributes
    name = models.CharField(max_length=150)
    description = models.TextField(null=True)
    color = models.CharField(max_length=50, default="#FFFFFF")

    # relationships
    # (all models using Department as foreign key will SET_NULL on deletion of Department)
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE, related_name="org_departments")

    # timestamps
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

from django.contrib.auth.models import User


class Cohort(models.Model):
    """
    A Cohort is used to group associates together by schedule.  This will be necessary for shift
    planning.  Each Cohort has a "code" which can be thought of as the short name for the Cohort. 
    The application is agnostic towards the actual codes; they are designed to be customizable so that 
    they can adapt to the convention already used by an organization.  Not that a Cohort is unrelated 
    to a Department, as Cohorts are usually established at the Organization level.
    """

    # attributes
    name = models.CharField(max_length=50)
    description = models.TextField(null=True)

    # relationships
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE, related_name="org_cohorts")
    color = models.CharField(max_length=50, default="#FFFFFF")

    # timestamps
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.code
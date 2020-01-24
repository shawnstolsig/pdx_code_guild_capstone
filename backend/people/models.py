from django.db import models
from django.contrib.auth.models import User
from org.models import Organization, Department, Cohort

# These models are relating to the people element of an organization:
# Manager (extends base User class)
# Worker
# Role

class Manager(models.Model):
    """
    The Manager extends Django's built-in User class in order to link each user to a specific 
    Department and Organization. It does not contain first, last, or user names because these are 
    already provided by Django's User class. Additionally, Managers do not have roles or a badge ID.
    """

    # attributes
    full_name = models.CharField(max_length=180, null=True)
    dark_mode_enabled = models.BooleanField(default=False)

    # relationships
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE, null=True)
    department = models.ForeignKey(Department, on_delete=models.SET_NULL, null=True)

    # timestamps
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.user.username


class Worker(models.Model):
    """
    The Worker represents an employee that can be assigned to a Job.  This model has 
    lationships with many other models within the Organization.  Organizationally, Workers
    are linked to the Department and not the Manager, as Managers are more likely to change
    than the Department a Worker is assigned to.
    """

    # attributes
    badge_id = models.CharField(max_length=50, null=True)
    username = models.CharField(max_length=50, null=True)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    full_name = models.CharField(max_length=50)
    hire_date = models.DateField(null=True)
  
    # relationships
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE)
    department = models.ForeignKey(Department, on_delete=models.SET_NULL, null=True)
    cohort = models.ForeignKey(Cohort, on_delete=models.SET_NULL, null=True)

    # timestamps
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.full_name

class Role(models.Model):
    """
    A Role is a particular process path/function within an Organization.  The (many to many)
    relationship between a Role and a Worker represents a task that the Worker is qualified to do.  
    Additionally, Roles will be linked to     Nodes in order to identify the functional purpose of 
    the Node. Depending on the Role, there may be a productivity rate (ie, widgets/hr) configured
    for determining throughput.  Additionally, the Role model will also contain a field for tracking 
    the last Worker that was assigned to the Role.  This will be critical to the algorithm that 
    will help Managers create Shift plans.  
    """

    # attributes
    name = models.CharField(max_length=50)
    description = models.TextField(null=True)
    rate = models.FloatField(null=True)
    last_staffed = models.CharField(max_length=50, null=True)

  
    # relationships
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE)
    department = models.ForeignKey(Department, on_delete=models.SET_NULL, null=True)
    workers = models.ManyToManyField(Worker, related_name="roles")

    # timestamps
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
from django.db import models
from org.models import Organization, Department, Cohort
from process.models import SVGElement, Workspace, Zone, Node, FlowpathWorkspace, FlowpathZone, FlowpathNode
from people.models import Manager, Worker, Role

# These models deal with tying together all other models to form shift plans:
# Shift
# Job

class Shift(models.Model):
    """
    A Shift is primarily a collection of worker/node (Job) assignments.  A Shift will include
    a specified start and end date/time so that Shifts can be explicitly described to users.
    Note that these start/end datetimes must be specified and cannot be null.  They will be 
    specified by the front-end, not using auto_now.  
    """

    # attributes
    start = models.DateTimeField()
    end = models.DateTimeField()
  
    # relationships
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE)
    department = models.ForeignKey(Department, on_delete=models.SET_NULL, null=True)

    # timestamps
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.department.name}: {self.start} - {self.end}'

class Job(models.Model):
    """
    A Job is the matching of a Worker, Node, Role, and Shift.  
    """
    # attributes
    # (none)
    
    # relationships
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE)
    department = models.ForeignKey(Department, on_delete=models.SET_NULL, null=True)
    node = models.ForeignKey(Node, on_delete=models.CASCADE)
    shift = models.ForeignKey(Shift, on_delete=models.CASCADE)
    role = models.ForeignKey(Role, on_delete=models.CASCADE)
    worker = models.ForeignKey(Worker, on_delete=models.CASCADE)

    # timestamps
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.shift}: {self.worker} at {self.node} in role {self.role}'
from django.db import models
from django.contrib.auth.models import User

class Organization(models.Model):
    """
    Organization helps groups together all information relevant to the User.  It represents the 
    business (or other organization) that the User is managing.  Users from the same Organization
    will have visibility on the same data. 
    """

    # attributes
    name = models.CharField(max_length=150)
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

    # relationships
    # (all models using Department as foreign key will SET_NULL on deletion of Department)
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE)

    # timestamps
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

class Cohort(models.Model):
    """
    A Cohort is used to group associates together by schedule.  This will be necessary for shift
    planning.  Each Cohort has a "code" which can be thought of as the short name for the Cohort. 
    The application is agnostic towards the actual codes; they are designed to be customizable so that 
    they can adapt to the convention already used by an organization.  Not that a Cohort is unrelated 
    to a Department, as Cohorts are usually established at the Organization level.
    """

    # attributes
    code = models.CharField(max_length=50)
    description = models.TextField(null=True)

    # relationships
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE)

    # timestamps
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.code

class Manager(models.Model):
    """
    The Manager extends Django's built-in User class in order to link each user to a specific 
    Department and Organization. It does not contain first, last, or user names because these are 
    already provided by Django's User class. Additionally, Managers do not have roles or a badge ID.
    """

    # attributes
    # (inherited from built-in User class)

    # relationships
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE)
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

class SVGElement(models.Model):
    """
    A SVGElement will contain all of the information/attributes necessary to render each Workspace,
    Zone, and Node.  All attributes of a SVGElement will be nullable so that one-size-fits-all with
    the different things that need to be rendered. 
    """
    svg_shape = models.CharField(max_length=50, null=True)
    svg_stroke = models.IntegerField(null=True)
    svg_stroke_width = models.IntegerField(null=True)
    svg_m = models.IntegerField(null=True)
    svg_l = models.IntegerField(null=True)
    svg_points = models.CharField(max_length=50, null=True)
    svg_x = models.IntegerField(null=True)
    svg_y = models.IntegerField(null=True)
    svg_height = models.IntegerField(null=True)
    svg_width = models.IntegerField(null=True)
    svg_fill_r = models.IntegerField(null=True)
    svg_fill_g = models.IntegerField(null=True)
    svg_fill_b = models.IntegerField(null=True)
    svg_opacity = models.FloatField(null=True, default=1.0)

class Workspace(models.Model):
    """
    A Workspace represents a single Department's work area and will be the foundation for rendering 
    a work area to a user.  In other words, when rendering SVG, the attributes of a Workspace will be
    used for the base <svg> tag in HTML.  Each Workspace will be composed of Zones, Nodes, and Flowpaths 
    to help link everything together. 
    """

    # attributes
    name = models.CharField(max_length=50)
    description = models.TextField(null=True)
    volume = models.IntegerField(null=True)
  
    # relationships
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE)
    department = models.ForeignKey(Department, on_delete=models.SET_NULL, null=True)
    svg = models.OneToOneField(SVGElement, on_delete=models.SET_NULL, null=True)

    # timestamps
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

class Zone(models.Model):
    """
    A Zone will be a collection of Nodes (although not all Nodes will need to be in a Zone).  This is an
    extra layer to help with organizing the functional parts of a Workspace (for example, a single production
    line would be grouped together as a Zone, and there could be multiple production lines in the same 
    Workspacelike.
    """

    # attributes
    name = models.CharField(max_length=50)
    description = models.TextField(null=True)
    volume = models.IntegerField(null=True)
  
    # relationships
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE)
    department = models.ForeignKey(Department, on_delete=models.SET_NULL, null=True)
    workspace = models.ForeignKey(Workspace, on_delete=models.CASCADE)
    svg = models.OneToOneField(SVGElement, on_delete=models.SET_NULL, null=True)

    # timestamps
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

class Node(models.Model):
    """
    A Node represents a location where a number of Workers (in the same Role) would be assigned.  A
    Node should be thought of a as a workstation or physical area of the operation where Workers 
    performing the same function would be assigned (like pickers in one area of the building).
    """

    # attributes
    name = models.CharField(max_length=50)
    volume = models.IntegerField(null=True)
  
    # relationships
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE)
    department = models.ForeignKey(Department, on_delete=models.SET_NULL, null=True)
    workspace = models.ForeignKey(Workspace, on_delete=models.CASCADE)
    zone = models.ForeignKey(Zone, on_delete=models.CASCADE)
    role = models.ForeignKey(Role, on_delete=models.SET_NULL, null=True)
    svg = models.OneToOneField(SVGElement, on_delete=models.SET_NULL, null=True)

    # timestamps
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

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

class FlowpathNode(models.Model):
    """
    A path from one Node to another.  Helps do define the flow of widgets, and has an attribute
    for tracking volume per unit of time.  
    """
    # attributes
    volume = models.IntegerField(null=True)
    
    # relationships
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE)
    department = models.ForeignKey(Department, on_delete=models.CASCADE)
    svg = models.OneToOneField(SVGElement, on_delete=models.SET_NULL, null=True)

    input_node = models.ForeignKey(Node, on_delete=models.CASCADE, related_name="flowpath_in")
    output_node = models.ForeignKey(Node, on_delete=models.CASCADE, related_name="flowpath_out")

    # timestamps
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'Node flowpath from {self.input_node} to {self.output_node}'

class FlowpathZone(models.Model):
    """
    A path from one Zone to another.  Helps do define the flow of widgets, and has an attribute
    for tracking volume per unit of time.  
    """
    # attributes
    volume = models.IntegerField(null=True)
    
    # relationships
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE)
    department = models.ForeignKey(Department, on_delete=models.CASCADE)
    svg = models.OneToOneField(SVGElement, on_delete=models.SET_NULL, null=True)

    input_zone = models.ForeignKey(Zone, on_delete=models.CASCADE, related_name="flowpath_in")
    output_zone = models.ForeignKey(Zone, on_delete=models.CASCADE, related_name="flowpath_out")

    # timestamps
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'Zone flowpath from {self.input_zone} to {self.output_zone}'

class FlowpathWorkspace(models.Model):
    """
    A path from one Workspace to another.  Helps do define the flow of widgets, and has an attribute
    for tracking volume per unit of time.  
    """
    # attributes
    volume = models.IntegerField(null=True)
    
    # relationships
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE)

    input_workspace = models.ForeignKey(Workspace, on_delete=models.CASCADE, related_name="flowpath_in")
    output_workspace = models.ForeignKey(Workspace, on_delete=models.CASCADE, related_name="flowpath_out")

    # timestamps
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'Workspace flowpath from {self.input_workspace} to {self.output_workspace}'
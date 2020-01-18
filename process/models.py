from django.db import models
from django.apps import apps
from org.models import Organization, Department
from people.models import Role

# These models deal with the process elements of an organization:
# SVGElement (for rendering only)
# Workspace
# Zone
# Node
# FlowpathWorkspace
# FlowpathZone
# FlowpathNode

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

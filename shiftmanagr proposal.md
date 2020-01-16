# Capstone Proposal

### Project Name: 
shiftmanagr

### Project Overview
---
Prior to PDX Code Guild, I worked at Amazon as an Operations Manager for just over two years.  In this position, I managed a large number of associates (from 30 to 200+ people) who performed a variety of warehouse tasks: receiving, stowing, picking, packing, and shipping.  I learned pretty quickly that managing such a large workforce is a challenge, from basic tasks (deciding what workstation each associate would work at and balancing your workflow) to more advanced leadership concepts (avoiding favoritism).  The job was complicated by the large size of warehouses (850,000 sqft+) and surprisingly limited technology available to Amazon managers.  If a tool hadn't already been created at corporate, then you were out of luck; as an operator, it was nearly impossible to influence corporate Amazon's allocation of tech/development resources. 

One of the biggest pain points as an operations leader was managing where associates are assigned to work for a given shift (which workstation, area, process path, etc).  This is completely non-technological process at Amazon.  Here's an outline of the process: each department had a large rolling whiteboard in their area, called the "labor tracking board." On this whiteboard is a visual representation/diagram of the different workstations in the department.  Associates would be assigned to each workstation using a laminated, magnetic name-badge (or just their name hand-written in dry erase marker, if their name-badge had gone missing as they often did).  And that's it!

Even if you have no operations experience, there are a number of problems and opportunities with this approach.  How does a manager know where an associate is working (and that the associate is in their designated workstation/process), if they aren't standing next to the whiteboard?  If a manager moves an associate from one workstation to another, how is this communicated to other leaders that are running the department?  How do you plan ahead for the next shift without clearing the board and losing track of where everyone is currently assigned?  What if an associate moves their own name-badge to pick where they want to work?  These might seem like small issues, but they can easily result in miscommunications that have large financial impact on any given shift.

My capstone will alleviate these problems by digitizing the labor tracking board.  After performing a one-time configuration to define and visually diagram their work space, managers will assign employees to workstations electronically through a reactive web application.  Multiple managers will be able to login and see the same dashboard to track associate assignments in real-time.   Furthermore, a digital labor tracking board enables several additional enhancements that will add value for managers and employees alike: algorithm-based workstation assignments for each shift, improved assignment communication with empoloyees, and easier oversight for senior leadership. 

While I am leveraging my prior Amazon experience to build the first iteration of this project, I believe it has applications beyond warehouse operations.  Construction sites, hospitals, resturants, hotels, mueseums, manufacturing, retail...all of these industries could benefit from a reactive web application that allows for assigning employees to physical work areas and workstations, tracking their assignments electronically, and ensuring they are rotated algorithmically (instead of at a manager's whim) between each job that they are qualified for. 

### Features
---
###### Confiuration:
A manager will first need to define their work space.  This will be done either visually with a SVG diagram editor or with data entry into a table/spreadsheet.  Also, a manager will have to define the different roles in their workspace.  A single role type will be assigned to a workstation/node. Each workstation/node will also be assigned to a given zone, which will help with calculating throughput/flow for each step of the operation (for operations that process some type of widget).  

###### Manager use: 
Before a shift, a manager will generate the employee assignments.  This will be done either manually (drag and drop associate cards onto nodes of the work space diagram, or using drop-down selectors for non-graphical interface) or automatically with a button click (using a rotation-based algorithm).  Once the shift has started, managers will use the app to move employees between work stations as needed.  These moves will be rendered in real-time on the web app, so that other managers can view them.  Based on the workstation configurations, a throughput will be calculated (for applicable operations) in each zone and compared against the zones that are upstream/downstream on a dashboard.  This will help with managing flow and optimizing productivity.

###### Employee use:
An associate will have a kiosk where they can scan their badge and be shown which workstation they are assigned to. Ideally, this would located next to the time clock so that they know where to go immediately upon commencing their workday, without any need of communicating directly with a supervisor.

##### User Stories:
1. As a manager, I want to be able to view up-to-date workstation assignments for every employee so I can make timely labor adjustments based on shifting business needs.
2. As a manager, I want to be able to generate an entire set of employee/workstation shift assignments to save me time preparing for the next shift and to protect me from perceived favoritism that might result if I manually assign people.
3. As a manager, I want to make sure I only assign qualified, trained employees to a given process path to ensure employee safety and quality for those downstream of my operation.
4. As a manager, I want to see an automatic calculation of my volume flow/throughput based on how my employees are assigned to help me make the correct business decisions and labor moves. 
5. As an employee, I want to see where I am assigned as soon as I clock in so that I can get to work. 
6. As an employee, I want to be rotated between all of the positions that I am trained for to make sure I am not stuck doing the same thing every day.

##### Tasks:
- Build models: managers, employees, organization, department, workspace, flowpath, node, zone, role, shift
- Build API for models to serve to front end
- Allow manager to create new organization
- Allow manager to create workspace with nodes, zones, and flowpaths (visually)
- Allow manager to create workspace with nodes, zones, and flowpaths (text/tabular)
- Allow manager to create pre-shift plan by assigning single employees to node (visually)
- Allow manager to create pre-shift plan by assigning multiple employees to multiple nodes (via algorithm)
- Allow manager to make manual modifications to pre-shift plan (specifically, the one generated via algorithm)
- Allow manager to view and compare each zone's throughput in their workspace
- Allow manager to batch import employee information using (csv format) 
- Allow manager to batch import employee roles (csv format)
- Allow employee to input/scan their employee number at a kiosk to see where they are assigned

##### Stack:
Front-end: Vue.js (via CLI) with Axios
SVG editor: [diagram-vue](https://github.com/pb10005/diagram-vue) or similar.  I will need to modify/extend this to include different workspace SVG elements (like a desk, conveyor, table, chairs, etc)
Styling: A Vue component library (such as Vuetify, Bootstrap-Vue, Vue Material Kit, or CoreUI)
Back-end: Django with custom Django Rest Framework API

### Data Model
---
**Manager**
Manager will extend Django's built in User class.  It will contain relationships to one Organization, one Department, and many Employees, along with other user configuration/settings.

**Organization**
This will hold information about the Organization that the Managers and Employees are part of.  One of the primary functions of the Organization will be to tie seperate Departments and Managers together, so that Managers can login with their own credentials but still see the same Workspaces (that are related to the Organization).

**Department**
This will operate similiarly to Organization in that it will primarily contain relationships between Managers, Workspaces, and Employees.  One of the key differences will be with permissions: only Managers related to the Department will be able to edit Workspaces of the Department (Managers will still have read permissions for all Workspaces of the Organization).

**Employee**
Employee will contain basic information about an employee (name, workplace ID number, cohort/shift).  It will have relationships to many Roles (correlating to the different positions they are qualified to work) and one Node (which represents where they are assigned to work on a shift).  

**Workspace**
A Worksplace will contain relationships to the many Nodes and Flowpaths that together describe how a collection of processes and workstations combine within a Department.  A Workspace will have one Department and Organization.

**Zone**
A Zone will have many Nodes and Flowpaths within it.  The primary function of the Zone will be to help segment different areas of a Workspace so that you can monitor aspects of it's operation (such as throughput).

**Node**
A Node will represent a workspace/workstation that an Employee can be assigned to for a shift. It will also have one Role assigned to it, representing the function of the workstation.  Each Node will have many Flowpaths, representing the inputs and output of production.

**Flowpath**
A Flowpath will be a directional link between Nodes, helping to describe the flow of the Operation.  Flowpaths will have related many-to-many with Nodes.

**Role**
A role will describe a particular process path within the Department.  It will help define which Employees are eligible to be assigned to which Nodes.  Each Role will have many Employees and many Nodes as relationships. 

**Shift**
A Shift will hold all of the Employee to Node relationships for a given period of time.  A Shift will be created only by a manager, and will accessible by other Managers within the same Department.

### Schedule
---
**Milestone #1:** Django project created. First iteration of all models created. *Due Jan 18*

**Milestone #2:** Create first iteration API serializers for models using DRF.  Create Vue project via CLI with initial UI elements for testing (in particular, text-entry/tabular version of app) *Due Jan 22*

**Milestone #3:** Refine models and serializers until initial text-entry/tabular version operational. Create csv import features for employee roster and roles.  *Due Jan 25*

**Milestone #4:** Create/extend SVG editor for configuring workplace.  Replace initial UI elements with a Vue component-based UI. *Due Jan 29*

**Milestone #5:** Final seven days allocated for catch-up time, final QA/testing, and bug fixes.  Work on capstone presentation. *Due Feb 5*

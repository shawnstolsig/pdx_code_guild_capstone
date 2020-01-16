# Capstone Proposal

### Project Name
---

### Project Overview
---
Prior to PDX Code Guild, I worked at Amazon as an Operations Manager for just over two years.  In this position, I managed a large number of associates (from 30 to 200+ people) who performed a variety of warehouse tasks: receiving, stowing, picking, packing, and shipping.  I learned pretty quickly that managing such a large workforce is a challenge, from basic tasks (deciding what workstation each associate would work at and balancing your workflow) to more advanced leadership concepts (avoiding favoritism).  The job was complicated by the large size of warehouses (850,000 sqft+) and surprisingly limited technology available to Amazon managers.  If a tool hadn't already been created at corporate, then you were out of luck; as an operator, it was nearly impossible to influence the way in which corporate Amazon allocated tech/development resources. 

One of the biggest pain points as an operations leader was managing where associates are assigned to work for a given shift (which workstation, area, process path, etc).  This is completely non-technological process at Amazon, and worked as follows: Each department had a large rolling whiteboard in their area, called the "labor tracking board." On this whiteboard is a visual representation/diagram of the different workstations in the department.  Associates would be assigned to each workstation using a laminated, magnetic name-badge (or just their name hand-written in, if their name-badge had gone missing as they often did).  And that's it!

Even if you have no operations experience, there are a number of problems and opportunities with this approach.  How does a manager know where an associate is working, if they can't see the whiteboard?  If a manager shifts an associate from one workstation to another, how is this communicated to other leaders that are running the department?  How do you plan ahead for the next shift without clearing the board and losing track of where everyone is currently assigned?  What if an associate moves their own name-badge to pick where they want to work?  These might seem like small issues, but they can easily amount to miscommunications that have large financial impact on any given shift.

My capstone will alleviate these problems by digitizing the labor tracking board.  After performing a one-time configuration to define and visually diagram their work space, managers will assign employees to workstations electronically through the application.  Multiple managers will be able to login and see the same dashboard to track associate assignments in real-time.   Furthermore, a digital labor tracking board enables several additional enhancements that will add value to managers and associates alike: algorithm-based workstation assignments for each shift, improved assignment communication with associates, and easier oversight for senior leadership. 


### Features
---
###### Confiuration:
A manager will first need to define their work space.  This will be done either visually with a SVG diagram or with data entry into a table/spreadsheet.  Also, a manager will have to define the different roles in their workspace.  A single role type will be assigned to a workstation/node. Each workstation/node will also be assigned to a given zone, which will help with calculating throughput/flow for each step of the operation.  

###### Manager use: 
Before a shift, a manager will generate the employee assignments.  This will be done either manually (graphically drag and drop associate cards onto nodes of the work space diagram, or using drop-down selectors for non-graphical interface) or automatically with a button click (using a rotation-based algorithm).  Once the shift has started, managers will use the app to move employees between work stations as needed.  These moves will be rendered in real-time on the website, so that other users can view then.  Based on the workstation configurations, a throughput will be calculated for each zone and compared against the zones that are upstream/downstream on a dashboard.  This will help with managing flow and optimizing productivity.

###### Employee use:
An associate will have a kiosk where they can scan their badge and be shown which workstation they are assigned to. 

##### User Stories:
1. As a manager, I want to be able to view up-to-date workstation assignments for every associate so I can make timely labor adjustments based on shifting business needs.
2. As a manager, I want to be able to generate an entire set of associate/workstation shift assignments to save me time preparing for the next shift and to protect me from perceived favoritism that might result if I manually assign people.
3. As a manager, I want to make sure I only assign qualified, trained associates to a given process path to ensure employee safety and quality for those downstream of my operation.
4. As a manager, I want to see an automatic calculation of my volume flow/throughput based on how my employees are assigned to help me make the correct business decisions and labor moves. 
5. As an employee, I want to see where I am assigned as soon as I clock in so that I can get to work. 
6. As an employee, I want to be rotated between all of the positions that I am trained for to make sure I am not stuck doing the same thing every day.

##### Tasks:
- Build models: managers, employees, organization, workspace, flowpath, node, zone, role
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

### Data Model
---


### Schedule
---

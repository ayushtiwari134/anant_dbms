from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///construction.db'
db = SQLAlchemy(app)

# Projects Table
class Project(db.Model):
    ProjectID = db.Column(db.Integer, primary_key=True)
    ProjectName = db.Column(db.String(50), nullable=False)
    Location = db.Column(db.String(50), nullable=False)
    StartDate = db.Column(db.String(20), nullable=False)
    EndDate = db.Column(db.String(20), nullable=False)
    ProjectManagerID = db.Column(db.Integer, db.ForeignKey('employee.EmployeeID'), nullable=False)

# Employees Table
class Employee(db.Model):
    EmployeeID = db.Column(db.Integer, primary_key=True)
    FirstName = db.Column(db.String(50), nullable=False)
    LastName = db.Column(db.String(50), nullable=False)
    ContactNumber = db.Column(db.String(15), nullable=False)
    Designation = db.Column(db.String(50), nullable=False)
    Skills = db.Column(db.String(100), nullable=False)
    ProjectID = db.Column(db.Integer, db.ForeignKey('project.ProjectID'))

# Resources Table
class Resource(db.Model):
    ResourceID = db.Column(db.Integer, primary_key=True)
    ResourceType = db.Column(db.String(50), nullable=False)
    ResourceName = db.Column(db.String(50), nullable=False)
    AvailabilityStatus = db.Column(db.String(20), nullable=False)
    MaintenanceSchedule = db.Column(db.String(50), nullable=True)

# Tasks Table
class Task(db.Model):
    TaskID = db.Column(db.Integer, primary_key=True)
    TaskName = db.Column(db.String(50), nullable=False)
    ProjectID = db.Column(db.Integer, db.ForeignKey('project.ProjectID'), nullable=False)
    EmployeeID = db.Column(db.Integer, db.ForeignKey('employee.EmployeeID'), nullable=False)
    StartDate = db.Column(db.String(20), nullable=False)
    EndDate = db.Column(db.String(20), nullable=False)
    CompletionStatus = db.Column(db.String(20), nullable=False)

# Clients Table
class Client(db.Model):
    ClientID = db.Column(db.Integer, primary_key=True)
    ClientName = db.Column(db.String(50), nullable=False)
    ContactPerson = db.Column(db.String(50), nullable=False)
    ContactNumber = db.Column(db.String(15), nullable=False)
    ProjectRequirements = db.Column(db.String(200), nullable=True)

# Create tables
with app.app_context():
    db.create_all()

# Sample data
sample_data = {
    'projects': [
        {'ProjectName': 'Project A', 'Location': 'City A', 'StartDate': '2024-03-01', 'EndDate': '2024-12-31', 'ProjectManagerID': 1},
        {'ProjectName': 'Project B', 'Location': 'City B', 'StartDate': '2024-04-01', 'EndDate': '2024-11-30', 'ProjectManagerID': 2},
        # Add more project data as needed
    ],
    'employees': [
        {'FirstName': 'John', 'LastName': 'Doe', 'ContactNumber': '123-456-7890', 'Designation': 'Engineer', 'Skills': 'Civil, Structural', 'ProjectID': 1},
        {'FirstName': 'Jane', 'LastName': 'Smith', 'ContactNumber': '987-654-3210', 'Designation': 'Architect', 'Skills': 'Architectural Design', 'ProjectID': 2},
        # Add more employee data as needed
    ],
    'resources': [
        {'ResourceType': 'Material', 'ResourceName': 'Concrete', 'AvailabilityStatus': 'Available', 'MaintenanceSchedule': 'Monthly'},
        {'ResourceType': 'Equipment', 'ResourceName': 'Excavator', 'AvailabilityStatus': 'In Use', 'MaintenanceSchedule': 'Bi-Weekly'},
        # Add more resource data as needed
    ],
    'tasks': [
        {'TaskName': 'Foundation Work', 'ProjectID': 1, 'EmployeeID': 1, 'StartDate': '2024-03-10', 'EndDate': '2024-03-25', 'CompletionStatus': 'Incomplete'},
        {'TaskName': 'Architectural Design', 'ProjectID': 2, 'EmployeeID': 2, 'StartDate': '2024-04-15', 'EndDate': '2024-05-01', 'CompletionStatus': 'Incomplete'},
        # Add more task data as needed
    ],
    'clients': [
        {'ClientName': 'Client X', 'ContactPerson': 'Mr. X', 'ContactNumber': '555-123-4567', 'ProjectRequirements': 'High-rise building construction'},
        {'ClientName': 'Client Y', 'ContactPerson': 'Ms. Y', 'ContactNumber': '555-987-6543', 'ProjectRequirements': 'Residential development'},
        # Add more client data as needed
    ]
}

# Insert sample data into tables
with app.app_context():
    for table_name, data in sample_data.items():
        class_name = table_name[:-1].capitalize()
        model_class = globals()[class_name]
        
        for entry in data:
            # Check if an entry with the same data exists
            existing_entry = model_class.query.filter_by(**entry).first()
            
            if existing_entry is None:
                db.session.add(model_class(**entry))
                db.session.commit()

# Routes
@app.route('/')
def index():
    return render_template('index.html', projects=Project.query.all(),
                           employees=Employee.query.all(),
                           resources=Resource.query.all(),
                           tasks=Task.query.all(),
                           clients=Client.query.all())

# Routes for displaying individual HTML pages
@app.route('/projects')
def projects():
    return render_template('projects.html', projects=Project.query.all())

@app.route('/employees')
def employees():
    return render_template('employees.html', employees=Employee.query.all())

@app.route('/resources')
def resources():
    return render_template('resources.html', resources=Resource.query.all())

@app.route('/tasks')
def tasks():
    return render_template('tasks.html', tasks=Task.query.all())

@app.route('/clients')
def clients():
    return render_template('clients.html', clients=Client.query.all())

@app.route('/add_project', methods=['POST'])
def add_project():
    if request.method == 'POST':
        project_name = request.form['project_name']
        location = request.form['location']
        start_date = request.form['start_date']
        end_date = request.form['end_date']
        project_manager_id = request.form['project_manager_id']

        # Validate or sanitize input if necessary

        new_project = Project(ProjectName=project_name, Location=location, StartDate=start_date,
                              EndDate=end_date, ProjectManagerID=project_manager_id)

        db.session.add(new_project)
        db.session.commit()

    return redirect(url_for('index'))

@app.route('/add_employee', methods=['POST'])
def add_employee():
    if request.method == 'POST':
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        contact_number = request.form['contact_number']
        designation = request.form['designation']
        skills = request.form['skills']
        project_id = request.form['project_id']

        new_employee = Employee(FirstName=first_name, LastName=last_name, ContactNumber=contact_number,
                                Designation=designation, Skills=skills, ProjectID=project_id)

        db.session.add(new_employee)
        db.session.commit()

    return redirect(url_for('index'))

@app.route('/add_resource', methods=['POST'])
def add_resource():
    if request.method == 'POST':
        resource_type = request.form['resource_type']
        resource_name = request.form['resource_name']
        availability_status = request.form['availability_status']
        maintenance_schedule = request.form['maintenance_schedule']

        new_resource = Resource(ResourceType=resource_type, ResourceName=resource_name,
                                AvailabilityStatus=availability_status, MaintenanceSchedule=maintenance_schedule)

        db.session.add(new_resource)
        db.session.commit()

    return redirect(url_for('resources'))

@app.route('/add_task', methods=['POST'])
def add_task():
    if request.method == 'POST':
        task_name = request.form['task_name']
        project_id = request.form['projecT_id']
        employee_id = request.form['employee_id']
        start_date = request.form['start_date']
        end_date = request.form['end_date']
        completion_status = request.form['completion_status']

        new_task = Task(TaskName=task_name, ProjectID=project_id, EmployeeID=employee_id,
                        StartDate=start_date, EndDate=end_date, CompletionStatus=completion_status)

        db.session.add(new_task)
        db.session.commit()

    return redirect(url_for('tasks'))

@app.route('/add_client', methods=['POST'])
def add_client():
    if request.method == 'POST':
        client_name = request.form['client_name']
        contact_person = request.form['contact_person']
        contact_number = request.form['contact_number']
        project_requirements = request.form['project_requirements']

        new_client = Client(ClientName=client_name, ContactPerson=contact_person,
                            ContactNumber=contact_number, ProjectRequirements=project_requirements)

        db.session.add(new_client)
        db.session.commit()

    return redirect(url_for('clients'))


# Routes for modifying data
@app.route('/modify_project/<int:id>', methods=['POST'])
def modify_project(id):
    project = Project.query.get_or_404(id)
    if request.method == 'POST':
        project.ProjectName = request.form['project_name']
        project.Location = request.form['location']
        project.StartDate = request.form['start_date']
        project.EndDate = request.form['end_date']
        project.ProjectManagerID = request.form['project_manager_id']

        db.session.commit()

    return redirect(url_for('index'))

@app.route('/modify_employee/<int:id>', methods=['POST'])
def modify_employee(id):
    employee = Employee.query.get_or_404(id)
    if request.method == 'POST':
        employee.FirstName = request.form['first_name']
        employee.LastName = request.form['last_name']
        employee.ContactNumber = request.form['contact_number']
        employee.Designation = request.form['designation']
        employee.Skills = request.form['skills']
        employee.ProjectID = request.form['project_id']

        db.session.commit()

    return redirect(url_for('index'))

@app.route('/modify_resource/<int:id>', methods=['POST'])
def modify_resource(id):
    resource = Resource.query.get_or_404(id)
    if request.method == 'POST':
        resource.ResourceType = request.form['resource_type']
        resource.ResourceName = request.form['resource_name']
        resource.AvailabilityStatus = request.form['availability_status']
        resource.MaintenanceSchedule = request.form['maintenance_schedule']

        db.session.commit()

    return redirect(url_for('resources'))

@app.route('/modify_task/<int:id>', methods=['POST'])
def modify_task(id):
    task = Task.query.get_or_404(id)
    if request.method == 'POST':
        task.TaskName = request.form['task_name']
        task.ProjectID = request.form['project_id']
        task.EmployeeID = request.form['employee_id']
        task.StartDate = request.form['start_date']
        task.EndDate = request.form['end_date']
        task.CompletionStatus = request.form['completion_status']

        db.session.commit()

    return redirect(url_for('tasks'))

@app.route('/modify_client/<int:id>', methods=['POST'])
def modify_client(id):
    client = Client.query.get_or_404(id)
    if request.method == 'POST':
        client.ClientName = request.form['client_name']
        client.ContactPerson = request.form['contact_person']
        client.ContactNumber = request.form['contact_number']
        client.ProjectRequirements = request.form['project_requirements']

        db.session.commit()

    return redirect(url_for('clients'))



# Routes for deleting data
@app.route('/delete_project/<int:id>', methods=['POST'])
def delete_project(id):
    project = Project.query.get_or_404(id)
    db.session.delete(project)
    db.session.commit()
    return redirect(url_for('projects'))

@app.route('/delete_employee/<int:id>', methods=['POST'])
def delete_employee(id):
    employee = Employee.query.get_or_404(id)
    db.session.delete(employee)
    db.session.commit()
    return redirect(url_for('employees'))

@app.route('/delete_resource/<int:id>', methods=['POST'])
def delete_resource(id):
    resource = Resource.query.get_or_404(id)
    db.session.delete(resource)
    db.session.commit()
    return redirect(url_for('resources'))

@app.route('/delete_task/<int:id>', methods=['POST'])
def delete_task(id):
    task = Task.query.get_or_404(id)
    db.session.delete(task)
    db.session.commit()
    return redirect(url_for('tasks'))

@app.route('/delete_client/<int:id>', methods=['POST'])
def delete_client(id):
    client = Client.query.get_or_404(id)
    db.session.delete(client)
    db.session.commit()
    return redirect(url_for('clients'))

if __name__ == '__main__':
    app.run(debug=True)


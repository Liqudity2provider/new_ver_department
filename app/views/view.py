from datetime import date

from flask import render_template, request, flash
from sqlalchemy.sql import func

from app import app
from app.models.models import DepartmentModel, EmployeeModel


@app.template_filter('dateformat')
def dateformat(value, format='%B %d, %Y'):
    """Format function for date"""
    return value.strftime(format)


@app.route('/test')
def test():
    """route for test"""
    return 'test'


@app.route('/')
@app.route('/home')
def home():
    """Homepage,
    Display a list departments quantity;
    Display a list employees quantity;
    Display automatically calculated total salary
    """
    departments = DepartmentModel.query.all()
    employees = EmployeeModel.query.all()
    total_salary = EmployeeModel.query.with_entities(func.sum(EmployeeModel.salary)).first()

    return render_template('home.html', departments=departments, employees=employees, total_salary=total_salary)


@app.route('/departments')
def departments_page():
    """Departments table page
    Display list of departments with automatically calculated average salary"""
    departments = DepartmentModel.query.all()

    average_salary_query = EmployeeModel.query.with_entities(EmployeeModel.related_department_id, func.avg(
        EmployeeModel.salary)).group_by(
        EmployeeModel.related_department_id)
    average_salary = dict((department, salary) for department, salary in average_salary_query)

    return render_template('departments.html', departments=departments, average_salary=average_salary)


@app.route('/departments/<int:department_id>')
def department_page(department_id):
    """Department page,
    Display department name;
    Display average and total salary;
    Employees quantity in department
    """
    department = DepartmentModel.query.get_or_404(department_id)

    average_salary = EmployeeModel.query.with_entities(EmployeeModel.related_department_id, func.avg(
        EmployeeModel.salary)).group_by(
        EmployeeModel.related_department_id).all()
    average_salary = dict((key, value) for key, value in average_salary)

    total_salary = EmployeeModel.query.with_entities(EmployeeModel.related_department_id, func.sum(
        EmployeeModel.salary)).group_by(
        EmployeeModel.related_department_id).all()
    total_salary = dict((key, value) for key, value in total_salary)

    return render_template(
        'department.html',
        department=department,
        average_salary=average_salary,
        total_salary=total_salary
    )


@app.route('/employees', methods=['GET', 'POST'])
def employees_page():
    """Display list of employees,
    Search field to search for employees born on a certain date or in the period between dates
    """
    employees = EmployeeModel.query.all()
    today = date.today()
    if request.method == 'POST':
        date_from = request.form['date_from']
        date_by = request.form['date_by']
        if date_from and date_by:
            employees = EmployeeModel.query.filter(EmployeeModel.date_of_birth <= date_by).filter(
                EmployeeModel.date_of_birth >= date_from)
            return render_template('employees.html', employees=employees, date_from=date_from, date_by=date_by)
        elif date_from:
            employees = EmployeeModel.query.filter(EmployeeModel.date_of_birth == date_from)
            return render_template('employees.html', employees=employees, date_from=date_from)
        elif date_by:
            employees = EmployeeModel.query.filter(EmployeeModel.date_of_birth == date_by)
            return render_template('employees.html', employees=employees, date_by=date_by)
        else:
            flash('Please enter at least one date for filter', 'error-filter')
            return render_template('employees.html', employees=employees)
    return render_template('employees.html', employees=employees, today=today)


@app.route('/employees/<int:employee_id>')
def employee_page(employee_id):
    """Employee page
    Display employee name, salary, date of birth and his/her department"""
    employee = EmployeeModel.query.get_or_404(employee_id)
    return render_template('employee.html', employee=employee)

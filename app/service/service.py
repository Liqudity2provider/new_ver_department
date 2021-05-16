from datetime import date

import requests
import json
from flask import render_template, request, redirect, url_for, flash

from app import app
from app.models.models import DepartmentModel, EmployeeModel


path = 'http://127.0.0.1:5000/'
headers = {'Content-Type': 'application/json'}


@app.route('/add_department')
def add_department():
    """Add department page"""
    return render_template('add_department.html')


@app.route('/add_department', methods=['POST'])
def add_department_post():
    """Add department to database;
    Flash error throw if department already exist"""
    if request.method == "POST":
        new_department = {
                'name': request.form['name']
            }
        response = requests.post(
            path + '/api/departments',
            headers=headers,
            data=json.dumps(new_department)
        )
        output = json.loads(response.text)
        if output.get('error'):
            flash(output['error'], 'error')
        else:
            flash('New department added', 'success')
        return redirect(url_for('departments_page'))


@app.route('/edit_department/<int:department_id>', methods=['GET', 'POST'])
def edit_department(department_id):
    """Edit department page"""
    department = DepartmentModel.query.get_or_404(department_id)

    if request.method == 'POST':
        department = {
            'name': request.form['name']
        }
        response = requests.put(path + '/api/departments/' + str(department_id),
                                headers=headers,
                                data=json.dumps(department))
        output = json.loads(response.text)
        if output.get('error'):
            flash(output['error'], 'error')
        else:
            flash('Department updated', 'success')
        return redirect(url_for('departments_page'))

    return render_template('edit_department.html', department=department)


@app.route('/departments/<int:department_id>/delete', methods=['GET', 'POST'])
def delete_department(department_id):
    """Delete department from database"""
    DepartmentModel.query.get_or_404(department_id)
    requests.delete(path + '/api/departments/' + str(department_id), headers=headers)
    flash('Department deleted', 'success')
    return redirect(url_for('departments_page'))


@app.route('/add_employee')
def add_employee():
    """Add employee page"""
    departments = DepartmentModel.query.all()
    today = date.today()
    return render_template('add_employee.html', departments=departments, today=today)


@app.route('/add_employee', methods=['POST'])
def add_employee_post():
    """Add employee to database"""
    if request.method == 'POST':
        new_employee = {
            'related_department_id': request.form['related_department_id'],
            'name': request.form['name'],
            'date_of_birth': request.form['date_of_birth'],
            'salary': request.form['salary']
        }
        response = requests.post(path + '/api/employees', headers=headers, data=json.dumps(new_employee))
        output = json.loads(response.text)
        if output.get('error'):
            flash(output['error'], 'error')
        else:
            flash('New employee added', 'success')
        return redirect(url_for('employees_page'))


@app.route('/edit_employee/<int:employee_id>', methods=['GET', 'POST'])
def edit_employee(employee_id):
    """Edit employee"""
    employee = EmployeeModel.query.get_or_404(employee_id)
    departments = DepartmentModel.query.all()
    today = date.today()
    if request.method == 'POST':
        employee = {
            'related_department_id': request.form['related_department_id'],
            'name': request.form['name'],
            'date_of_birth': request.form['date_of_birth'],
            'salary': request.form['salary']
        }
        response = requests.put(path + '/api/employees/' + str(employee_id), data=json.dumps(employee), headers=headers)
        output = json.loads(response.text)
        if output.get('error'):
            flash(output['error'], 'error')
        else:
            flash('Employee info updated')
        return redirect(url_for('employees_page'))

    return render_template('edit_employee.html', employee=employee, departments=departments, today=today)


@app.route('/employees/<int:employee_id>/delete', methods=['GET', 'POST'])
def delete_employee(employee_id):
    """Delete department from database"""
    EmployeeModel.query.get_or_404(employee_id)
    requests.delete(path + '/api/employees/' + str(employee_id), headers=headers)
    flash('Employee deleted', 'success')
    return redirect(url_for('employees_page'))

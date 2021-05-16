from datetime import datetime

from flask import request
from flask_restful import Resource
from sqlalchemy.exc import IntegrityError, OperationalError

from app.models.models import DepartmentModel, EmployeeModel, DepartmentSchema, EmployeeSchema
from app import db

department_schema = DepartmentSchema()
departments_schema = DepartmentSchema(many=True)
employee_schema = EmployeeSchema()
employees_schema = EmployeeSchema(many=True)


class DepartmentList(Resource):
    """Read all departments;
    create new department"""

    def get(self):
        """Get method to list all departments"""
        departments = DepartmentModel.query.all()
        return departments_schema.dump(departments)

    def post(self):
        """Post method to add new department"""
        try:
            new_department = DepartmentModel(
                name=request.json['name']
            )
            db.session.add(new_department)
            db.session.commit()
        except IntegrityError:
            db.session.rollback()
            return {"error": "This department already exist"}

        return department_schema.dump(new_department), 201


class Department(Resource):
    """Read, update and delete department"""

    def get(self, department_id):
        """Get method to list department"""
        department = DepartmentModel.query.get_or_404(department_id)
        return department_schema.dump(department)

    def put(self, department_id):
        """Put method for update department"""
        department = DepartmentModel.query.get_or_404(department_id)

        try:
            department.name = request.json.get('name', department.name)
            db.session.commit()
            return department_schema.dump(department)
        except IntegrityError:
            db.session.rollback()
            return {"error": "This department already exist"}

    def delete(self, department_id):
        """Delete method for delete department"""
        department = DepartmentModel.query.get_or_404(department_id)
        db.session.delete(department)
        db.session.commit()
        return '', 204


class EmployeeList(Resource):
    """Read all employees;
    create new employee
    """

    def get(self):
        """Get method for list all employees"""
        employees = EmployeeModel.query.all()
        return employees_schema.dump(employees)

    def post(self):
        """Post method to add new employee"""
        try:
            new_employee = EmployeeModel(
                related_department_id=request.json['related_department_id'],
                name=request.json['name'],
                date_of_birth=request.json['date_of_birth'],
                salary=request.json['salary']
            )
            if int(new_employee.salary) < 1000:
                return {"error": "Minimum salary for employee must be more than $1000"}
            db.session.add(new_employee)
            db.session.commit()
        except OperationalError:
            db.session.rollback()
            return {"error": "Incorrect value enter error"}
        except ValueError:
            return {"error": "Incorrect value enter error"}
        return employee_schema.dump(new_employee), 201


class Employee(Resource):
    """Read, update and delete employee"""

    def get(self, employee_id):
        """Get method to list employee"""
        employee = EmployeeModel.query.get_or_404(employee_id)
        return employee_schema.dump(employee)

    def put(self, employee_id):
        """Put method to update employee"""
        employee = EmployeeModel.query.get_or_404(employee_id)
        try:
            employee.related_department_id = request.json.get('related_department_id', employee.related_department_id)
            employee.name = request.json.get('name', employee.name)
            employee.date_of_birth = request.json.get('date_of_birth', employee.date_of_birth)
            employee.salary = request.json.get('salary', employee.salary)
            db.session.commit()
            return employee_schema.dump(employee)
        except OperationalError:
            return {"error": "Incorrect data entered"}
        except ValueError:
            return {"error": "Incorrect data entered"}

    def delete(self, employee_id):
        """Delete method for delete employee"""
        employee = EmployeeModel.query.get_or_404(employee_id)
        db.session.delete(employee)
        db.session.commit()
        return '', 204

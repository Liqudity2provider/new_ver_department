from flask_restful import Resource
from sqlalchemy.sql import func

from app.models.models import EmployeeModel, DepartmentSchema, EmployeeSchema
from app import db

department_schema = DepartmentSchema()
departments_schema = DepartmentSchema(many=True)
employee_schema = EmployeeSchema()
employees_schema = EmployeeSchema(many=True)


class DateFilter(Resource):
    """Filter employees by date of birth"""

    def get(self, date_from, date_by):
        """Filter employees by date of birth between 2 dates"""
        employees = EmployeeModel.query.filter(EmployeeModel.date_of_birth <= date_by).filter(
            EmployeeModel.date_of_birth >= date_from)
        return employees_schema.dump(employees)


class CertainDateFilter(Resource):
    """Filter employees from certain date"""
    def get(self, date):
        """List employees from certain date"""
        employees = EmployeeModel.query.filter(EmployeeModel.date_of_birth == date)
        return employees_schema.dump(employees)


class AverageSalary(Resource):
    """Calculate average departments salary"""

    def get(self):
        """List department and average department salary"""
        sql_query = 'select * from department,' \
                    ' (select employee.related_department_id, avg(employee.salary) as salary' \
                    ' from employee group by related_department_id ) as result' \
                    ' where result.related_department_id = department.id;'
        result = db.session.execute(sql_query)
        return employees_schema.dump(result)


class TotalSalary(Resource):
    """Calculate total company salary"""

    def get(self):
        total_salary = EmployeeModel.query.with_entities(func.sum(EmployeeModel.salary).label("salary"))
        return employees_schema.dump(total_salary)

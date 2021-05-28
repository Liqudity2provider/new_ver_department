from app.rest.crud import DepartmentList, Department, EmployeeList, Employee
from app.rest.calculations import DateFilter, CertainDateFilter, AverageSalary, TotalSalary
from app import app, api, db, create_app
from app.rest import crud
from app.views import view
from app.service import service


"""Api endpoints"""
api.add_resource(DepartmentList, '/api/departments')
api.add_resource(Department, '/api/departments/<int:department_id>')
api.add_resource(EmployeeList, '/api/employees')
api.add_resource(Employee, '/api/employees/<int:employee_id>')
api.add_resource(DateFilter, '/api/date_filter/<string:date_from>-<string:date_by>')
api.add_resource(CertainDateFilter, '/api/date_filter/<string:date>')
api.add_resource(AverageSalary, '/api/average_salary')
api.add_resource(TotalSalary, '/api/total_salary')


if __name__ == '__main__':
    db.create_all(app=app)
    app.run()

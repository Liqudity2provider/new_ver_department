import unittest

import json
from flask import url_for
import datetime

from app.tests import TestBase


class ApiTest(TestBase):
    """Test REST API"""

    API_URL = 'http://localhost/api'
    DEPARTMENTS_URL = f'{API_URL}/departments'
    EMPLOYEES_URL = f'{API_URL}/employees'
    DATE_FILTER_RANGE_URL = f'{API_URL}/date_filter/'
    DATE_FILTER_URL = f'{API_URL}/date_filter/'
    AVERAGE_SALARY = f'{API_URL}/average_salary'
    TOTAL_SALARY = f'{API_URL}/total_salary'
    HEADERS = {'content-type': 'application/json'}

    DEPARTMENT_OBJECT_TEST = {
        'name': 'Unittestapi'
    }

    UPDATE_DEPARTMENT = {
        "name": "Production update"
    }
    # s_datetime = datetime.datetime.strptime(s, '%Y%m%d')

    EMPLOYEE_OBJECT_TEST = {
        "name": "Test employee",
        "salary": "5555",
        "related_department_id": "1",
        "date_of_birth": "1998:11:11"
    }

    EMPLOYEE_OBJECT_LOW_SALARY_TEST = {
        "name": "Test employee",
        "salary": "900",
        "related_department_id": "1",
        "date_of_birth": "981111"
    }

    EMPLOYEE_OBJECT_WRONG_DATE_TEST = {
        "name": "Test employee",
        "salary": "5555",
        "related_department_id": "1",
        "date_of_birth": 983451111
    }

    UPDATE_EMPLOYEE = {
        "name": "Update employee",
        "salary": "6666",
        "related_department_id": "1",
        "date_of_birth": "1999:12:12"
    }

    DATE_EMPLOYEE = {
        "name": "Update employee",
        "salary": "6666",
        "related_department_id": "2",
        "date_of_birth": "950405"
    }

    def test_01_get_departments(self):
        """Test list all departments"""
        response = self.app.get(ApiTest.DEPARTMENTS_URL)
        self.assertEqual(response.status_code, 200)

    def test_02_post_department(self):
        """Test post method"""
        response = self.app.post(ApiTest.DEPARTMENTS_URL, headers=ApiTest.HEADERS,
                                 data=json.dumps(ApiTest.DEPARTMENT_OBJECT_TEST))
        self.assertEqual(response.status_code, 201)

    def test_03_post_existed_department(self):
        """Test error if department already exist"""
        response = self.app.post(ApiTest.DEPARTMENTS_URL, headers=ApiTest.HEADERS,
                                 data=json.dumps(ApiTest.DEPARTMENT_OBJECT_TEST))
        self.assertEqual(response.status_code, 201)
        response = self.app.post(ApiTest.DEPARTMENTS_URL, headers=ApiTest.HEADERS,
                                 data=json.dumps(ApiTest.DEPARTMENT_OBJECT_TEST))
        output = json.loads(response.data)
        expected_response = {'error': 'This department already exist'}
        self.assertEqual(output, expected_response)

    def test_04_get_department(self):
        """Test get department"""
        self.app.post(ApiTest.DEPARTMENTS_URL, headers=ApiTest.HEADERS,
                      data=json.dumps(ApiTest.DEPARTMENT_OBJECT_TEST))
        response = self.app.get(ApiTest.DEPARTMENTS_URL + '/1')
        self.assertEqual(response.status_code, 200)
        expected_response = 'Unittestapi'
        output = json.loads(response.data)
        self.assertEqual(output['name'], expected_response)

    def test_05_get_department_404(self):
        """Error 404 for not existed department"""
        response = self.app.get(ApiTest.DEPARTMENTS_URL + '/143213')
        self.assertEqual(response.status_code, 404)

    def test_06_put_department(self):
        """Update department test"""
        self.app.post(ApiTest.DEPARTMENTS_URL, headers=ApiTest.HEADERS,
                      data=json.dumps(ApiTest.DEPARTMENT_OBJECT_TEST))
        response = self.app.put(ApiTest.DEPARTMENTS_URL + '/1',
                                headers=ApiTest.HEADERS,
                                data=json.dumps(ApiTest.UPDATE_DEPARTMENT))
        self.assertEqual(response.status_code, 200)
        output = json.loads(response.data)
        expected_response = 'Production update'
        self.assertEqual(output['name'], expected_response)
        update_department_back = {
            "name": "Production"
        }
        response_2 = self.app.put(ApiTest.DEPARTMENTS_URL + '/1', headers=ApiTest.HEADERS,
                                  data=json.dumps(update_department_back))
        output = json.loads(response_2.data)
        expected_response_2 = 'Production'
        self.assertEqual(output['name'], expected_response_2)

    def test_07_put_department_existed_error(self):
        """Update department test error (department already exist)"""
        self.app.post(ApiTest.DEPARTMENTS_URL, headers=ApiTest.HEADERS,
                      data=json.dumps(ApiTest.DEPARTMENT_OBJECT_TEST))
        self.app.post(ApiTest.DEPARTMENTS_URL, headers=ApiTest.HEADERS,
                      data=json.dumps(ApiTest.UPDATE_DEPARTMENT))
        response = self.app.put(ApiTest.DEPARTMENTS_URL + '/2',
                                headers=ApiTest.HEADERS,
                                data=json.dumps(ApiTest.DEPARTMENT_OBJECT_TEST))
        output = json.loads(response.data)
        expected_response = {'error': 'This department already exist'}
        self.assertEqual(output, expected_response)

    def test_08_delete_department(self):
        """Delete department test"""
        response = self.app.post(ApiTest.DEPARTMENTS_URL, headers=ApiTest.HEADERS,
                                 data=json.dumps(ApiTest.UPDATE_DEPARTMENT))
        output = json.loads(response.data)
        response_delete = self.app.delete(ApiTest.DEPARTMENTS_URL + '/' + str(output['id']), headers=ApiTest.HEADERS)
        self.assertEqual(response_delete.status_code, 204)

    def test_09_delete_department_404(self):
        """Delete not existed department 404 test"""
        response = self.app.delete(ApiTest.DEPARTMENTS_URL + '/2143564326', headers=ApiTest.HEADERS)
        self.assertEqual(response.status_code, 404)

    def test_10_get_employees(self):
        """Get employees list test"""
        response = self.app.get(ApiTest.EMPLOYEES_URL)
        self.assertEqual(response.status_code, 200)

    def test_11_post_employee(self):
        """Create employee test"""

        self.app.post(ApiTest.DEPARTMENTS_URL, headers=ApiTest.HEADERS,
                      data=json.dumps(ApiTest.DEPARTMENT_OBJECT_TEST))
        response = self.app.post(ApiTest.EMPLOYEES_URL, headers=ApiTest.HEADERS,
                                 data=json.dumps(ApiTest.EMPLOYEE_OBJECT_TEST))
        self.assertEqual(response.status_code, 201)

    def test_12_post_employee_low_salary(self):
        """Create employee with wrong input data"""
        response = self.app.post(ApiTest.EMPLOYEES_URL, headers=ApiTest.HEADERS,
                                 data=json.dumps(ApiTest.EMPLOYEE_OBJECT_LOW_SALARY_TEST))
        output = json.loads(response.data)
        expected_response = {"error": "Minimum salary for employee must be more than $1000"}
        self.assertEqual(output, expected_response)

    def test_14_get_employee(self):
        """Get employee test"""
        self.app.post(ApiTest.DEPARTMENTS_URL, headers=ApiTest.HEADERS,
                      data=json.dumps(ApiTest.DEPARTMENT_OBJECT_TEST))
        self.app.post(ApiTest.EMPLOYEES_URL, headers=ApiTest.HEADERS,
                      data=json.dumps(ApiTest.EMPLOYEE_OBJECT_TEST))
        response = self.app.get(ApiTest.EMPLOYEES_URL + '/1')
        self.assertEqual(response.status_code, 200)
        output = json.loads(response.data)
        self.assertEqual(output['name'], 'Test employee')

    def test_15_get_employee_404(self):
        """Get not existed employee 404 test"""
        response = self.app.get(ApiTest.EMPLOYEES_URL + '/1414124')
        self.assertEqual(response.status_code, 404)

    def test_16_update_employee(self):
        """Update employee info test"""
        self.app.post(ApiTest.DEPARTMENTS_URL, headers=ApiTest.HEADERS,
                      data=json.dumps(ApiTest.DEPARTMENT_OBJECT_TEST))
        self.app.post(ApiTest.EMPLOYEES_URL, headers=ApiTest.HEADERS,
                      data=json.dumps(ApiTest.EMPLOYEE_OBJECT_TEST))
        response = self.app.put(ApiTest.EMPLOYEES_URL + '/1', headers=ApiTest.HEADERS,
                                data=json.dumps(ApiTest.UPDATE_EMPLOYEE))
        self.assertEqual(response.status_code, 200)
        output = json.loads(response.data)
        self.assertEqual(output['name'], 'Update employee')
        employee_undo = {
            "name": "Adam Barness",
            "salary": "6422",
            "related_department_id": "1",
            "date_of_birth": "951111"
        }
        response_undo = self.app.put(ApiTest.EMPLOYEES_URL + '/1', headers=ApiTest.HEADERS,
                                     data=json.dumps(employee_undo))
        self.assertEqual(response_undo.status_code, 200)
        output = json.loads(response_undo.data)
        self.assertEqual(output['name'], 'Adam Barness')

    def test_17_update_employee_wrong_input(self):
        """Update employee with wrong input error test"""

        response = self.app.put(ApiTest.EMPLOYEES_URL + '/1', headers=ApiTest.HEADERS,
                                data=json.dumps(ApiTest.EMPLOYEE_OBJECT_WRONG_DATE_TEST))
        output = json.loads(response.data)
        expected_response = {
            "message": "The requested URL was not found on the server. If you entered the URL manually please check your spelling and try again."}
        self.assertEqual(output, expected_response)

    def test_18_delete_employee(self):
        """Delete employee test"""
        self.app.post(ApiTest.DEPARTMENTS_URL, headers=ApiTest.HEADERS,
                      data=json.dumps(ApiTest.DEPARTMENT_OBJECT_TEST))
        self.app.post(ApiTest.EMPLOYEES_URL, headers=ApiTest.HEADERS,
                      data=json.dumps(ApiTest.EMPLOYEE_OBJECT_TEST))
        response = self.app.post(ApiTest.EMPLOYEES_URL, headers=ApiTest.HEADERS,
                                 data=json.dumps(ApiTest.UPDATE_EMPLOYEE))
        output = json.loads(response.data)
        response_delete = self.app.delete(ApiTest.EMPLOYEES_URL + '/' + str(output['id']), headers=ApiTest.HEADERS)
        self.assertEqual(response_delete.status_code, 204)

    def test_19_delete_employee_404(self):
        """Delete not existed employee 404 test"""
        response = self.app.delete(ApiTest.EMPLOYEES_URL + '/2143564326', headers=ApiTest.HEADERS)
        self.assertEqual(response.status_code, 404)

    def test_20_date_filter(self):
        """Test date filter"""
        self.app.post(ApiTest.DEPARTMENTS_URL, headers=ApiTest.HEADERS,
                      data=json.dumps(ApiTest.DEPARTMENT_OBJECT_TEST))
        self.app.post(ApiTest.EMPLOYEES_URL, headers=ApiTest.HEADERS,
                      data=json.dumps(ApiTest.EMPLOYEE_OBJECT_TEST))
        self.app.post(ApiTest.EMPLOYEES_URL, headers=ApiTest.HEADERS,
                      data=json.dumps(ApiTest.UPDATE_EMPLOYEE))
        response = self.app.get(ApiTest.DATE_FILTER_RANGE_URL + '1998:11:17-2000:01:01')

        expected_output = [{'date_of_birth': '1999:12:12',
                            'id': 2,
                            'name': 'Update employee',
                            'related_department_id': 1,
                            'salary': 6666.0}
                           ]
        output = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(output, expected_output)

    def test_21_certain_date_filter(self):
        """Test certain date employees filter"""
        self.app.post(ApiTest.DEPARTMENTS_URL, headers=ApiTest.HEADERS,
                      data=json.dumps(ApiTest.DEPARTMENT_OBJECT_TEST))
        self.app.post(ApiTest.EMPLOYEES_URL, headers=ApiTest.HEADERS,
                      data=json.dumps(ApiTest.EMPLOYEE_OBJECT_TEST))
        response = self.app.get(ApiTest.DATE_FILTER_URL + '1998:11:11')
        output = json.loads(response.data)
        expected_output = [{
            "name": "Test employee",
            "salary": 5555.0,
            "related_department_id": 1,
            "date_of_birth": "1998:11:11",
            "id": 1
        }]
        self.assertEqual(response.status_code, 200)
        self.assertEqual(output, expected_output)

    def test_22_average_salary(self):
        """Test for average department salary"""
        self.app.post(ApiTest.DEPARTMENTS_URL, headers=ApiTest.HEADERS,
                      data=json.dumps(ApiTest.DEPARTMENT_OBJECT_TEST))
        self.app.post(ApiTest.EMPLOYEES_URL, headers=ApiTest.HEADERS,
                      data=json.dumps(ApiTest.EMPLOYEE_OBJECT_TEST))
        self.app.post(ApiTest.EMPLOYEES_URL, headers=ApiTest.HEADERS,
                      data=json.dumps(ApiTest.UPDATE_EMPLOYEE))
        response = self.app.get(ApiTest.AVERAGE_SALARY)
        output = json.loads(response.data)
        expected_output = [{'id': 1, 'salary': 6110.5, 'name': 'Unittestapi', 'related_department_id': 1}]
        self.assertEqual(response.status_code, 200)
        self.assertEqual(output, expected_output)

    def test_23_total_salary(self):
        """Test for total company salary"""
        self.app.post(ApiTest.DEPARTMENTS_URL, headers=ApiTest.HEADERS,
                      data=json.dumps(ApiTest.DEPARTMENT_OBJECT_TEST))
        self.app.post(ApiTest.EMPLOYEES_URL, headers=ApiTest.HEADERS,
                      data=json.dumps(ApiTest.EMPLOYEE_OBJECT_TEST))
        self.app.post(ApiTest.EMPLOYEES_URL, headers=ApiTest.HEADERS,
                      data=json.dumps(ApiTest.UPDATE_EMPLOYEE))
        response = self.app.get(ApiTest.TOTAL_SALARY)
        output = json.loads(response.data)
        expected_output = [{'salary': 12221.0}]
        self.assertEqual(response.status_code, 200)
        self.assertEqual(output, expected_output)


class ViewsTest(TestBase):
    """Views unit tests"""

    URL = 'http://127.0.0.1:5000'

    def test_homepage(self):
        """Test access to homepage"""
        response = self.app.get(url_for('home'))
        self.assertEqual(response.status_code, 200)

    def test_departments_page(self):
        """Test access to departments page"""
        response = self.app.get(url_for('departments_page'))
        self.assertEqual(response.status_code, 200)

    def test_department_page(self):
        """Test access to department page"""
        self.app.post(ApiTest.DEPARTMENTS_URL, headers=ApiTest.HEADERS,
                      data=json.dumps(ApiTest.DEPARTMENT_OBJECT_TEST))
        self.app.post(ApiTest.EMPLOYEES_URL, headers=ApiTest.HEADERS,
                      data=json.dumps(ApiTest.EMPLOYEE_OBJECT_TEST))

        response = self.app.get(ViewsTest.URL + '/departments/1')
        self.assertEqual(response.status_code, 200)

    def test_department_page_404(self):
        response = self.app.get(ViewsTest.URL + '/departments/notexisted')
        self.assertEqual(response.status_code, 404)

    def test_employees_page(self):
        """Test access to employees page"""
        response = self.app.get(url_for('employees_page'))
        self.assertEqual(response.status_code, 200)

    def test_employees_filter(self):
        """Test filter on employees page"""
        response = self.app.post(ViewsTest.URL + '/employees', data=dict(
            date_from='980101',
            date_by='990101'
        ))
        self.assertEqual(response.status_code, 200)

    def test_employee_page(self):
        """Test access to employee page"""
        self.app.post(ApiTest.DEPARTMENTS_URL, headers=ApiTest.HEADERS,
                      data=json.dumps(ApiTest.DEPARTMENT_OBJECT_TEST))
        self.app.post(ApiTest.EMPLOYEES_URL, headers=ApiTest.HEADERS,
                      data=json.dumps(ApiTest.EMPLOYEE_OBJECT_TEST))
        response = self.app.get(ViewsTest.URL + '/employees/1')
        self.assertEqual(response.status_code, 200)

    def test_employee_page_404(self):
        """Test not existed employee response"""
        response = self.app.get(ViewsTest.URL + '/emplyoees/notexisted')
        self.assertEqual(response.status_code, 404)

    def test_add_department_page(self):
        """Test add department response"""
        response = self.app.get(url_for('add_department'))

        self.assertEqual(response.status_code, 200)

    def test_edit_department_page(self):
        """Test edit department response"""
        self.app.post(ApiTest.DEPARTMENTS_URL, headers=ApiTest.HEADERS,
                      data=json.dumps(ApiTest.DEPARTMENT_OBJECT_TEST))
        response = self.app.get(ViewsTest.URL + '/departments/1')
        self.assertEqual(response.status_code, 200)

    def test_edit_department_page_404(self):
        """Test edit department response for not existed department"""
        self.app.post(ApiTest.DEPARTMENTS_URL, headers=ApiTest.HEADERS,
                      data=json.dumps(ApiTest.DEPARTMENT_OBJECT_TEST))
        response = self.app.get(ViewsTest.URL + '/departments/notexisted')
        self.assertEqual(response.status_code, 404)

    def test_add_employee_page(self):
        """Test add employee response"""
        response = self.app.get(url_for('add_employee'))
        self.assertEqual(response.status_code, 200)

    def test_edit_employee(self):
        """Test edit employee response"""
        self.app.post(ApiTest.DEPARTMENTS_URL, headers=ApiTest.HEADERS,
                      data=json.dumps(ApiTest.DEPARTMENT_OBJECT_TEST))
        self.app.post(ApiTest.EMPLOYEES_URL, headers=ApiTest.HEADERS,
                      data=json.dumps(ApiTest.EMPLOYEE_OBJECT_TEST))
        response = self.app.get(ViewsTest.URL + '/edit_employee/1')
        self.assertEqual(response.status_code, 200)

    def test_edit_employee_404(self):
        """Test edit employee response not existed employee"""
        self.app.post(ApiTest.DEPARTMENTS_URL, headers=ApiTest.HEADERS,
                      data=json.dumps(ApiTest.DEPARTMENT_OBJECT_TEST))
        self.app.post(ApiTest.EMPLOYEES_URL, headers=ApiTest.HEADERS,
                      data=json.dumps(ApiTest.EMPLOYEE_OBJECT_TEST))
        response = self.app.get(ViewsTest.URL + '/edit_employee/notexisted')
        self.assertEqual(response.status_code, 404)

    def test_error_404(self):
        """Test 404 error"""
        response = self.app.get(ViewsTest.URL + '/error404')
        self.assertEqual(response.status_code, 404)
        self.assertIn(b'Error 404', response.data)


if __name__ == '__main__':
    unittest.main()

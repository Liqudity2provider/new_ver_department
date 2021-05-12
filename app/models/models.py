from app import db, ma


class EmployeeModel(db.Model):
    """Create an Employee table"""
    __tablename__ = 'employee'

    id = db.Column(db.Integer, primary_key=True)
    related_department_id = db.Column(db.Integer, db.ForeignKey('department.id'))
    name = db.Column(db.String(40))
    date_of_birth = db.Column(db.Date)
    salary = db.Column(db.DECIMAL(asdecimal=False, precision=0, decimal_return_scale=0))


class EmployeeSchema(ma.SQLAlchemyAutoSchema):
    """Generate marshmallow schema for employee model"""
    class Meta:
        model = EmployeeModel
        include_fk = True


class DepartmentModel(db.Model):
    """Create Department table"""
    __tablename__ = 'department'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(25), unique=True)
    employees = db.relationship('EmployeeModel', backref='department', lazy='dynamic')


class DepartmentSchema(ma.SQLAlchemyAutoSchema):
    """Generate marshmallow schema for department model"""
    class Meta:
        model = DepartmentModel

    id = ma.auto_field()
    name = ma.auto_field()
    employees = ma.auto_field()

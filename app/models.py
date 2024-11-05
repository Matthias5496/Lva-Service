from . import db

class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(150), nullable=False)
    firstname = db.Column(db.String(50), nullable=False)
    lastname = db.Column(db.String(50), nullable=False)
    role = db.Column(db.String(50), nullable=False)

    assignments = db.relationship('Assignment', back_populates='student')
    registrations = db.relationship('Registration', back_populates='student')


class Lva(db.Model): 
    __tablename__ = 'lvas'

    lva_number = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(150), unique=True, nullable=False)
    description = db.Column(db.String(10000))
    instructor_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    instructor = db.relationship('User', backref='lvas_taught', foreign_keys=[instructor_id])
    exercises = db.relationship('Exercise', back_populates='lva')
    registrations = db.relationship('Registration', back_populates='lva')

class Exercise(db.Model):
    __tablename__ = 'exercises'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=True)
    lva_id = db.Column(db.Integer, db.ForeignKey('lvas.lva_number'), nullable=False)

    lva = db.relationship('Lva', back_populates='exercises')
    assignments = db.relationship('Assignment', back_populates='exercise')
    
class Assignment(db.Model):
    __tablename__ = 'assignments'

    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    exercise_id = db.Column(db.Integer, db.ForeignKey('exercises.id'), nullable=False)
    file_path = db.Column(db.String(255), nullable=False)  # name der datei, nicht der path
    
    student = db.relationship('User', back_populates='assignments')
    exercise = db.relationship('Exercise', back_populates='assignments')
    grade = db.relationship('Grade', uselist=False, back_populates='assignment')

class Grade(db.Model):
    __tablename__ = 'grades'

    id = db.Column(db.Integer, primary_key=True)
    assignment_id = db.Column(db.Integer, db.ForeignKey('assignments.id'), nullable=False, unique=True)
    grade = db.Column(db.Integer, nullable=False) 

    assignment = db.relationship('Assignment', back_populates='grade')


class Registration(db.Model):
    __tablename__ = 'registrations'

    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    lva_id = db.Column(db.Integer, db.ForeignKey('lvas.lva_number'), nullable=False)

    student = db.relationship('User', back_populates='registrations')
    lva = db.relationship('Lva', back_populates='registrations')
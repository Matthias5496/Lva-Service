import os
from flask import Blueprint, render_template, g, redirect, send_from_directory, url_for, request, flash, current_app
from app.models import Lva, User, Exercise, Grade, Assignment, Registration
from app import db
from werkzeug.utils import secure_filename

routes = Blueprint('routes', __name__)
#hallo
@routes.route('/')
def index():
    user = User.query.filter_by(email="student1@example.com").first()
    #user = User.query.filter_by(email="instructor2@example.com").first()
    lvas = Lva.query.all()

    lva_von_leiter = Lva.query.filter_by(instructor_id=user.id).first()#all falls lva leiter mehrere lvas hat
    if lva_von_leiter is not None:
        registrations = Registration.query.filter_by(lva_id=lva_von_leiter.lva_number).all()
    else:
        registrations = []

    if user.role=='student':
        return render_template('student.html', lvas = lvas, user = user)
    else:
        return render_template('lva-leiter.html', registrations=registrations, user = user)
    

@routes.route('/Lva/<int:lva_number>')
def lva(lva_number):
    user = User.query.filter_by(email="student1@example.com").first()
    lva = Lva.query.get_or_404(lva_number)
    is_registered = Registration.query.filter_by(student_id = user.id, lva_id = lva_number).first() is not None
    exercises = Exercise.query.filter_by(lva_id=lva_number).all()
    return render_template('lva.html', lva = lva, is_registered = is_registered, user = user, exercises = exercises)
    

@routes.route('/Lva/<int:lva_number>/register', methods=['POST'])
def register_lva(lva_number):
    user = User.query.filter_by(email="student1@example.com").first()

    # Anmeldung zum Kurs
    registration = Registration(student_id=user.id, lva_id=lva_number)
    db.session.add(registration)
    db.session.commit()
    return redirect(url_for('routes.lva', lva_number=lva_number))


@routes.route('/exercise/<int:exercise_id>')
def exercise(exercise_id):
    user = User.query.filter_by(email="student1@example.com").first()
    exercise = Exercise.query.get_or_404(exercise_id)
    assignment = Assignment.query.filter_by(student_id=user.id, exercise_id=exercise_id).first()
    return render_template('exercise.html', user = user, exercise=exercise, assignment=assignment)



UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'pdf'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@routes.route('/student/<int:student_id>/assignments')
def assignments(student_id):
    user = User.query.filter_by(email="instructor2@example.com").first()

    assignments = Assignment.query.filter_by(student_id=student_id).all()
    student = User.query.filter_by(id=student_id).first()

    return render_template('assignments.html', assignments = assignments, student=student, user = user)

@routes.route('/student/<int:student_id>/assignments/<int:assignment_id>')
def assignment_detail(student_id, assignment_id):
    assignment = Assignment.query.filter_by(id=assignment_id).first()
    student = User.query.filter_by(id=student_id).first()
    return render_template('assignment_detail.html', assignment = assignment, student=student)

@routes.route('/assignments/<int:assignment_id>/download')
def download_assignment(assignment_id):
    assignment = Assignment.query.get_or_404(assignment_id)
    student_id = assignment.student_id
    upload_folder = current_app.config['UPLOAD_FOLDER']
    file_path = assignment.file_path
        
    # Überprüfen, ob die Datei wirklich existiert
    if not os.path.exists(os.path.join(upload_folder, file_path)):
        print(f"Redirecting to assignment_detail with student_id: {student_id} and assignment_id: {assignment_id}")
        flash("File not found.")
        return redirect(url_for('routes.assignment_detail', student_id=student_id, assignment_id=assignment_id))
    
    # Sende die Datei aus dem Upload-Verzeichnis
    return send_from_directory(directory=upload_folder, path=file_path, as_attachment=True)


@routes.route('/assignments/<int:assignment_id>/grade', methods=['POST'])
def grade_assignment(assignment_id):
    assignment = Assignment.query.get_or_404(assignment_id)
    
    # Note aus dem Formular
    grade_value = request.form.get('grade')
    
    # vorhande Bewertung holen
    existing_grade = Grade.query.filter_by(assignment_id=assignment.id).first()
    #wenn es schon eine Bewertung gibt, wird es überschrieben
    if existing_grade:
        existing_grade.grade = grade_value
    #wenn keine gibt wird eine neue Bewertung erstellt
    else:
        # Neue Bewertung erstellen
        grade = Grade(assignment_id=assignment.id, grade=grade_value)
        db.session.add(grade)
    
    db.session.commit()
    
    return redirect(url_for('routes.assignment_detail', student_id=assignment.student_id, assignment_id=assignment.id))


@routes.route('/exercise/<int:exercise_id>/submit', methods=['POST'])
def submit_assignment(exercise_id):
    user = User.query.filter_by(email="student1@example.com").first()  # Replace this with the logged-in user

    if 'file' not in request.files:
        flash('No file part')
        return redirect(request.url)

    file = request.files['file']
    
    if file.filename == '':
        flash('No selected file')
        return redirect(request.url)

    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file_path = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)

        # überprüfen ob der user bereits eine abgabe für diese übung hat
        assignment = Assignment.query.filter_by(student_id=user.id, exercise_id=exercise_id).first()
        #wenn ja wird die abgabe überschrieben
        if assignment:
            if os.path.exists(os.path.join(current_app.config['UPLOAD_FOLDER'], assignment.file_path)):
                os.remove(os.path.join(current_app.config['UPLOAD_FOLDER'], assignment.file_path))
            assignment.file_path = filename
        #wenn nicht wird eine neue Abgabe erstellt
        else:
            assignment = Assignment(student_id=user.id, exercise_id=exercise_id, file_path=filename)  # Only save the filename
            db.session.add(assignment)

        file.save(file_path)
        
        db.session.commit()

        flash('File uploaded successfully!')
        return redirect(url_for('routes.exercise', exercise_id=exercise_id))

    else:
        flash('Invalid file type. Only PDF files are allowed.')
        return redirect(request.url)

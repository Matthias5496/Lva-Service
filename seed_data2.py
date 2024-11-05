from app import app, db
from app.models import User, Lva, Exercise, Registration, Assignment, Grade
from werkzeug.security import generate_password_hash

with app.app_context():
    # Erstelle die Datenbank und die Tabellen (nur einmal ausführen, wenn noch keine Tabellen vorhanden sind)
    db.create_all()

    exercise1 = Exercise(title="Algebra", description="Lösen Sie Aufgabe 103 a) im Buch auf Seite 45", lva_id=1)
    exercise2 = Exercise(title="Matrizen", description="Lösen Sie alle Aufgabe im Buch auf Seite 45-48", lva_id=1)
    exercise3 = Exercise(title="Past tense", description="Lösen Sie Aufgabe 20 c) im Buch auf Seite 18", lva_id=2)
    exercise4 = Exercise(title="Writing an Article", description="Lösen Sie Aufgabe 67 a) im Buch auf Seite 26", lva_id=2)
    db.session.add(exercise1)
    db.session.add(exercise2)
    db.session.add(exercise3)
    db.session.add(exercise4)
    db.session.commit()
    print("Beispiel-Übung erfolgreich hinzugefügt!")
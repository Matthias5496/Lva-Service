from app import app, db
from app.models import User, Lva, Exercise, Registration, Assignment, Grade
from werkzeug.security import generate_password_hash

with app.app_context():
    # Erstelle die Datenbank und die Tabellen (nur einmal ausführen, wenn noch keine Tabellen vorhanden sind)
    db.create_all()

    # Beispiel-User erstellen
    user1 = User(email="student1@example.com", password="password123", firstname="Max", lastname="Mustermann", role="student")
    user2 = User(email="student2@example.com", password="password123", firstname="Anna", lastname="Musterfrau", role="student")
    user3 = User(email="instructor1@example.com", password="password123", firstname="Markus", lastname="Leiter", role="instructor")
    user4 = User(email="instructor2@example.com", password="password123", firstname="Richard", lastname="Reis", role="instructor")
 # User zur Datenbank hinzufügen
    db.session.add(user1)
    db.session.add(user2)
    db.session.add(user3)
    db.session.add(user4)
    db.session.commit()


    # Beispiel-Kurs erstellen
    lva1 = Lva(title="Mathematik 1", description="Einführung in die Mathematik", instructor_id=user3.id)
    lva2 = Lva(title="Englisch", description="Einführung in die englische Sprache", instructor_id=user4.id)
    lva3 = Lva(title="Mathematik 2", description="Forgeschrittene Mathematik", instructor_id=user3.id)
    # Kurs zur Datenbank hinzufügen
    db.session.add(lva1)
    db.session.add(lva2)
    db.session.add(lva3)
    db.session.commit()

    print("Beispiel-User und Kurs erfolgreich hinzugefügt!")

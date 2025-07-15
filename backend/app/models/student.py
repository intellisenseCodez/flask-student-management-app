from datetime import datetime, timezone

from app import db


class Student(db.Model):
    """
    Represents a student's personal and academic information.

    Each student has identifying details such as full name, age, gender, and email.
    The student is linked to courses through the `StudentCourse` association table,
    enabling a many-to-many relationship.

    Attributes:
        id (int): Primary key of the student.
        full_name (str): Full name of the student.
        age (int): Age of the student.
        gender (Enum): Gender of the student; either "Male" or "Female".
        email (str, optional): Email address of the student.
        created_at (datetime): Timestamp of when the student record was created.
        updated_at (datetime): Timestamp of the last update to the student record.

    Relationships:
        courses (list[StudentCourse]): The list of student-course enrollment associations.

    Methods:
        __repr__(): Returns a string representation of the Student object.
    """
    __tablename__ = "students"

    id = db.Column(db.Integer, primary_key=True)
    full_name = db.Column(db.String(100), nullable=False)
    age = db.Column(db.Integer, nullable=False)
    gender = db.Column(db.Enum("Male", "Female", name="gender_types"), nullable=False)
    email = db.Column(db.String(255), nullable=True)

    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    updated_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc),
                                              onupdate=lambda: datetime.now(timezone.utc))
    
    # Relationship to Course through StudentCourse
    courses = db.relationship(
        'StudentCourse',
        back_populates='student',
        cascade='all, delete-orphan',
        lazy="dynamic"
    )

    def __repr__(self) -> str:
        """Provides a friendly string representation of the student."""
        return (
            f"Student(id={self.id!r}, full_name={self.full_name!r}, "
            f"age={self.age!r}, email={self.email!r})")

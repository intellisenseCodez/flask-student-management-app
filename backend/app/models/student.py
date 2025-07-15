from datetime import datetime, timezone

from app import db


class Student(db.Model):
    """
    Represents a student information.
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
        """Provides a friendly representation of the student."""
        return (
            f"Student(id={self.id!r}, name={self.name!r}, "
            f"age={self.age!r}, email={self.email!r})"
        )

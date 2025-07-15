from datetime import datetime, timezone

from app import db
    
class Course(db.Model):
    """
    Represents a course that students can enroll in.
    """
    __tablename__ = "courses"
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), unique=True, nullable=False)
    code = db.Column(db.String(10), unique=True, nullable=False)
    description = db.Column(db.Text, nullable=True)
    
    # Relationship to Student through StudentCourse
    students = db.relationship(
        'StudentCourse',
        back_populates='course',
        cascade='all, delete-orphan',
        lazy="dynamic"
    )
    
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    updated_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc),
                                              onupdate=lambda: datetime.now(timezone.utc))
    

    def __repr__(self) -> str:
        """Provides a developer-friendly representation of the course."""
        return f"Course(id={self.id!r}, title={self.title!r}, code={self.code!r})"
    

class StudentCourse(db.Model):
    __tablename__ = 'student_course'
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('students.id'), nullable=False)
    course_id = db.Column(db.Integer, db.ForeignKey('courses.id'), nullable=False)

    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    updated_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc),
                                              onupdate=lambda: datetime.now(timezone.utc))

    # define relationships for backrefs
    student = db.relationship("Student", back_populates="courses")
    course = db.relationship("Course", back_populates="students")
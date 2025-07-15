from datetime import datetime, timezone

from app import db
    

class Enrollment(db.Model):
    """
    Represents the association between a student and a course in a many-to-many relationship.

    This model serves as a join table that links students and courses, 
    tracking which students are enrolled in which courses. It also includes
    timestamps for when the association was created and last updated.

    Attributes:
        id (int): Primary key for the association.
        student_id (int): Foreign key referencing the student.
        course_id (int): Foreign key referencing the course.
        created_at (datetime): Timestamp of when the record was created.
        updated_at (datetime): Timestamp of the last update to the record.

    Relationships:
        student (Student): The student associated with this record.
        course (Course): The course associated with this record.
    """
    __tablename__ = 'enrollments'
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('students.id'), nullable=False)
    course_id = db.Column(db.Integer, db.ForeignKey('courses.id'), nullable=False)

    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    updated_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc),
                                              onupdate=lambda: datetime.now(timezone.utc))

    # define relationships for backrefs
    student = db.relationship("Student", back_populates="courses")
    course = db.relationship("Course", back_populates="students")

    def __repr__(self) -> str:
        """Provides a friendly representation of the course."""
        return f"Enrollment(studentID={self.student_id!r}, courseID={self.course_id!r})"
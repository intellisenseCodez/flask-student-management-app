from datetime import datetime, timezone

from app import db
    
class Course(db.Model):
    """
    Represents a course that students can enroll in.

    Each course has a unique title and code, along with an optional description.
    This model maintains a relationship with students through the `StudentCourse`
    association table, enabling a many-to-many relationship.

    Attributes:
        id (int): Primary key of the course.
        title (str): Unique title of the course (e.g., "Introduction to Biology").
        code (str): Unique course code (e.g., "BIO101").
        description (str, optional): A brief description of the course content.
        created_at (datetime): Timestamp when the course was created.
        updated_at (datetime): Timestamp of the last update to the course.

    Relationships:
        students (list[StudentCourse]): The list of student-course enrollment associations.

    Methods:
        __repr__(): Returns a string representation of the Course object.
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
        """Provides a friendly representation of the course."""
        return f"Course(id={self.id!r}, title={self.title!r}, code={self.code!r})"
    
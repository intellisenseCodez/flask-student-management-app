from flask import jsonify, request
from werkzeug.exceptions import BadRequest, Conflict, NotFound

from app import app, db
from app.models import Student, Course, StudentCourse

@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"


@app.route("/api/v1.0/student/create", methods=['POST'])
def create_user():
    """Create new student"""
    try:
        # check if the request is in JSON
        if not request.is_json:
            raise BadRequest("Request must be JSON")
        
        # collect all user request
        data = request.get_json()

        # Validate all required fields
        required_fields = ['full_name', 'age', 'gender']
        if not all(field in data for field in required_fields):
            raise BadRequest(f"Missing required fields. Required: {required_fields}")
        
        # Check if email already exists
        if Student.query.filter_by(email=data['email']).first():
            raise Conflict("Email address already in use")
        
        # Validate gender 
        if data['gender'].title() not in ["Male", "Female"]:
            raise BadRequest("Gender must be Male or Female")
    
        # serialization
        new_student = Student(full_name = data["full_name"].title().strip(),
                        age = data["age"],
                        email = data["email"].title().strip(),
                        gender = data["gender"].title().strip())
        
    
        # store in database
        db.session.add(new_student)
        db.session.commit()

        response = {
            "id": new_student.id,
            "full_name": new_student.full_name,
            "age": new_student.age,
            "email": new_student.email,
            "gender": new_student.gender,
            "created_at": new_student.created_at.isoformat(),
            "updated_at": new_student.updated_at.isoformat(),
        }

        return jsonify(response), 201

    except BadRequest as e:
        return jsonify({"error": str(e)}), 400
    except Conflict as e:
        return jsonify({"error": str(e)}), 409
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": "Internal server error"}), 500
    

@app.route("/api/v1.0/students/all", methods=['GET'])
def get_all_students():
    """
    Get all students
    """
    try:
        students = Student.query.all()

    
        response = [{
            "id": student.id,
            "full_name": student.full_name,
            "age": student.age,
            "email": student.email,
            "gender": student.gender,
            "created_at": student.created_at,
            "updated_at": student.updated_at
        } for student in students]
        
        return jsonify(response), 200
    
    except Exception as e:
        app.logger.error(f"Error fetching students: {str(e)}")
        return jsonify({"error": "Internal server error"}), 500
    
@app.route("/api/v1.0/students/<int:student_id>", methods=['PUT'])
def update_student(student_id):
    """
    Update a student
    """
    try:
        if not request.is_json:
            raise BadRequest("Request must be JSON")
        
        student = Student.query.get_or_404(student_id)
        data = request.get_json()
        
        # Check for email conflict
        if 'email' in data and data['email'] != student.email:
            if Student.query.filter_by(email=data['email']).first():
                raise Conflict("Email already in use")
        
        # Update fields if provided
        if 'full_name' in data:
            student.full_name = data['full_name']
        if 'age' in data:
            student.age = data['age']
        if 'email' in data:
            student.email = data['email']
        if 'gender' in data:
            student.gender = data['gender']
        
        db.session.commit()
        
        return jsonify({
            "message": "Student updated successfully",
            "student": {
                "id": student.id,
                "full_name": student.full_name,
                "email": student.email
            }
        }), 200
    
    except BadRequest as e:
        return jsonify({"error": str(e)}), 400
    except NotFound:
        return jsonify({"error": "Student not found"}), 404
    except Conflict as e:
        return jsonify({"error": str(e)}), 409
    except Exception as e:
        db.session.rollback()
        app.logger.error(f"Error updating student: {str(e)}")
        return jsonify({"error": "Internal server error"}), 500
    

@app.route("/api/v1.0/students/<int:student_id>", methods=['DELETE'])
def delete_student(student_id):
    """
    Delete a student and their courses (cascade)
    """
    try:
        student = Student.query.get_or_404(student_id)
        
        db.session.delete(student)
        db.session.commit()
        
        return jsonify({
            "message": "Student and associated courses deleted successfully",
            "student_id": student_id
        }), 200
    
    except NotFound:
        return jsonify({"error": "Student not found"}), 404
    except Exception as e:
        db.session.rollback()
        app.logger.error(f"Error deleting student: {str(e)}")
        return jsonify({"error": "Internal server error"}), 500

@app.route("/api/v1.0/students/<int:student_id>", methods=['GET'])
def get_student_by_id(student_id):
    """
    Get a specific student by ID
    """
    try:
        student = Student.query.get_or_404(student_id)
        
        response = {
            "id": student.id,
            "full_name": student.full_name,
            "age": student.age,
            "email": student.email,
            "gender": student.gender,
            "courses": [{
                "id": course.id,
                "title": course.title,
                "created_at": course.created_at.isoformat()
            } for course in student.courses],
            "created_at": student.created_at,
            "updated_at": student.updated_at
        }
        
        return jsonify(response), 200
    
    except NotFound:
        return jsonify({"error": "Student not found"}), 404
    except Exception as e:
        app.logger.error(f"Error fetching student: {str(e)}")
        return jsonify({"error": "Internal server error"}), 500
    

@app.route("/api/v1.0/students/by-course", methods=['GET'])
def get_students_by_course():
    """
    Find students taking specific courses
    """
    try:
        if 'course_titles' not in request.args:
            raise BadRequest("course_title parameter is required")
        
        course_titles = [title.strip() for title in request.args['course_titles'].split(',')]

        # Check if courses exists
        for course_title in course_titles:
            course = Course.query.filter_by(title=course_title).first()
            if not course:
                raise NotFound("Course not found")
        
        # join Student and StudentCourse to filter out where records matches selected course title
        students = Student.query.join(StudentCourse).filter(
            Course.title.in_(course_titles)
        ).distinct().all()
        
        response = [{
            "id": student.id,
            "full_name": student.full_name,
            "email": student.email,
            "matching_courses": [course.title for course in student.courses 
                               if course.title in course_titles]
        } for student in students]

        if len(response) < 1:
            response = f"No Students Matches to {course_titles}"
        
        return jsonify(response), 200
    
    except BadRequest as e:
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        app.logger.error(f"Error fetching students by course: {str(e)}")
        return jsonify({"error": "Internal server error"}), 500


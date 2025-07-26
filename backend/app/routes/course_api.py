from flask import jsonify, request
from werkzeug.exceptions import BadRequest, Conflict, NotFound

from app import app, db
from app.models.student import Student
from app.models.course import Course
from app.models.enrollment import Enrollment



@app.route("/api/v1.0/course/create", methods=['POST'])
def create_course():
    """Create new course"""
    try:
        # check if the request is in JSON
        if not request.is_json:
            raise BadRequest("Request must be JSON")
        
        # collect all user request
        data = request.get_json()

        # Validate all required fields
        required_fields = ['title', 'code']
        if not all(field in data for field in required_fields):
            raise BadRequest(f"Missing required fields. Required: {required_fields}")
        

        # Check if course already exists
        if Course.query.filter_by(title=data['title']).first():
            raise Conflict("Course already exits")
        
        # Check if course code already exists 
        if Course.query.filter_by(code=data['code']).first():
            raise Conflict("Course Code already taken")
    

        # serialization
        new_course = Course(title = data["title"].title().strip(),
                            code = data["code"].upper().strip())
    

        if data["description"]:
            new_course.description = data["description"]
        
    
        # store in database
        db.session.add(new_course)
        db.session.commit()

        response = {
            "id": new_course.id,
            "title": new_course.title,
            "code": new_course.code,
            "description": new_course.description,
            "created_at": new_course.created_at.isoformat(),
            "updated_at": new_course.updated_at.isoformat(),
        }

        return jsonify(response), 201

    except BadRequest as e:
        return jsonify({"error": str(e)}), 400
    except Conflict as e:
        return jsonify({"error": str(e)}), 409
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": "Internal server error"}), 500
    
@app.route("/api/v1.0/courses/all", methods=['GET'])
def get_all_courses():
    """
    Get all courses
    """
    try:
        courses = Course.query.all()

        response = [{
            "id": course.id,
            "title": course.title,
            "code": course.code,
            "description": course.description,
            "created_at": course.created_at,
            "updated_at": course.updated_at
        } for course in courses]
        
        return jsonify(response), 200
    
    except Exception as e:
        app.logger.error(f"Error fetching students: {str(e)}")
        return jsonify({"error": "Internal server error"}), 500
    

@app.route("/api/v1.0/courses/<int:course_id>", methods=['PUT'])
def update_course(course_id):
    """
    Update a course
    """
    try:
        if not request.is_json:
            raise BadRequest("Request must be JSON")
        
        course = Course.query.get_or_404(course_id)
        data = request.get_json()

        print(data["title"])

        if Course.query.filter_by(title=data["title"]).first():
            raise Conflict("Course already exits")
        
        if Course.query.filter_by(code=data["code"]).first():
            raise Conflict("Course Code already taken")
        
        if 'title' in data:
            course.title = data['title'].strip().title()
        if 'code' in data:
            course.code = data['code'].strip().title()
        if 'description' in data:
            course.description = data['description'].strip()
        
        db.session.commit()
        
        return jsonify({
            "message": "Course updated successfully",
            "course": {
                "id": course.id,
                "title": course.title,
                "code": course.code,
                "description": course.description
            }
        }), 200
    
    except BadRequest as e:
        return jsonify({"error": str(e)}), 400
    except NotFound:
        return jsonify({"error": "Course not found"}), 404
    except Exception as e:
        db.session.rollback()
        app.logger.error(f"Error updating course: {str(e)}")
        return jsonify({"error": "Internal server error"}), 500

@app.route("/api/v1.0/courses/<int:course_id>", methods=['DELETE'])
def delete_course(course_id):
    """
    Delete a course
    """
    try:
        course = Course.query.get_or_404(course_id)
        
        db.session.delete(course)
        db.session.commit()
        
        return jsonify({
            "message": "Course deleted successfully",
            "course_id": course_id
        }), 200
    
    except NotFound:
        return jsonify({"error": "Course not found"}), 404
    except Exception as e:
        db.session.rollback()
        app.logger.error(f"Error deleting course: {str(e)}")
        return jsonify({"error": "Internal server error"}), 500

@app.route("/api/v1.0/courses/<int:course_id>", methods=['GET'])
def get_course_by_id(course_id):
    """
    Get a specific course by ID
    """
    try:
        course = Course.query.get_or_404(course_id)
        
        response = {
            "id": course.id,
            "title": course.title,
            "code": course.code,
            "description": course.description,
            "created_at": course.created_at,
            "updated_at": course.updated_at

        }
        
        return jsonify(response), 200
    
    except NotFound:
        return jsonify({"error": "Course not found"}), 404
    except Exception as e:
        app.logger.error(f"Error fetching course: {str(e)}")
        return jsonify({"error": "Internal server error"}), 500



@app.route("/api/v1.0/course/add/<int:user_id>", methods=['POST'])
def add_course_to_student(user_id:int):
    """Add courses to existing student"""
    try:
        if not request.is_json:
            raise BadRequest("Request must be JSON")
        
        data = request.get_json()
        
        # Validate required fields
        required_fields = ['title']
        if not all(field in data for field in required_fields):
            raise BadRequest(f"Missing required fields. Required: {required_fields}")
        
        # Check if course exists
        course = Course.query.filter_by(title=data["title"]).first()
        if not course:
            raise NotFound("Course not found")
        
        # Check if student exists
        student = Student.query.filter_by(id=user_id).first()
        if not student:
            raise NotFound("Student not found")
        
        # Check if the student is already enrolled in this course
        existing_enrollment = Enrollment.query.filter_by(
            student_id=user_id,
            course_id=course.id
        ).first()

        if existing_enrollment:
            raise Conflict("Student is already enrolled in this course.")

        # Enroll student in the course
        enrollment = Enrollment(student_id=user_id, course_id=course.id)
        db.session.add(enrollment)
        db.session.commit()

        return jsonify({
            "id": enrollment.id,
            "student_id": enrollment.student_id,
            "course_id": enrollment.course_id,
            "created_at": enrollment.created_at.isoformat(),
            "updated_at": enrollment.updated_at.isoformat()
        }), 201

    except (BadRequest, NotFound, Conflict) as e:
        return jsonify({"error": str(e)}), e.code
    except Exception as e:
        db.session.rollback()
        app.logger.error(f"Error adding course to student: {e}")
        return jsonify({"error": "Internal server error"}), 500


@app.route("/api/v1.0/students/<int:student_id>/courses", methods=['GET'])
def get_student_courses(student_id):
    """
    Get all courses for a specific student
    """
    try:
        student = Student.query.get_or_404(student_id)

        # Fetch all associated courses via Enrollment
        student_courses = Enrollment.query.filter_by(student_id=student.id).all()

        if not student_courses:
            return jsonify({"message": "Student is not enrolled in any courses."}), 200

        
        response = []
        for sc in student_courses:
            course = sc.course
            response.append({
                "id": course.id,
                "title": course.title,
                "code": course.code,
                "description": course.description,
                "created_at": course.created_at.isoformat() if course.created_at else None,
                "updated_at": course.updated_at.isoformat() if course.updated_at else None
            })

        return jsonify(response), 200

    except NotFound:
        return jsonify({"error": "Student not found"}), 404
    except Exception as e:
        app.logger.error(f"Error fetching student courses: {str(e)}")
        return jsonify({"error": "Internal server error"}), 500
from abc import ABC, abstractmethod

# Custom Exceptions
class CourseFullException(Exception):
    pass

class StudentNotFoundException(Exception):
    pass

class TeacherNotFoundException(Exception):
    pass

class CourseNotFoundException(Exception):
    pass

class MemberNotFoundException(Exception):
    pass

# Abstract Base Class
class SchoolMember(ABC):
    def __init__(self, name, member_id):
        self._name = name
        self._id = member_id
    
    @abstractmethod
    def display_details(self):
        pass
    
    @property
    def name(self):
        return self._name
    
    @name.setter
    def name(self, value):
        self._name = value
    
    @property
    def id(self):
        return self._id

# Student Class
class Student(SchoolMember):
    def __init__(self, name, student_id):
        super().__init__(name, student_id)
        self._courses = []
        self._grades = {}
        self._attendance = {}
        self._gpa = 0.0  # Initialize GPA to 0.0
    
    def enroll_in_course(self, course):
        if course not in self._courses:
            self._courses.append(course)
            course.add_student(self)
            self._update_gpa()
        else:
            print(f"Student {self._name} is already enrolled in {course.course_name}")

    def drop_course(self, course):
        if course in self._courses:
            self._courses.remove(course)
            course.remove_student(self)
            self._update_gpa()
        else:
            print(f"Student {self._name} is not enrolled in {course.course_name}")
    
    def view_grades(self):
        for course, grade in self._grades.items():
            print(f"Course: {course.course_name}, Grade: {grade}")
    
    def receive_grade(self, course, grade):
        self._grades[course] = grade
        self._update_gpa()

    def mark_attendance(self, course, date, present):
        if course not in self._attendance:
            self._attendance[course] = []
        self._attendance[course].append((date, present))

    def view_attendance(self):
        for course, attendance in self._attendance.items():
            print(f"Attendance for {course.course_name}:")
            for date, present in attendance:
                status = "Present" if present else "Absent"
                print(f"- {date}: {status}")

    def _update_gpa(self):
        total_credits = 0
        total_grade_points = 0

        for course, grade in self._grades.items():
            if grade == 'A':
                grade_point = 4.0
            elif grade == 'B':
                grade_point = 3.0
            elif grade == 'C':
                grade_point = 2.0
            elif grade == 'D':
                grade_point = 1.0
            else:
                grade_point = 0.0  # F or other grades

            # Assuming all courses have equal weight (1 credit each)
            total_credits += 1
            total_grade_points += grade_point

        if total_credits > 0:
            self._gpa = total_grade_points / total_credits
        else:
            self._gpa = 0.0  # No grades available

    def calculate_cgpa(self):
        # CGPA calculation can be similar to GPA if all courses have equal weight
        return self._gpa

    def display_details(self):
        print(f"Student Name: {self._name}, ID: {self._id}, Courses: {[course.course_name for course in self._courses]}, GPA: {self._gpa:.2f}")
    
    @property
    def courses(self):
        return self._courses
    
    @property
    def grades(self):
        return self._grades

# Teacher Class
class Teacher(SchoolMember):
    def __init__(self, name, teacher_id):
        super().__init__(name, teacher_id)
        self._courses = []
        self._schedule = {}
    
    def assign_grade(self, student, course, grade):
        if course in self._courses:
            student.receive_grade(course, grade)
        else:
            print(f"Teacher {self._name} does not teach {course.course_name}")
    
    def teach_course(self, course):
        if course not in self._courses:
            self._courses.append(course)
            course.assign_teacher(self)
        else:
            print(f"Teacher {self._name} is already teaching {course.course_name}")

    def set_schedule(self, course, time_slot):
        if course in self._courses:
            self._schedule[course] = time_slot
        else:
            print(f"Teacher {self._name} does not teach {course.course_name}")

    def view_schedule(self):
        print(f"Schedule for Teacher {self._name}:")
        for course, time_slot in self._schedule.items():
            print(f"- {course.course_name}: {time_slot}")

    def display_details(self):
        print(f"Teacher Name: {self._name}, ID: {self._id}, Courses: {[course.course_name for course in self._courses]}")
    
    @property
    def courses(self):
        return self._courses

# Course Class
class Course:
    def __init__(self, course_name, course_id, max_students=30):
        self._course_name = course_name
        self._course_id = course_id
        self._teacher = None
        self._students = []
        self._grades = {}
        self._max_students = max_students
    
    def add_student(self, student):
        if len(self._students) < self._max_students:
            self._students.append(student)
        else:
            raise CourseFullException(f"Course {self._course_name} is full")

    def remove_student(self, student):
        if student in self._students:
            self._students.remove(student)
        else:
            raise StudentNotFoundException(f"Student not found in course {self._course_name}")
    
    def assign_teacher(self, teacher):
        self._teacher = teacher

    def display_students(self):
        print(f"Students enrolled in {self._course_name}:")
        for student in self._students:
            print(f"- {student.name} (ID: {student.id})")
    
    def display_details(self):
        print(f"Course Name: {self._course_name}, ID: {self._course_id}, Teacher: {self._teacher.name if self._teacher else 'None'}, Students: {[student.name for student in self._students]}")
    
    @property
    def course_name(self):
        return self._course_name
    
    @property
    def course_id(self):
        return self._course_id
    
    @property
    def teacher(self):
        return self._teacher
    
    @property
    def students(self):
        return self._students
    
    @property
    def grades(self):
        return self._grades

# School Class to manage all students, teachers, and courses
class School:
    def __init__(self):
        self._students = []
        self._teachers = []
        self._courses = []
    
    def add_student(self, student):
        self._students.append(student)
    
    def add_teacher(self, teacher):
        self._teachers.append(teacher)
    
    def add_course(self, course):
        self._courses.append(course)
    
    def remove_student(self, student_id):
        student = self.find_student_by_id(student_id)
        if student:
            self._students.remove(student)
        else:
            raise StudentNotFoundException(f"Student with ID {student_id} not found")
    
    def remove_teacher(self, teacher_id):
        teacher = self.find_teacher_by_id(teacher_id)
        if teacher:
            self._teachers.remove(teacher)
        else:
            raise TeacherNotFoundException(f"Teacher with ID {teacher_id} not found")
    
    def remove_course(self, course_id):
        course = self.find_course_by_id(course_id)
        if course:
            self._courses.remove(course)
        else:
            raise CourseNotFoundException(f"Course with ID {course_id} not found")
    
    def find_student_by_id(self, student_id):
        for student in self._students:
            if student.id == student_id:
                return student
        raise StudentNotFoundException(f"Student with ID {student_id} not found")
    
    def find_teacher_by_id(self, teacher_id):
        for teacher in self._teachers:
            if teacher.id == teacher_id:
                return teacher
        raise TeacherNotFoundException(f"Teacher with ID {teacher_id} not found")
    
    def find_course_by_id(self, course_id):
        for course in self._courses:
            if course.course_id == course_id:
                return course
        raise CourseNotFoundException(f"Course with ID {course_id} not found")
    
    def find_student_by_name(self, name):
        results = []
        for student in self._students:
            if student.name.lower() == name.lower():
                results.append(student)
        if results:
            return results
        raise StudentNotFoundException(f"No students found with the name '{name}'")
    
    def display_all_students(self):
        print("All Students in School:")
        for student in self._students:
            print(f"- {student.name} (ID: {student.id})")
    
    def display_all_teachers(self):
        print("All Teachers in School:")
        for teacher in self._teachers:
            print(f"- {teacher.name} (ID: {teacher.id})")
    
    def display_all_courses(self):
        print("All Courses in School:")
        for course in self._courses:
            print(f"- {course.course_name} (ID: {course.course_id})")
    
    def display_student_details_by_id(self, student_id):
        student = self.find_student_by_id(student_id)
        student.display_details()
    
    def display_student_details_by_name(self, name):
        students = self.find_student_by_name(name)
        for student in students:
            student.display_details()

    def display_teacher_schedule(self, teacher_id):
        teacher = self.find_teacher_by_id(teacher_id)
        teacher.view_schedule()

    @property
    def students(self):
        return self._students
    
    @property
    def teachers(self):
        return self._teachers
    
    @property
    def courses(self):
        return self._courses

# Testing the System
try:
    # Create School
    school = School()

    # Create Courses
    math_course = Course("Mathematics", "MATH101")
    science_course = Course("Science", "SCI101")
    
    # Create Students
    student1 = Student("Alice", "S001")
    student2 = Student("Bob", "S002")
    
    # Create Teacher
    teacher1 = Teacher("Dr. Smith", "T001")
    
    # Add Students, Teachers, and Courses to School
    school.add_student(student1)
    school.add_student(student2)
    school.add_teacher(teacher1)
    school.add_course(math_course)
    school.add_course(science_course)
    
    # Enroll Students in Courses
    student1.enroll_in_course(math_course)
    student1.enroll_in_course(science_course)
    student2.enroll_in_course(math_course)
    
    # Assign Teacher to Course
    teacher1.teach_course(math_course)
    
    # Assign Grades
    teacher1.assign_grade(student1, math_course, 'A')
    teacher1.assign_grade(student2, math_course, 'B')
    
    # Mark Attendance
    student1.mark_attendance(math_course, "2024-07-01", True)
    student1.mark_attendance(math_course, "2024-07-02", False)
    student2.mark_attendance(math_course, "2024-07-01", True)
    
    # Set Teacher's Schedule
    teacher1.set_schedule(math_course, "Monday 10-12")
    
    # Display Details
    student1.display_details()
    student2.display_details()
    teacher1.display_details()
    
    student1.view_grades()
    student1.view_attendance()

    # Display all Students, Teachers, and Courses in School
    school.display_all_students()
    school.display_all_teachers()
    school.display_all_courses()

    # Display Students enrolled in specific Course
    math_course.display_students()
    
    # Search for student by ID
    school.display_student_details_by_id("S001")

    # Search for student by name
    school.display_student_details_by_name("Bob")

    # Display teacher's schedule
    school.display_teacher_schedule("T001")

    # Calculate CGPA for students
    print(f"\nCGPA for {student1.name}: {student1.calculate_cgpa()}")
    print(f"CGPA for {student2.name}: {student2.calculate_cgpa()}")

except Exception as e:
    print(e)

import csv
from canvasapi import Canvas
# from canvasapi.exceptions import CanvasAPIError
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()
API_TOKEN = os.getenv("CANVAS_API_TOKEN")
API_URL = "https://canvas.ucsc.edu"
COURSE_ID = 78919
SECTION_ID = 186973
ASSIGNMENTS_IDS = [674202, 675093]  # Replace with your assignment IDs

# Initialize the Canvas object
canvas = Canvas(API_URL, API_TOKEN)

# Fetch all students in the section
def get_all_students_from_section():
    try:
        course = canvas.get_course(COURSE_ID)
        section = course.get_section(SECTION_ID, include=["students"])
        students = section.students

        if isinstance(students, list) and all(isinstance(student, dict) for student in students):
            student_details = [
                {"id": student.get("id"), "name": student.get("name"), "email": student.get("login_id")}
                for student in students
            ]
            return student_details
        else:
            print("Unexpected data format for students:", students)
            return []
    # except CanvasAPIError as e:
    #     print(f"API error occurred: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

# Batch assignment of students to an assignment
def batch_assign_to_students(assignments_map):
    try:
        course = canvas.get_course(COURSE_ID)

        for assignment_id, student_ids in assignments_map.items():
            assignment = course.get_assignment(assignment_id)
            # Create an assignment override for the batch
            override = assignment.create_override(
                assignment_override={
                    "student_ids": student_ids,
                    "title": f"Batch Override for Assignment {assignment_id}",
                }
            )
            print(f"Override created for Assignment {assignment_id}: {override}")
    # except CanvasAPIError as e:
    #     print(f"API error occurred: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

# Create CSV file with the assignment distribution
def generate_csv(students, assignments):
    try:
        with open("assignment_distribution.csv", "w", newline="") as csvfile:
            fieldnames = ["Student Name", "Email", "Canvas ID", "Assignment ID"]
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

            writer.writeheader()
            for student, assignment_id in zip(students, assignments):
                writer.writerow({
                    "Student Name": student["name"],
                    "Email": student["email"],
                    "Canvas ID": student["id"],
                    "Assignment ID": assignment_id,
                })

        print("CSV file 'assignment_distribution.csv' created successfully.")
    except Exception as e:
        print(f"Error creating CSV file: {e}")

# Main logic to distribute assignments evenly and in batch
def assign_assignments_in_batch():
    students = get_all_students_from_section()

    if students:
        student_ids = [student["id"] for student in students]
        num_students = len(student_ids)
        num_assignments = len(ASSIGNMENTS_IDS)

        # Create a mapping of assignment_id -> student_ids
        assignments_map = {assignment_id: [] for assignment_id in ASSIGNMENTS_IDS}

        for i, student_id in enumerate(student_ids):
            assignment_index = i % num_assignments
            assignments_map[ASSIGNMENTS_IDS[assignment_index]].append(student_id)

        # Batch assign students to assignments
        batch_assign_to_students(assignments_map)

        # Generate the CSV for the distribution
        assignments = [ASSIGNMENTS_IDS[i % num_assignments] for i in range(num_students)]
        generate_csv(students, assignments)

# Run the script
assign_assignments_in_batch()

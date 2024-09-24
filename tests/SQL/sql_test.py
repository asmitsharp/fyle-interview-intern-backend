import random
from sqlalchemy import text

from core import db
from core.models.assignments import Assignment, AssignmentStateEnum, GradeEnum


def create_n_graded_assignments_for_teacher(number: int = 0, teacher_id: int = 1, grade: str = GradeEnum.A) -> int:
    """
    Creates 'n' graded assignments for a specified teacher and returns the count of assignments with the specified grade.

    Parameters:
    - number (int): The number of assignments to be created.
    - teacher_id (int): The ID of the teacher for whom the assignments are created.
    - grade (str): The grade to be assigned to the created assignments.

    Returns:
    - int: Count of assignments with the specified grade.
    """
    # Count the existing assignments with the specified grade for the specified teacher
    grade_counter: int = Assignment.filter(
        Assignment.teacher_id == teacher_id,
        Assignment.grade == grade
    ).count()

    # Create 'n' graded assignments
    for _ in range(number):
        # Create a new Assignment instance with the specified grade
        assignment = Assignment(
            teacher_id=teacher_id,
            student_id=1,
            grade=grade,
            content='test content',
            state=AssignmentStateEnum.GRADED
        )

        # Add the assignment to the database session
        db.session.add(assignment)

        # Update the grade_counter
        grade_counter = grade_counter + 1

    # Commit changes to the database
    db.session.commit()

    # Return the count of assignments with the specified grade
    return grade_counter


def test_get_assignments_in_graded_state_for_each_student():
    """Test to get graded assignments for each student"""

    # Find all the assignments for student 1 and change its state to 'GRADED'
    submitted_assignments: Assignment = Assignment.filter(Assignment.student_id == 1)

    # Iterate over each assignment and update its state
    for assignment in submitted_assignments:
        assignment.state = AssignmentStateEnum.GRADED  # Or any other desired state

    # Flush the changes to the database session
    db.session.flush()
    # Commit the changes to the database
    db.session.commit()

    # Define the expected result before any changes
    expected_result = [(2, 1)] ## update the expected result according to the data

    # Execute the SQL query and compare the result with the expected result
    with open('tests/SQL/number_of_graded_assignments_for_each_student.sql', encoding='utf8') as fo:
        sql = fo.read()

    # Execute the SQL query compare the result with the expected result
    sql_result = db.session.execute(text(sql)).fetchall()
    print(sql_result)
    sql_result.sort()
    expected_result.sort()
    assert len(sql_result) == len(expected_result)
    for itr, result in enumerate(sql_result):
        assert result[0] == expected_result[itr][0]
        assert result[1] == expected_result[itr][1]


def test_get_grade_A_assignments_for_teacher_with_max_grading():
    """Test to get count of grade A assignments for teacher which has graded maximum assignments"""

    # Read the SQL query from a file
    with open('tests/SQL/count_grade_A_assignments_by_teacher_with_max_grading.sql', encoding='utf8') as fo:
        sql = fo.read()

    # Create and grade 5 assignments for the default teacher (teacher_id=1)
    grade_a_count_1 = create_n_graded_assignments_for_teacher(5, grade='A')

    # Execute the SQL query and check if the count matches the created assignments
    sql_result = db.session.execute(text(sql)).fetchall()
    assert len(sql_result) > 0
    assert grade_a_count_1 == sql_result[0][1]

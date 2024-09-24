from unittest.mock import patch
from core.models.assignments import AssignmentStateEnum, GradeEnum


def test_get_assignments(client, h_principal):
    response = client.get(
        '/principal/assignments',
        headers=h_principal
    )

    assert response.status_code == 200

    data = response.json['data']
    for assignment in data:
        assert assignment['state'] in [AssignmentStateEnum.SUBMITTED, AssignmentStateEnum.GRADED]


def test_grade_assignment_draft_assignment(client, h_principal):
    """
    failure case: If an assignment is in Draft state, it cannot be graded by principal
    """
    response = client.post(
        '/principal/assignments/grade',
        json={
            'id': 5,
            'grade': GradeEnum.A.value
        },
        headers=h_principal
    )

    assert response.status_code == 400


def test_grade_assignment(client, h_principal):
    response = client.post(
        '/principal/assignments/grade',
        json={
            'id': 4,
            'grade': GradeEnum.C.value
        },
        headers=h_principal
    )
    print(response)
    assert response.status_code == 200

    assert response.json['data']['state'] == AssignmentStateEnum.GRADED.value
    assert response.json['data']['grade'] == GradeEnum.C


def test_regrade_assignment(client, h_principal):
    response = client.post(
        '/principal/assignments/grade',
        json={
            'id': 4,
            'grade': GradeEnum.B.value
        },
        headers=h_principal
    )

    assert response.status_code == 200

    assert response.json['data']['state'] == AssignmentStateEnum.GRADED.value
    assert response.json['data']['grade'] == GradeEnum.B


def test_grade_assignment_invalid_grade(client, h_principal):
    """
    Test case: Grading an assignment with an invalid grade
    """
    response = client.post(
        '/principal/assignments/grade',
        json={
            'id': 4,
            'grade': 'invalid_grade'
        },
        headers=h_principal
    )

    assert response.status_code == 400
    assert 'grade' in response.json['message']

def test_grade_assignment_unauthenticated(client):
    """
    Test case: Grading an assignment when the principal is not authenticated
    """
    response = client.post(
        '/principal/assignments/grade',
        json={
            'id': 4,
            'grade': GradeEnum.A.value
        }
    )

    assert response.status_code == 401

def test_grade_assignment_missing_id(client, h_principal):
    # Missing ID
    response = client.post(
        '/principal/assignments/grade',
        json={
            'grade': GradeEnum.A.value
        },
        headers=h_principal
    )

    assert response.status_code == 400

def test_grade_assignment_missing_grade(client, h_principal):
        ##Missing Grade
        response = client.post(
        '/principal/assignments/grade',
        json={
            'id': 4
        },
        headers=h_principal
    )

        assert response.status_code == 400

def test_grade_assignment_edge_case_grades(client, h_principal):
    # Test with the lowest boundary grade
    response = client.post(
        '/principal/assignments/grade',
        json={
            'id': 4,
            'grade': GradeEnum.D.value 
        },
        headers=h_principal
    )

    assert response.status_code == 200
    assert response.json['data']['grade'] == GradeEnum.D

    # Test with the highest boundary grade
    response = client.post(
        '/principal/assignments/grade',
        json={
            'id': 4,
            'grade': GradeEnum.A.value  # Assuming A is the highest grade
        },
        headers=h_principal
    )

    assert response.status_code == 200
    assert response.json['data']['grade'] == GradeEnum.A

def test_grade_assignment_multiple_grades(client, h_principal):
    ## Test case: Grading multiple assignments in a single request.
    response = client.post(
        '/principal/assignments/grade',
        json=[
            {'id': 1, 'grade': GradeEnum.A.value},
            {'id': 2, 'grade': GradeEnum.B.value}
        ],
        headers=h_principal
    )

    assert response.status_code == 200
    assert response.json['data'][0]['grade'] == GradeEnum.A
    assert response.json['data'][1]['grade'] == GradeEnum.B

def test_grade_assignment_unauthorized_role(client, h_teacher_1):
    ## Test case: Attempting to grade an assignment when the user is not a principal.

    response = client.post(
        '/principal/assignments/grade',
        json={
            'id': 4,
            'grade': GradeEnum.A.value
        },
        headers=h_teacher_1  # Assuming h_teacher is a header for a teacher
    )

    assert response.status_code == 403

def test_grade_assignment_with_empty_request(client, h_principal):
    ## Test case: Sending an empty request body to the grading endpoint.

    response = client.post(
        '/principal/assignments/grade',
        json={},
        headers=h_principal
    )

    assert response.status_code == 400

def test_list_teachers(client, h_principal):
    ## Test case: Retrieve the list of all teachers as a principal.

    response = client.get(
        '/principal/teachers',
        headers=h_principal
    )

    assert response.status_code == 200 

def test_list_teachers_unauthenticated(client):
    ## Test case: Attempting to retrieve the list of teachers when the principal is not authenticated.

    response = client.get(
        '/principal/teachers'
    )

    assert response.status_code == 401

def test_list_teachers_forbidden_role(client, h_teacher_1):
    ## Test case: Attempting to retrieve the list of teachers with a non-principal role.

    response = client.get(
        '/principal/teachers',
        headers=h_teacher_1
    )

    assert response.status_code == 403


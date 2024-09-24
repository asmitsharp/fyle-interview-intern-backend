from flask import Blueprint
from core import db
from core.apis import decorators
from core.apis.responses import APIResponse
from core.models.teachers import Teacher

from .schema import TeacherSchema
principal_teachers_resources = Blueprint('principal_teachers_resources', __name__)

@principal_teachers_resources.route('/teachers', methods=['GET'], strict_slashes=False)
@decorators.authenticate_principal
def list_teachers(p):
    """Return list of all Teachers."""
    principal_teachers = Teacher.get_teachers()
    teacher_dump = TeacherSchema().dump(principal_teachers, many=True)
    return APIResponse.respond(data=teacher_dump)
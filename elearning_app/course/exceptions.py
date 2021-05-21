from rest_framework.exceptions import APIException


class AlreadyEnrolledAsTeacherException(APIException):
    status_code = 400
    default_detail = 'You have already enrolled for this course as a teacher'
    default_code = 'already_enrolled'


class AlreadyEnrolledAsStudentException(APIException):
    status_code = 400
    default_detail = 'You have already enrolled for this course as a student'
    default_code = 'already_enrolled'

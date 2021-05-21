from .models import Participation, CourseSession
from .exceptions import AlreadyEnrolledAsStudentException, AlreadyEnrolledAsTeacherException


def enroll_as_student(user, course):
    participation, created = Participation.objects.get_or_create_student(user=user, course=course)
    if not created:
        if participation.role == Participation.Role.STUDENT:
            raise AlreadyEnrolledAsStudentException
        raise AlreadyEnrolledAsTeacherException
    set_course_session(participation)


def set_course_session(participation):
    course_session = CourseSession(participation=participation)
    course_session.save()

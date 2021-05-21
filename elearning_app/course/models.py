from django.db import models
from django.db.models import Count, Q
from polymorphic.models import PolymorphicModel
from django.conf import settings


class Category(models.Model):
    title = models.CharField(max_length=100)

    def __str__(self):
        return self.title


class CourseQuerySet(models.QuerySet):
    def published(self):
        return self.filter(is_published=True)

    def is_student(self, user):
        return self.filter(participations__role=Participation.Role.STUDENT, participations__user_id=user.id)

    def attach_number_of_completed_steps(self, user):
        return self.annotate(
            number_of_completed_steps=Count(
                "participations__coursesession__theorysessions__id",
                distinct=True,
                filter=Q(
                    participations__coursesession__theorysessions__is_completed=True
                )
                & Q(participations__role=Participation.Role.STUDENT)
                & Q(participations__user_id=user.id),
            )
            + Count(
                "participations__coursesession__testsessions__id",
                distinct=True,
                filter=Q(participations__coursesession__testsessions__is_completed=True)
                & Q(participations__role=Participation.Role.STUDENT)
                & Q(participations__user_id=user.id),
            )
        )

    def attach_number_of_steps(self):
        return self.annotate(number_of_steps=Count("lessons__steps", distinct=True))


class Course(models.Model):
    title = models.CharField(max_length=100, unique=True)
    description = models.TextField()
    category = models.ForeignKey('Category', on_delete=models.PROTECT)
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)
    is_published = models.BooleanField(default=False)
    users = models.ManyToManyField(settings.AUTH_USER_MODEL, through='Participation')

    objects = CourseQuerySet.as_manager()

    def __str__(self):
        return self.title


class ParticipationManager(models.Manager):
    def get_or_create_student(self, user, course):
        return self.get_or_create(user=user, course=course, defaults={'role': Participation.Role.STUDENT})


class Participation(models.Model):
    class Role(models.TextChoices):
        STUDENT = 'Student'
        TEACHER = 'Teacher'

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='participations')
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='participations')
    role = models.CharField(max_length=7, choices=Role.choices, default=Role.STUDENT)

    objects = ParticipationManager()

    class Meta:
        unique_together = (("user", "course"),)


class Lesson(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    course = models.ForeignKey('Course', on_delete=models.CASCADE, related_name='lessons')
    position = models.IntegerField()
    is_published = models.BooleanField(default=False)

    class Meta:
        ordering = ['position']

    def __str__(self):
        return self.title


class Step(PolymorphicModel):
    lesson = models.ForeignKey('Lesson', on_delete=models.CASCADE, related_name='steps')
    position = models.IntegerField()

    class Meta:
        ordering = ['position']

    def __str__(self):
        return self.title


class Theory(Step):
    title = models.CharField(max_length=100)
    body = models.TextField()


class Test(Step):
    title = models.CharField(max_length=100)
    body = models.TextField()


class Question(models.Model):
    title = models.CharField(max_length=100)
    test = models.ForeignKey('Test', on_delete=models.CASCADE, related_name='questions')

    def __str__(self):
        return self.title


class Answer(models.Model):
    title = models.CharField(max_length=100)
    is_correct = models.BooleanField(default=False)
    question = models.ForeignKey('Question', on_delete=models.CASCADE, related_name='answers')

    def __str__(self):
        return self.title


class CourseSession(models.Model):
    is_completed = models.BooleanField(default=False)
    participation = models.OneToOneField(Participation, on_delete=models.CASCADE)


class TheorySession(models.Model):
    is_completed = models.BooleanField(default=False)
    course_session = models.ForeignKey(CourseSession, on_delete=models.CASCADE, related_name='theorysessions')
    theory = models.ForeignKey(Theory, on_delete=models.CASCADE, related_name='theorysessions')

    class Meta:
        unique_together = (("course_session", "theory"),)


class TestSession(models.Model):
    is_completed = models.BooleanField(default=False)
    course_session = models.ForeignKey(CourseSession, on_delete=models.CASCADE, related_name='testsessions')
    test = models.ForeignKey(Test, on_delete=models.CASCADE, related_name='testsessions')

    class Meta:
        unique_together = (("course_session", "test"),)

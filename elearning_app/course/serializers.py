from rest_framework import serializers
from rest_polymorphic.serializers import PolymorphicSerializer
from .models import Course, Category, Lesson, Theory, Test


class CourseListResponseSerializer(serializers.ModelSerializer):
    number_of_steps = serializers.IntegerField(required=True)
    number_of_completed_steps = serializers.IntegerField(required=False)

    class Meta:
        model = Course
        fields = ['id', 'title', 'description', 'number_of_steps', 'number_of_completed_steps']


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'title']


class TheorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Theory
        fields = ["id", "position", "title", "body"]


class TestSerializer(serializers.ModelSerializer):
    class Meta:
        model = Test
        fields = ["id", "position", "title", "body"]


class StepSerializer(PolymorphicSerializer):
    model_serializer_mapping = {
        Theory: TheorySerializer,
        Test: TestSerializer}


class LessonSerializer(serializers.ModelSerializer):
    steps = StepSerializer(many=True)

    class Meta:
        model = Lesson
        fields = ['id', 'title', 'description', 'position', 'steps']


class CourseSerializer(serializers.ModelSerializer):
    lessons = LessonSerializer(many=True)
    number_of_steps = serializers.IntegerField(required=True)
    number_of_completed_steps = serializers.IntegerField(required=False)

    class Meta:
        model = Course
        fields = ['id', 'title', 'description', 'lessons', 'number_of_steps', 'number_of_completed_steps']

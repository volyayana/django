import pytest
from rest_framework.test import APIClient
from model_bakery import baker

from students.models import Student, Course
from django.conf import settings


@pytest.fixture
def client():
    return APIClient()

@pytest.fixture
def student_factory():
    def factory(*args, **kwargs):
        return baker.make(Student, *args, **kwargs)
    return factory

@pytest.fixture
def course_factory():
    def factory(*args, **kwargs):
        return baker.make(Course, *args, **kwargs)
    return factory


@pytest.mark.django_db
def test_courses_get_retrieve(client, course_factory):
    courses = course_factory(_quantity=5)
    response = client.get(f'/api/v1/courses/{courses[0].id}/')
    assert response.status_code == 200
    assert response.json()['name'] == courses[0].name


@pytest.mark.django_db
def test_courses_get(client, course_factory):
    courses_db = course_factory(_quantity=5)
    response = client.get('/api/v1/courses/')
    assert response.status_code == 200
    for i, c in enumerate(response.json()):
        assert c['name'] == courses_db[i].name


@pytest.mark.django_db
def test_courses_filter_id(client, course_factory):
    courses_db = course_factory(_quantity=5)
    response = client.get(f'/api/v1/courses/', data={'id': courses_db[1].id})
    assert response.status_code == 200
    assert len(response.json()) == 1
    assert response.json()[0]['name'] == courses_db[1].name


@pytest.mark.django_db
def test_courses_filter_name(client, course_factory):
    courses_db = course_factory(_quantity=5)
    target_course_name = courses_db[2].name
    response = client.get(f'/api/v1/courses/', data={'name': target_course_name})
    assert response.status_code == 200
    assert response.json()[0]['id'] == courses_db[2].id


@pytest.mark.django_db
def test_courses_create(client):
    count = Course.objects.count()
    response = client.post('/api/v1/courses/', data={'name': 'New test course'})
    assert response.status_code == 201
    assert Course.objects.count() == count + 1
    assert Course.objects.get(id=response.json()['id']).name == response.json()['name']


@pytest.mark.django_db
def test_courses_update(client, course_factory):
    new_course = Course.objects.create(name='test_courses_update')
    response = client.put(f'/api/v1/courses/{new_course.id}/', data={'name': 'test_courses_update_new'})
    assert response.status_code == 200
    assert Course.objects.get(id=response.json()['id']).name == 'test_courses_update_new'


@pytest.mark.django_db
def test_courses_delete(client):
    count = Course.objects.count()
    new_course = Course.objects.create(name='test_courses_delete')
    response = client.delete(f'/api/v1/courses/{new_course.id}/')
    assert response.status_code == 204
    assert Course.objects.count() == count


@pytest.mark.parametrize("max_students,current_students,response_code", [(2, 1, 200), (3, 4, 400)])
@pytest.mark.django_db
def test_students_max_count(client, student_factory, max_students, current_students, response_code):
    new_course = Course.objects.create(name='test_students_max_count')
    students = student_factory(_quantity=current_students)
    settings.MAX_STUDENTS_PER_COURSE = max_students
    student_ids = [student.id for student in students]
    response = client.patch(f'/api/v1/courses/{new_course.id}/', data={'students': student_ids})
    assert response.status_code == response_code

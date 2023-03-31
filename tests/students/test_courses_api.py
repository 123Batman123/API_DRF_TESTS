import pytest
from model_bakery import baker
from rest_framework.test import APIClient
from students.models import Student, Course


@pytest.fixture
def test_with_specific_settings(settings):
    settings.MAX_STUDENTS_PER_COURSE = 20
    print(settings.MAX_STUDENTS_PER_COURSE)
    assert settings.MAX_STUDENTS_PER_COURSE

@pytest.fixture
def client():
    return APIClient()


@pytest.fixture
def student_factory():
    def factory(*args, **kwargs):
        return baker.make(Student, *args, **kwargs)

    return factory


@pytest.fixture
def course_factory(student_factory):
    def factory(*args, **kwargs):
        students_set = student_factory(_quantity=5)
        return baker.make(Course,
                          students=students_set,
                          *args,
                          **kwargs,
                          make_m2m=True)

    return factory

@pytest.mark.django_db
def test_get_1_course(client, course_factory, student_factory):
    # Arrange
    test_id = 7
    courses = course_factory(_quantity=10)
    # python = Course.objects.create(name='Python')
    # python.students.create(name='Tom', birth_date='1900-01-01')

    # Act
    res = client.get(f'http://127.0.0.1:8000/api/v1/courses/{test_id}/')
    data = res.json()
    print(f'LOOK{res.json()}, courses{courses} ') #{Student.objects.all()[0].name}

    # Assert
    assert res.status_code == 200
    assert data['name'] == courses[test_id-1].name




@pytest.mark.django_db
def test_get_list_course(client, course_factory):
    # Arrange
    courses = course_factory(_quantity=10)

    # Act
    res = client.get(f'http://127.0.0.1:8000/api/v1/courses/')

    data = res.json()

    # Assert
    assert res.status_code == 200
    assert [i["id"] for i in data] == [i.id for i in courses]



@pytest.mark.django_db
def test_check_filter_course(client, course_factory):
    # Arrange
    test_id = 21
    course_factory(_quantity=10)

    # Act
    res = client.get('http://127.0.0.1:8000/api/v1/courses/', {'id': 21})

    data = res.json()

    # Assert
    assert res.status_code == 200
    assert data[0]['id'] == test_id


@pytest.mark.django_db
def test_check_name_filter_course(client, course_factory):
    # Arrange
    courses = course_factory(_quantity=10)
    get_name = courses[0].name

    # Act
    res = client.get('http://127.0.0.1:8000/api/v1/courses/', {'name': get_name})

    data = res.json()
    print(f'LOOK{res.json()}, courses{courses} ')  # {Student.objects.all()[0].name}

    # Assert
    assert res.status_code == 200
    assert get_name == data[0]['name']


@pytest.mark.django_db
def test_check_create_course(client, course_factory):
    # Arrange
    data = {"name": 'Python_2'}

    # Act
    res = client.post('http://127.0.0.1:8000/api/v1/courses/', data=data)

    data_r = res.json()
    print(data_r)

    # Assert
    assert res.status_code == 201
    assert data_r['name'] == data['name']


@pytest.mark.django_db
def test_check_put_course(client, course_factory):
    # Arrange
    course_factory(_quantity=10)
    data = {"name": 'Python_2'}

    # Act
    response = client.put('http://127.0.0.1:8000/api/v1/courses/42/', data=data)

    data_r = response.json()
    print(f'AAAAA{data_r}')

    # Assert
    assert response.status_code == 200
    assert data_r['name'] == data['name']


@pytest.mark.django_db
def test_check_delete_course(client, course_factory):
    # Arrange
    course_factory(_quantity=10)
    test_id = 52

    # Act
    response = client.delete(f'http://127.0.0.1:8000/api/v1/courses/{test_id}/')
    response_get = client.get('http://127.0.0.1:8000/api/v1/courses/')
    data = [x["id"] for x in response_get.json()]

    # Assert
    assert response.status_code == 204
    assert test_id not in data



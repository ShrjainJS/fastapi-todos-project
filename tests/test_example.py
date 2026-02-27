import pytest

def test_equal_or_not_equal():
    assert 3 == 3
    assert 3 != 1


class Student:
    def __init__(self, first_name: str, last_name: str, major: str, years: int) -> None:
        self.first_name = first_name
        self.last_name = last_name
        self.major = major
        self.years = years
    
@pytest.fixture
def default_student():
    return Student('John', 'Doe', 'CS', 3)

def test_person_init(default_student):
    assert default_student.first_name == 'John', 'first Name should be John'
    assert default_student.last_name == 'Doe', 'last name should be Doe'
    assert default_student.major == 'CS', 'Should be CS'
    assert default_student.years == 3, 'Should be 3'
    assert isinstance(default_student.years, int)
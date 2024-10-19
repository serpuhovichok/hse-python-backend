import pytest
from datetime import date
from lecture_4.demo_service.core.users import password_is_longer_than_8, UserService, UserInfo
from lecture_4.demo_service.core.users import UserEntity, UserRole


@pytest.mark.parametrize(
    ("password", "expected_result"),
    [
        ("1234567", False),
        ("12345678", False),
        ("123456789", True),
    ],
)
def test_password_is_longer_than_8(password: str, expected_result: bool):
    assert password_is_longer_than_8(password) is expected_result

def test_user_service_ok():
    user_service = UserService(password_validators=[password_is_longer_than_8])
    user_info = UserInfo(
        username='test_username',
        name='test_name',
        birthdate=date(2001, 1, 1),
        password='test_password'
    )
    user_entity = UserEntity(uid=1, info=user_info)
    assert user_service.register(user_info=user_info) == user_entity

@pytest.mark.parametrize(
    ("username", "test_name", "birthdate", "password", "expected_result"),
    [
        ('test_username', 'test_name', date(2001, 1, 1), 'test_password', "username is already taken"),
    ],
)
def test_user_service_exception_username_is_already_taken(
        username,
        test_name,
        birthdate,
        password,
        expected_result
):
    user_service = UserService(password_validators=[password_is_longer_than_8])
    user_info = UserInfo(
        username=username,
        name=test_name,
        birthdate=birthdate,
        password=password
    )
    user_entity = UserEntity(uid=1, info=user_info)
    assert user_service.register(user_info=user_info) == user_entity
    with pytest.raises(ValueError) as exception:
        user_service.register(user_info=user_info)
    assert expected_result in str(exception.value)


@pytest.mark.parametrize(
    ("username", "test_name", "birthdate", "password", "expected_result"),
    [
        ('test_username', 'test_name', date(2001, 1, 1), 'test', "invalid password"),
    ],
)
def test_user_service_exception_invalid_password(
        username,
        test_name,
        birthdate,
        password,
        expected_result
):
    user_service = UserService(password_validators=[password_is_longer_than_8])
    user_info = UserInfo(
        username=username,
        name=test_name,
        birthdate=birthdate,
        password=password
    )
    with pytest.raises(ValueError) as exception:
        user_service.register(user_info=user_info)
    assert expected_result in str(exception.value)

@pytest.mark.parametrize(
    ("username", "test_name", "birthdate", "password"),
    [
        ('test_username', 'test_name', date(2001, 1, 1), 'test_password'),
    ],
)
def test_get_by_username(
        username,
        test_name,
        birthdate,
        password
):
    user_service = UserService(password_validators=[password_is_longer_than_8])
    user_info = UserInfo(
        username=username,
        name=test_name,
        birthdate=birthdate,
        password=password
    )
    assert user_service.get_by_username(username) is None
    user_service.register(user_info)
    user_entity = UserEntity(uid=1, info=user_info)

    assert user_service.get_by_username(username) == user_entity

@pytest.mark.parametrize(
    ("username", "test_name", "birthdate", "password"),
    [
        ('test_username', 'test_name', date(2001, 1, 1), 'test_password'),
    ],
)
def test_get_by_id(
        username,
        test_name,
        birthdate,
        password
):
    user_service = UserService(password_validators=[password_is_longer_than_8])
    user_info = UserInfo(
        username=username,
        name=test_name,
        birthdate=birthdate,
        password=password
    )
    assert user_service.get_by_id(1) is None
    user_service.register(user_info)
    user_entity = UserEntity(uid=1, info=user_info)
    assert user_service.get_by_id(1) == user_entity


@pytest.mark.parametrize(
    ("username", "test_name", "birthdate", "password"),
    [
        ('test_username', 'test_name', date(2001, 1, 1), 'test_password'),
    ],
)
def test_grant_admin(
        username,
        test_name,
        birthdate,
        password
):
    user_service = UserService(password_validators=[password_is_longer_than_8])
    user_info = UserInfo(
        username=username,
        name=test_name,
        birthdate=birthdate,
        password=password
    )
    with pytest.raises(ValueError) as exception:
        user_service.grant_admin(1)
    assert "user not found" in str(exception.value)
    user_service.register(user_info)
    user_service.grant_admin(1)
    user = user_service.get_by_id(1)
    assert user.info.role == UserRole.ADMIN
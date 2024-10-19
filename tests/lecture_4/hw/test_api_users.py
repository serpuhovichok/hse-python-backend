import pytest
from datetime import date
from http import HTTPStatus
from fastapi import HTTPException
from fastapi.responses import PlainTextResponse

from lecture_4.demo_service.api.users import (register_user, RegisterUserRequest,
                                              UserResponse, UserRole, UserServiceDep, AuthorDep,
                                              get_user, UserInfo, promote_user, AdminDep)


@pytest.mark.asyncio
@pytest.mark.parametrize(
    ("username", "test_name", "birthdate", "password"),
    [
        ('test_username', 'test_name', date(2001, 1, 1), 'test_password'),
    ],
)
async def test_register_user(
        username,
        test_name,
        birthdate,
        password,
) -> None:
    request = RegisterUserRequest(
        username=username,
        name=test_name,
        birthdate=birthdate,
        password=password
    )
    user_service = UserServiceDep()
    response = UserResponse(
        uid=1,
        username=username,
        name=test_name,
        birthdate=birthdate,
        role=UserRole.USER
    )
    result = await register_user(request, user_service)
    assert result == response


@pytest.mark.asyncio
@pytest.mark.parametrize(
    ("username", "test_name", "birthdate", "password"),
    [
        ('test_username', 'test_name', date(2001, 1, 1), 'test_password'),
    ],
)
async def test_get_user(
        username,
        test_name,
        birthdate,
        password,
) -> None:
    user_service = UserServiceDep()
    user_info = UserInfo(
        username=username,
        name=test_name,
        birthdate=birthdate,
        password=password,
        role=UserRole.ADMIN
    )
    author = AuthorDep(uid=1, info=user_info)
    with pytest.raises(ValueError) as exception:
        result = await get_user(user_service, author, id=1, username=username)
    assert "both id and username are provided" in str(exception.value)
    with pytest.raises(ValueError) as exception:
        result = await get_user(user_service, author, id=None, username=None)
    assert "neither id nor username are provided" in str(exception.value)

    with pytest.raises(HTTPException) as exception:
        result = await get_user(user_service, author, id=1)
    assert str(HTTPStatus.NOT_FOUND) in str(exception.value)

    request = RegisterUserRequest(
        username=username,
        name=test_name,
        birthdate=birthdate,
        password=password
    )
    await register_user(request, user_service)

    result = await get_user(user_service, author, id=1)
    response = UserResponse(
        uid=1,
        username=username,
        name=test_name,
        birthdate=birthdate,
        role=UserRole.USER
    )
    assert result == response
    result = await get_user(user_service, author, username=username)
    response = UserResponse(
        uid=1,
        username=username,
        name=test_name,
        birthdate=birthdate,
        role=UserRole.USER
    )
    assert result == response


@pytest.mark.asyncio
@pytest.mark.parametrize(
    ("username", "test_name", "birthdate", "password"),
    [
        ('test_username', 'test_name', date(2001, 1, 1), 'test_password'),
    ],
)
async def test_promote_user(
        username,
        test_name,
        birthdate,
        password,
) -> None:
    user_service = UserServiceDep()
    user_info = UserInfo(
        username=username,
        name=test_name,
        birthdate=birthdate,
        password=password,
        role=UserRole.ADMIN
    )
    author = AuthorDep(uid=1, info=user_info)
    request = RegisterUserRequest(
        username=username,
        name=test_name,
        birthdate=birthdate,
        password=password
    )
    await register_user(request, user_service)

    result = await get_user(user_service, author, id=1)
    response = UserResponse(
        uid=1,
        username=username,
        name=test_name,
        birthdate=birthdate,
        role=UserRole.USER
    )
    assert result == response
    await promote_user(id=1, _=AdminDep, user_service=user_service)
    result = await get_user(user_service, author, id=1)
    response = UserResponse(
        uid=1,
        username=username,
        name=test_name,
        birthdate=birthdate,
        role=UserRole.ADMIN
    )
    assert result == response
from http import HTTPStatus

from fastapi import Depends, APIRouter, status, HTTPException, Request
from async_fastapi_jwt_auth import AuthJWT
from async_fastapi_jwt_auth.auth_jwt import AuthJWTBearer

from schemas.user_schema import UserInDB, UserCreate, UserLogin
from services.user_service import get_user_service, UserService

router = APIRouter()
auth_dep = AuthJWTBearer()


@router.post('/signup',
             response_model=UserInDB,
             status_code=status.HTTP_201_CREATED,
             description='Регистрация пользователя')
async def signup(user_create: UserCreate, user_service: UserService = Depends(get_user_service)) -> UserInDB:
    created_user = await user_service.create_user(user_create)

    return created_user


@router.post('/login',
             status_code=status.HTTP_200_OK,
             description='Аутентификация пользователя, выдача access и refresh токенов')
async def login(user: UserLogin,
                request: Request,
                authorize: AuthJWT = Depends(auth_dep),
                user_service: UserService = Depends(get_user_service)):

    user_login = await user_service.login_user(user, request)
    if not user_login:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail='user not found')

    access_token = await authorize.create_access_token(subject=user_login)
    refresh_token = await authorize.create_refresh_token(subject=user_login)

    return {'access_token': access_token, 'refresh_token': refresh_token}


@router.post('/logout',
             status_code=status.HTTP_200_OK,
             description='Выход пользователя из системы')
async def logout(authorize: AuthJWT = Depends(auth_dep),
                 user_service: UserService = Depends(get_user_service)):

    await authorize.jwt_required()
    current_user = await authorize.get_jwt_subject()
    access_token = await authorize.get_raw_jwt()

    logout_user = await user_service.logout_user(access_token, current_user)
    if not logout_user:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail='user not found')

    return logout_user

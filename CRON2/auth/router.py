from fastapi import APIRouter, HTTPException, Depends, Cookie, Header
from ..dependencies import get_current_user
from . import schema
from .crud import UserCrud
from fastapi_jwt_auth import AuthJWT


router=APIRouter(prefix='/v1')

@router.get("/user-details")
async def user_details(user:dict=Depends(get_current_user)):
    return user

@router.post('/login', response_model=schema.LoginDetails)
async def Login(login:schema.Login,Authorize:AuthJWT=Depends()):

    password, email=login.password, login.email
    user=await UserCrud.authenticate(password=password, email=email)
    access_token=Authorize.create_access_token(subject=str(user["_id"]))
    refresh_token=Authorize.create_refresh_token(subject=str(user["_id"]))
    Authorize.set_access_cookies(access_token)
    Authorize.set_refresh_cookies(refresh_token)
    return {'access_token':access_token, 'refresh_token':refresh_token, 'user':user}


@router.post('/signup', response_model=schema.LoginDetails, summary='endpoint for users to signup', status_code=201)
async def signup(user:schema.Signup, Authorize:AuthJWT=Depends()):

    if  await UserCrud.get_user_by_email(user.email):
        raise HTTPException(status_code=400, detail='user with this email already exists')
    user=await UserCrud.create_user(user)
    access_token=Authorize.create_access_token(subject=str(user))
    refresh_token=Authorize.create_refresh_token(subject=str(user))
    Authorize.set_access_cookies(access_token)
    Authorize.set_refresh_cookies(refresh_token)
    return {'access_token':access_token, 'refresh_token':refresh_token, 'user':user}




@router.post('/refresh-token')
def refresh_token(Authorization:AuthJWT=Depends(), refresh_token:str=Cookie(default=None), Bearer:str=Header(default=None)):
    exception=HTTPException(status_code=401, detail='invalid refresh token or token has expired')
    try:
        Authorization.jwt_refresh_token_required()
        current_user=Authorization.get_jwt_subject()
        access_token=Authorization.create_access_token(current_user)
        Authorization.set_access_cookies(access_token)

        return {'access_token':access_token}
    except:
        raise exception
@router.post('/logout')
def logout(Authorize:AuthJWT=Depends()):
    Authorize.unset_jwt_cookies()
    return {'message':'successfully logout'}
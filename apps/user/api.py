from datetime import datetime, timedelta

from fastapi import APIRouter
from fastapi.params import Depends

from utils.Sqlalchemy.connect import transactional
from apps.auth.models import Verification, Token
from apps.user.models import User, UserInfo
from apps.user.schemas import UserInput, UserPasswordResetInput, UserVerificationInput, UserVerificationCreateInput, \
    UserLoginInput
from utils.fastapi_utils.debug.debug import DebugManager
from utils.pydantic_utils.response import ErrorResponseModel, SuccessResponseModel
from utils.snowflake_util import SnowflakeIDGenerator

router = APIRouter(tags=["user"], prefix="/user")

@router.get("/login")
async def user_login(param: UserLoginInput = Depends(),
                     debugger: DebugManager = Depends()):
    debugger.enabled = True
    snowflake_generator = SnowflakeIDGenerator()
    user_info = UserInfo.get_instance(error=False, debugger=debugger,
                                      username=param.username,
                                      email=param.email,
                                      phone=param.phone,
                                      password=param.password)

    if not user_info:
        if debugger.enabled:
            debugger.display()
        return ErrorResponseModel(message="Username and password don't link to an account, please try again.")

    token = snowflake_generator.generate_id(),
    expire_time = (datetime.now().date() + timedelta(days=(1 if param.stay_login == False else 365)))

    Token.add_instance(
        debugger=debugger,
        token = token,
        uid = user_info.id,
        expire_time = expire_time
    )

    if debugger.enabled:
        debugger.display()

    return SuccessResponseModel(data={"token" : token, "expire_time" : expire_time})

@router.post("/verification/create")
async def user_verification_create(param: UserVerificationCreateInput = Depends(),
                                   debugger: DebugManager = Depends()):
    debugger.enabled = False
    user = UserInfo.get_instance(error=False, debugger=debugger, phone=param.phone, email=param.email)

    if user:
        return ErrorResponseModel(message="This email or phone number is already linked to an account. Try again.")

    Verification.code_create(debugger=debugger, email=param.email,phone=param.phone)

    if debugger.enabled:
        debugger.display()

    return SuccessResponseModel()

@router.get("/verification")
async def user_verification(param: UserVerificationInput = Depends(),
                       debugger: DebugManager = Depends()):
    debugger.enabled = False
    verify_obj = Verification.get_instance(error=False, debugger=debugger,
                                           email=param.email,phone=param.phone,code=param.code
    )

    if not verify_obj:
        if debugger.enabled:
            debugger.display()

        return ErrorResponseModel(message="Incorrect verification code, try again.")

    verify_obj.delete(debugger=debugger)

    if debugger.enabled:
        debugger.display()

    return SuccessResponseModel(message="Verification Complete")

@router.get("/verification/recreate")
async def user_verification_recreate(param: UserVerificationCreateInput = Depends(),
                                     debugger: DebugManager = Depends()):
    debugger.enabled = False
    user = UserInfo.get_instance(error=False, debugger=debugger, phone=param.phone, email=param.email)

    if not user:
        if debugger.enabled:
            debugger.display()

        return ErrorResponseModel(message="User cannot be found, refresh the page to restart.")

    code_objs = Verification.get_instances_all(error=False, debugger=debugger,
                                               email=param.email,phone=param.phone)

    for code_obj in code_objs:
        code_obj.delete(debugger=debugger)

    Verification.code_create(debugger=debugger,email=param.email,phone=param.phone)

    if debugger.enabled:
        debugger.display()

    return SuccessResponseModel(message="Your user verification is now resend")

@router.post("/register")
async def register_user(param: UserInput = Depends(),
                        debugger: DebugManager = Depends()):
    debugger.enabled=False
    user_info = UserInfo.get_instance(error=False, debugger=debugger,
                                      email=param.email, username=param.username, phone=param.phone, )

    if user_info:
        error = ""
        if user_info.username == param.username and user_info.username != "":
            error += "Username, "
        if user_info.email == param.email and user_info.email != "":
            error += "Email, "
        if user_info.phone == param.phone and user_info.phone != "":
            error += "Phone number, "
        if debugger.enabled:
            debugger.display()
        return ErrorResponseModel(message=f"This is already linked to an account: {error}"
                                          f"Please login or try another one")

    with transactional() as db:
        user_info_new = UserInfo.add_instance(db=db, debugger=debugger, **param.model_dump())

        user_new = User.add_instance(db=db, debugger=debugger, uid=user_info_new.id, username=param.username)

        user_new.update(db=db, debugger=debugger, is_login=1)

    if debugger.enabled:
        debugger.display()

    return SuccessResponseModel()

@router.get("/password/reset")
async def user_password_reset(param: UserPasswordResetInput = Depends(),
                              debugger: DebugManager = Depends()):
    debugger.enabled=True
    user_info = UserInfo.get_instance(error=False, debugger=debugger,
                                      id=param.uid, username=param.username,
                                      phone=param.phone, email=param.email)

    if not user_info:
        if debugger.enabled:
            debugger.display()
        return ErrorResponseModel(message="User doesn't exist, please register an account before resetting password.")

    user_info.update(debugger=debugger, password=param.password)

    if debugger.enabled:
        debugger.display()

    return SuccessResponseModel()
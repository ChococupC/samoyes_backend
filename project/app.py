from fastapi import FastAPI, APIRouter, Depends
from fastapi.middleware.cors import CORSMiddleware

# from project.router import auto_load_routers
from project.settings import PROJECT_NAME, PROJECT_PATH, API_PREFIX
from apps.auth.api import router as auth_router
from apps.categorize.api import router as cate_router
from apps.user.api import router as user_router

app = FastAPI(title=PROJECT_NAME)
# router = APIRouter(prefix=API_PREFIX)

# auto_load_routers(app_router=router, base_path=PROJECT_PATH)
# app.include_router(auth_router)
# app.include_router(router)

# 路由注册
app.include_router(auth_router)
app.include_router(cate_router)
app.include_router(user_router)

"""
跨域处理

"""
origins = [
    "*"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # 允许访问的源列表
    allow_credentials=True,  # 允许携带 cookies
    allow_methods=["*"],  # 允许的方法
    allow_headers=["*"],  # 允许的头部
)

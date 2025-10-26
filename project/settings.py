import os
import platform
from pathlib import Path
from typing import List

from dotenv import find_dotenv, load_dotenv

# 导入 env
dotenv_path = find_dotenv(".env")
# if not dotenv_path:
#     raise EnvironmentError("Unable to find the environment.")
load_dotenv(dotenv_path=dotenv_path, override=True)

# 路由应用
ROUTE_APPS: List[str] = [
    '/auth',
]

EXCEPT_APPS: List[str] = [
]

PROJECT_PATH = Path(__file__).parents[1]  # 项目地址

# 导入来源
SOURCE_PATH = Path(os.getenv("SOURCE_PATH") or (PROJECT_PATH / "source"))
SOURCE_PATH.mkdir(parents=True, exist_ok=True)

# 添加日志进入环境变量
LOG_DIR_PATH = PROJECT_PATH / "logs"
os.environ["LOG_DIR_PATH"] = LOG_DIR_PATH.__str__()

SYSTEM = platform.system()

# 项目名称
PROJECT_NAME = os.getenv("PROJECT_NAME")  # 项目名称
# 接口前缀
API_PREFIX = os.getenv("API_PREFIX")  # 项目api前缀
# 数据库接口
USER = os.getenv("USER")
PASSWORD = os.getenv("PASSWORD")
HOST = os.getenv("HOST")
PORT = os.getenv("PORT")
DATABASE = os.getenv("DATABASE")
CONNECT = f"{USER}:{PASSWORD}@{HOST}:{PORT}/{DATABASE}"

# 项目启动

```shell
uvicorn main:app --reload
```

# 项目管理

使用conda管理Python版本
使用Poetry管理Python包

```shell
pip install poetry

# 检查版本
poetry --version

```

| 名称      | 功能                                    |
|---------|---------------------------------------|
| new     | 创建一个项目脚手架，包含基本结构、pyproject.toml 文件    |
| init    | 基于已有的项目代码创建 pyproject.toml 文件，支持交互式填写 |
| install | 安装依赖库                                 |
| update  | 更新依赖库                                 |
| add     | 添加依赖库                                 |
| remove  | 移除依赖库                                 |
| show    | 查看具体依赖库信息，支持显示树形依赖链                   |
| build   | 构建 tar.gz 或 wheel 包                   |
| publish | 发布到 PyPI                              |
| run     | 运行脚本和代码                               |
| shell   | 激活虚拟环境                                |

## 项目结构
fast_api
├── apps                        # 存放所有的app
│   ├── auth                    # 认证模块 众多app中的一个
│   │    ├── __init__.py        # 初始的包文件
│   │    ├── api.py             # 写接口的地方
│   │    ├── enums.py           # 枚举类型
│   │    ├── models.py          # 数据库模型
│   │    └── schemas.py         # 序列化器 验证输入、输出
├── project                     # 项目模块 类似于Django中的项目目录
│   ├── __init__.py             # 初始的包文件
│   ├── api.py                  # 写接口的地方
│   ├── app.py                  # FASTAPI 项目基础文件
│   └── settings.py             # 配置文件
├── source                      # 源数据 放杂物的地方
│── utils                       # 工具类 放一些常用的函数
│   ├── __init__.py             # 初始的包文件
│   └── sql_alchemy             # sql_alchemy 工具类
├── .env                        # 环境变脸文件
├── main.py                     # 项目入口文件
├── pyproject.toml              # 项目的依赖管理文件
└── README.md                   # 项目说明文件

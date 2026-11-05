from core.exceptions import register_exception_handlers
from fastapi.openapi.docs import get_swagger_ui_html
from routers import api_v2
from core.middlewares import register_middlewares
import time
from fastapi.responses import StreamingResponse
from contextlib import asynccontextmanager
from fastapi import FastAPI
from sqlmodel import SQLModel
from db.session import engine

# 这个只有运行的时候才会用到
from models.user import User
from models.chat import ChatMessage
from models.address import Address
from models.order import Order


# 1. 定义生命周期
@asynccontextmanager
async def lifespan(app: FastAPI):
    # 启动时：建表
    print("正在检查并创建数据库表...")
    SQLModel.metadata.create_all(bind=engine)
    print("数据库表准备就绪！")

    yield  # 服务器运行期间停在这里

    # 关闭时：可以做一些清理工作（目前不需要）


# 2. 把 lifespan 传给 FastAPI
app = FastAPI(
    title="FastAPI + SQLModel综合项目",
    version="1.0",
    lifespan=lifespan,
    docs_url=None,
    redoc_url=None
)



@app.get("/docs", include_in_schema=False)
async def custom_swagger_ui_html():
    return get_swagger_ui_html(
        openapi_url=app.openapi_url,
        title=app.title + " - Swagger UI",
        # 替换为国内的 CDN 地址，例如 staticfile 或 bootcdn
        swagger_js_url="https://cdn.staticfile.org/swagger-ui/5.1.0/swagger-ui-bundle.js",
        swagger_css_url="https://cdn.staticfile.org/swagger-ui/5.1.0/swagger-ui.css",
    )

@app.get('/')
def index():
    return {"Hello": "World"}

@app.get('/stream')
def stream():
    def generate():
        for i in range(3):
            yield f"data chunk {i}\n"
            time.sleep(0.1) # 模拟一点点延迟，不能加太长免得测试卡住
    return StreamingResponse(generate(), media_type="text/plain")

app.include_router(api_v2)


register_exception_handlers(app)


register_middlewares(app)


# uvicorn main9:app --reload

# 如果注册账户出现问题的报错说没有这表的话，就重启服务器试试，如果不行就在终端输入这行代码，（注意：这句代码是强行把模型导入并建表，跑完一次就行）
# python -c "from sqlmodel import SQLModel; from db.session import engine; import models.user, models.chat; SQLModel.metadata.create_all(bind=engine)"
from starlette.responses import StreamingResponse

from core.exceptions import register_exception_handlers
from fastapi import FastAPI
from fastapi.openapi.docs import get_swagger_ui_html
from routers import api_v2
from core.middlewares import register_middlewares
import time
from fastapi.responses import StreamingResponse


app = FastAPI(docs_url=None, redoc_url=None)

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

# cd 人工智能\FaA\fastapi_big_project
# uvicorn main9:app --reload
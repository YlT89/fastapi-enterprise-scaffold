import os
import json
import httpx
from langchain_core.tools import tool
from dotenv import load_dotenv

load_dotenv(encoding="utf-8")

@tool
def get_weather(loc: str) -> str:
    """查询指定城市的即时天气。参数 loc: 城市名称，如 Beijing, Shanghai."""

    # 1. 简单映射：把常见城市名转为高德需要的 adcode
    city_adcode_map = {
        "beijing": "110000",
        "shanghai": "310000",
        "guangzhou": "440100",
        "shenzhen": "440300",
    }

    # 如果用户传的是拼音，转成小写去查映射；如果没查到，可以给个默认值或直接返回错误
    city_code = city_adcode_map.get(loc.lower(), loc)

    # 2. 高德天气 API 的固定 URL
    url = "https://restapi.amap.com/v3/weather/weatherInfo"

    # 3. 正确的参数：key 和 city (adcode)
    params = {
        "key": os.getenv("GAODE_API_KEY"),
        "city": city_code,
        "extensions": "base", # base 表示实况天气，all 表示预报
    }

    try:
        response = httpx.get(url, params=params, timeout=10)
        response.raise_for_status() # 如果请求失败(4xx/5xx)会抛出异常

        data = response.json()

        # 高德返回的 JSON 如果 status 为 "0" 表示失败
        if data.get("status") == "1" and data.get("lives"):
            live = data["lives"][0]
            # 把关键信息整理成易读的字符串返回
            weather_info = f"{live['city']} {live['weather']} {live['temperature_float']}℃ {live['winddirection']}风 {live['windpower']}级"
            return json.dumps({"weather": weather_info}, ensure_ascii=False)
        else:
            return json.dumps({"error": f"高德API返回错误: {data.get('info')}"}, ensure_ascii=False)

    except Exception as e:
        return json.dumps({"error": f"请求失败: {str(e)}"}, ensure_ascii=False)
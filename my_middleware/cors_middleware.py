"""
name: cors_middleware
create_time: 2023/5/15
author: stayh

Description: 解决跨域问题
"""


class CorsMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        response["Access-Control-Allow-Origin"] = "http://192.168.31.97:5173/"  # 允许的源，可以是具体的域名或使用通配符 *
        response["Access-Control-Allow-Methods"] = "GET, POST, OPTIONS"  # 允许的请求方法
        response["Access-Control-Allow-Headers"] = "Content-Type"  # 允许的请求头
        return response


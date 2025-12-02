swagger_config = {
    "headers": [],  # 发送 Swagger 内部请求时附带的额外 Header，一般留空即可
    "specs": [
        {
          "endpoint": 'apispec_1',        # 内部用的名称，不用管
          "route": '/apispec_1.json',     # 【重要】生成的 JSON 数据文件的访问路径
          "rule_filter": lambda rule: True,  # 【重要】过滤器：决定哪些路由要显示在文档里
          "model_filter": lambda tag: True,  # 过滤器：决定哪些数据模型要显示
        }
    ],
    "static_url_path": "/flasgger_static",  # Swagger UI 所需的 JS/CSS 静态文件存放路径
    "swagger_ui": True,                     # 是否开启 HTML 页面？True 表示开启
    "specs_route": "/apidocs/"              # 【最重要】你在浏览器里输入的访问地址！
}

template = {
    "swagger": "2.0",  # 使用 Swagger 2.0 标准
    "info": {
        "title": "我的 Flask API 文档",      # 页面大标题
        "description": "...",              # 标题下的小字描述
        "version": "1.0.0"                 # API 版本号
    },
    "securityDefinitions": {
        "Bearer": {                    # 方案名称（你可以随便起，但在 docstring 里引用要一致）
            "type": "apiKey",          # 类型：API Key
            "name": "Authorization",   # 【关键】HTTP Header 的键名 (Key)
            "in": "header",            # 【关键】这个键放在哪里？放在 Header 里
            "description": "请输入你的 Bearer Token，格式为 Bearer <token>"       # 点击 Authorize 按钮时看到的提示语
        }
    }
}
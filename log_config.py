# log_config.py
import logging
import sys
from loguru import logger

def setup_logging():
    # 1. 移除 Loguru 默认的处理器 (防止重复打印)
    logger.remove()

    # 2. 添加控制台输出 (带颜色，方便开发调试)
    logger.add(
        sys.stderr,
        format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level: <8}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - <level>{message}</level>",
        level="DEBUG"
    )

    # 3. 添加文件输出 (生产环境必备)
    # rotation="1 day": 每天生成一个新文件 (或者 "500 MB")
    # retention="10 days": 只保留最近 10 天的日志
    # compression="zip": 旧日志自动压缩
    logger.add(
        "logs/app_{time:YYYY-MM-DD}.log",
        rotation="00:00", # 每天午夜轮转
        retention="10 days",
        encoding="utf-8",
        level="INFO",
        enqueue=True # 异步写入，不阻塞主线程
    )

    # 4. (进阶) 让 Flask 内部的日志 (如 404, 500 报错) 也由 Loguru 接管
    # 这段代码有点魔性，照抄即可
    class InterceptHandler(logging.Handler):
        def emit(self, record):
            try:
                level = logger.level(record.levelname).name
            except ValueError:
                level = record.levelno
            
            frame, depth = logging.currentframe(), 2
            while frame.f_code.co_filename == logging.__file__:
                frame = frame.f_back
                depth += 1
            
            logger.opt(depth=depth, exception=record.exc_info).log(level, record.getMessage())

    # 替换 Flask (Werkzeug) 的默认 Logger
    logging.basicConfig(handlers=[InterceptHandler()], level=0)
    logging.getLogger("werkzeug").handlers = []
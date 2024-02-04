import logging

# 创建一个日志记录器
logger = logging.getLogger('custom_logs')
logger.setLevel(logging.INFO)

# 创建一个文件处理器，并设置级别和格式
file_handler = logging.FileHandler('loggs.log')
file_handler.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
file_handler.setFormatter(formatter)

# 将文件处理器添加到日志记录器
logger.addHandler(file_handler)

# 记录信息
logger.info('这是一个信息级别的日志，它会被写入文件')

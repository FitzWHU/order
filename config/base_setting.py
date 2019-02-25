SERVER_PORT = 8999
DEBUG = False
SQLALCHEMY_ECHO = False

AUTH_COOKIE_NAME = 'mooc_food'

# 过滤url
IGNORE_URLS = [
    '^/user/login',
    '^/api'
]

IGNORE_CHECK_LOGIN_URLS = [
    "^/static",
    '^/favicon.ico'
]

PAGE_SIZE = 10
PAGE_DISPLAY = 10

STATUS_MAPPING = {
    '1': '正常',
    '0': '已删除'
}
MINA_APP = {
    'appid':'wx641d3b62ce8853a7',
    'secret': '47bd5a75364713146769d3db24635b20'
}

UPLOAD = {
    'ext': ['jpg', 'gif', 'bmp', 'jpeg', 'png'],
    'prefix_path': '/web/static/upload/',
    'prefix_url': '/static/upload/'
}

APP = {
    'domain': 'http://192.168.43.131:8999'
}
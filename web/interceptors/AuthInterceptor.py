import re

from application import app
from flask import request, redirect, g

from common.models.User import User
from common.libs.user.UserService import UserService
from common.libs.UrlManager import UrlManager


@app.before_request
def before_request():
    # 登录界面不检测
    ignore_urls = app.config['IGNORE_URLS']
    ignore_check_login_urls = app.config['IGNORE_CHECK_LOGIN_URLS']
    path = request.path
    pattern = re.compile('%s' % '|'.join(ignore_check_login_urls))
    if pattern.match(path):
        # app.logger.info('这是静态文件和图标过滤' + path)
        return
    # 判断是否已经登录
    user_info = check_login()

    g.current_user = None
    if user_info:
        g.current_user = user_info

    pattern = re.compile('%s' % '|'.join(ignore_urls))
    if pattern.match(path):
        # app.logger.info('这是登录过滤' + path)
        return

    if not user_info:
        return redirect(UrlManager.buildUrl('/user/login'))
    return

'''
    判断用户是否已经登录
'''


def check_login():
    cookies = request.cookies
    auth_cookie = cookies[app.config['AUTH_COOKIE_NAME']] if app.config['AUTH_COOKIE_NAME'] in cookies else ''
    # app.logger.info(auth_cookie)
    if auth_cookie is None:
        # app.logger.debug('这是没有cookie返回')
        return False
    auth_info = auth_cookie.split("#")
    if len(auth_info) != 2:
        # app.logger.debug('这是分割后没有两个返回')
        return False
    try:
        user_info = User.query.filter_by(uid=auth_info[1]).first()
    except Exception:
        # app.logger.debug('这是分割后没有查到返回')
        return False

    if user_info is None:
        # app.logger.debug('这是分割后查到是空返回')
        return False

    if auth_info[0] != UserService.geneAuthCode(user_info):
        # app.logger.debug('这是分割后对比不正却返回')
        return False

    if user_info.status != 1:
        return False

    return user_info
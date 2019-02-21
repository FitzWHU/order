import json

from web.controllers.api import route_api
from flask import request, jsonify
from application import app, db
import requests
from common.models.member.Member import Member
from common.models.member.Oauth_Member_Bind import OauthMemberBind
from common.libs.Helper import getCurrentData


@route_api.route('/member/login', methods=['GET', "POST"])
def login():
    resp = {'code': 200, 'msg': '成功', 'data': {}}
    req = request.values
    code = req['code'] if 'code' in req else''
    if not code or len(code) < 1:
        resp['code'] = -1
        resp['msg'] = '需要code'
        return jsonify(resp)
    url = 'https://api.weixin.qq.com/sns/jscode2session?appid={0}&secret={1}&js_code={2}&grant_type=authorization_code'\
        .format(app.config['MINA_APP']['appid'], app.config['MINA_APP']['secret'], code)
    r = requests.get(url)
    res = json.loads(r.text)
    app.logger.info(res)
    openid = res['openid']

    nickname = req['nickName'] if 'nickName' in req else ''
    sex = req['gender'] if 'gender' in req else 0
    avatar = req['avatarUrl'] if 'avatarUrl' in req else ''

    '''
        判断是否已经注册了
    '''
    bind_info = OauthMemberBind.query.filter_by(openid=openid, type=1).first()
    if not bind_info:
        model_member = Member()
        model_member.nickname = nickname
        model_member.sex = sex
        model_member.avatar = avatar
        model_member.salt = ''
        model_member.updated_time = model_member.created_time = getCurrentData()
        db.session.add(model_member)
        db.session.commit()
        model_bind = OauthMemberBind()
        model_bind.member_id = model_member.id
        model_bind.type = 1
        model_bind.openid = openid
        model_bind.extra = ''
        model_bind.updated_time = model_bind.created_time = getCurrentData()
        db.session.add(model_bind)
        db.session.commit()
        bind_info = model_bind

    member_info = Member.query.filter_by(id=bind_info.member_id).first()
    resp['data'] = {'nickname': member_info.nickname}
    return jsonify(resp)


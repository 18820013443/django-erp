from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from django.http import JsonResponse, response
from .models import UserInfo, UserToken
from account.serializers import UserSerializer
import hashlib
import coreapi
from rest_framework.schemas import AutoSchema
from rest_framework.response import Response
from account.utils.jwt_auth import create_token
# Create your views here.

def hash_code(s, salt='mysite'):
    h = hashlib.sha256()
    s += salt
    h.update(s.encode()) # update方法只接收bytes类型
    return h.hexdigest()

class AuthViewSchema(AutoSchema):
    def get_manual_fields(self, path, method):
        extra_fields = []
        if method.lower() == 'post':
            extra_fields = [
                coreapi.Field('username'),
                coreapi.Field('password'),
            ]
        manual_fields = super().get_manual_fields(path, method)
        return manual_fields + extra_fields

class AuthView(APIView):
    authentication_classes = []
    schema = AuthViewSchema()
    def post(self, request, *args, **kwargs):
        ret = {'code':1000, 'msg':None}
        username = request.data.get('username')
        password = request.data.get('password')
        print(username, password)
        user = UserInfo.objects.filter(username=username, password=password).first()
        if not user:
            ret['code'] = 1001
            ret['msg'] = '用户名或密码错误!'
            return Response(ret)
        # token = hash_code(username)
        # UserToken.objects.update_or_create(userinfo=user, defaults={'token':token})
        token  = create_token({'username': username})
        ret['msg'] = "登录成功"
        ret['id'] = user.id
        ret['username'] = username
        ret['token'] = token
        return Response(ret)

class UserView(ModelViewSet):
    def list(self, request, *args, **kwargs):
        data = {}
        data['id'] = request.user.id
        data['username'] = request.user.username
        data['password'] = request.user.password
        data['phone'] = request.user.phone
        data['wechat'] = request.user.wechat
        data['token'] = request.auth.token
        return JsonResponse(data)


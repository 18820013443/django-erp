from rest_framework.authentication import BaseAuthentication
from account.models import UserInfo, UserToken
from rest_framework import exceptions
from account.utils.jwt_auth import parse_payload


class UserAuthentication(BaseAuthentication):
    def authenticate(self, request):
        token = request.query_params.get('token')
        payload = parse_payload(token)
        if not payload['status']:
            raise exceptions.AuthenticationFailed(payload)

        # 如果想要request.user等于用户对象，此处可以根据payload去数据库中获取用户对象。
        return (payload, token)


        # # token = request.query_params.get('token')
        # token = request._request.GET.get('token')
        # obj = UserToken.objects.filter(token=token).first()
        # # auth = UserToken.objects.get(user=user, token=token)
        # if not obj:
        #     raise exceptions.AuthenticationFailed('用户认证失败')
        # user = obj.userinfo
        # return (user,obj)


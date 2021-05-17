from rest_framework import serializers
from account.models import UserInfo, UserToken


class UserSerializer(serializers.ModelSerializer):
    token = serializers.SerializerMethodField()
    class Meta:
        model = UserInfo
        fileds = ['id', 'username', 'password', 'phone', 'wechat', 'token']

    def get_token(self, user):
        pass
    # def get_token(self, user):
    #     token_list = user.token_set.all()
    #     if len(token_list)>0:
    #         return token_list[0]
    #     else:
    #         return ""
import random

from django.shortcuts import render

from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model
from django.db.models import Q

from rest_framework import mixins, viewsets, status
from rest_framework.response import Response
from rest_framework import permissions
from rest_framework import authentication
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from rest_framework_jwt.serializers import jwt_payload_handler, jwt_encode_handler

from .serializers import SmsSerializer, UserRegSerializer, UserDetailSerializer
from extrac.utils.SMS import yun_pian
from VcrTStore.settings import API_KEY
from .models import VerifyCode

User = get_user_model()
class CustomBackend(ModelBackend):
    """
    自定义用户验证
    """
    def authenticate(self, username=None, password=None, **kwargs):
        try:
            user = User.objects.get(Q(username = username)|Q(phone=username))
            if user.check_password(password):
                return user
        except Exception as e:
            return None
# Create your views here.

class SmsCodeViewSet(mixins.CreateModelMixin, viewsets.GenericViewSet):
    """
    发送短信验证码
    """
    serializer_class = SmsSerializer

    def generate_code(self):
        """
        生成验证码
        """
        seeds = '123456789'
        random_str = []
        for i in range(4):
            random_str.append(random.choice(seeds))
        return ''.join(random_str)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True) # 400 错误

        phone = serializer.validated_data['phone']
        code = self.generate_code()
        print(phone, code)
        yp = yun_pian.YunPian(API_KEY)
        sms_status =  yp.send_sms(code=code, phone=phone)
        if sms_status['code'] == 0:
            return Response({
                'phone': sms_status['msg']
            }, status=status.HTTP_400_BAD_REQUEST)
        else:
            code_record = VerifyCode(code=code, phone=phone)
            code_record.save()
            return Response({
                'mobile': phone,
                'code': code
            }, status=status.HTTP_201_CREATED)

class UserRegViewSet(mixins.CreateModelMixin, mixins.UpdateModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    """
    用户
    """
    queryset = User.objects.all()
    serializer_class = UserRegSerializer
    permission_classes = (permissions.IsAuthenticated, )
    authentication_classes = (JSONWebTokenAuthentication, authentication.SessionAuthentication)

    def get_permissions(self):
        if self.action == 'retrieve':
            return [permissions.IsAuthenticated()]
        elif self.action == 'create':
            return []
        return []

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return UserDetailSerializer
        elif self.action == 'create':
            return UserRegSerializer
        return UserDetailSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        print(serializer.initial_data)
        serializer.is_valid(raise_exception=True)
        user = self.perform_create(serializer)

        # 在create 中自定义方法 -> jwt 认证
        re_dict = serializer.data
        payload = jwt_payload_handler(user)
        re_dict['token'] = jwt_encode_handler(payload)
        re_dict['name'] = user.name if user.name else user.username

        headers = self.get_success_headers(serializer.data)
        print(re_dict)
        return Response(re_dict, status=status.HTTP_201_CREATED, headers=headers)

    def get_object(self):
        """
        retrieve 与 delete会用到 id
        不管 id 传任何数字，都得到的是当前的用户
        """
        return self.request.user

    def perform_create(self, serializer):
        return serializer.save()

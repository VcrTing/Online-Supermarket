import re
import datetime

from rest_framework import serializers
from rest_framework import validators as vldtor

from VcrTStore.settings import REGEX_PHONE
from django.contrib.auth import get_user_model
User = get_user_model()

from .models import VerifyCode

class SmsSerializer(serializers.Serializer):
    phone = serializers.CharField(max_length=11)

    def validate_phone(self, phone):
        """
        验证手机号码
        """
        if User.objects.filter(phone = phone).count():
            raise serializers.ValidationError('用户已存在')

        # 验证手机号码是否
        # if not re.match(REGEX_PHONE, phone):
        #    raise serializers.ValidationError('手机号码非法')

        # 验证码发送频率 (一分钟之前的时间)
        one_minits_ago = datetime.datetime.now() - datetime.timedelta(hours=0, minutes=1, seconds=0)
        if VerifyCode.objects.filter(add_time__gt=one_minits_ago, phone=phone):
            raise serializers.ValidationError('距离上一次发送未超过60s')
        return phone

class UserDetailSerializer(serializers.ModelSerializer):
    """
    用户详情序列化类
    """
    birthday = serializers.DateField(source='bith', help_text='生日', label='生日')
    mobile = serializers.CharField(source='phone', help_text='电话', label='电话')
    name = serializers.CharField(help_text='昵称', label='昵称')

    class Meta:
        model = User
        fields = ('name', 'birthday', 'email', 'mobile', 'gender')

class UserRegSerializer(serializers.ModelSerializer):
    code = serializers.CharField(max_length=4, min_length=4, label='验证码', write_only=True,
                                 error_messages={
                                    'required': '请输入验证码',
                                     'max_length': '验证码为4位数',
                                     'min_length': '验证码为4位数',
                                     'blank': '请输入验证码'
                                 },
                                 help_text='验证码')
    username = serializers.CharField(required=True, allow_blank=False,
                                 validators=[vldtor.UniqueValidator(queryset=User.objects.all(), message='用户验证失败')],
                                 help_text='用户名')
    password = serializers.CharField(help_text='密码', label='密码', write_only=True,
                                     style={
                                         'input_type': 'password'
                                     })

    def create(self, validated_data):
        user = super(UserRegSerializer, self).create(validated_data=validated_data)
        user.set_password(validated_data['password'])
        user.save()
        return user

    def validate_code(self, code):
        verify_records = VerifyCode.objects.filter(phone=self.initial_data['username']).order_by('-add_time')
        if verify_records:
            last_record = verify_records[0]
            five_minits_ago = datetime.datetime.now() - datetime.timedelta(hours=0, minutes=5, seconds=0)
            if five_minits_ago > last_record.add_time:
                raise serializers.ValidationError('验证码已经过期')
            if last_record.code != code:
                raise serializers.ValidationError('验证码错误')
        else:
            raise serializers.ValidationError('验证码错误')
        return code

    def validate(self, attrs):
        attrs['phone'] = attrs['username']
        print('attr =', attrs)
        del attrs['code']
        return attrs

    class Meta:
        model = User
        fields = ('username', 'code', 'password')
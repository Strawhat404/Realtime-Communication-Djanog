from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import UserDevice,LoginHistory

User = get_user_model()

class UserRegisterationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only = True, min_length=8)
    confirm_password  = serializers.CharField(write_only = True)
    
    class Meta:
        model = User
        fields = ('id','username','email','password','confirm_password','first_name','last_name','phone_number')
        extra_kwargs = {
            'password':{'write_only':True},
            'email': {'required':True}
        }
    def validate(self,data):
        if data['password'] != data.pop('confirm_password'):
            raise serializers.ValidationError("password do not match")
        return data
    def create(self,validated_data):
        return User.objects.create_user(**validated_data)
    
class UserDeviceSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserDevice
        fields = ('id','device_name','device_type','is_trusted','last_used')
        read_only_fields = ('laast_used',)
        
    class LoginHistorySerializer(serializers.ModelSerializer):
        class Meta:
            model = LoginHistory
            fields = '__all__'
            read_only_fields = ('user','login_datetime','ip_address')
    
    class ChangePasswordSerializer(serializers.Serializer):
        old_password =  serializers.CharField(required = True)
        new_password = serializers.CharField(required = True, min_length = 8)
        confirm_new_password = serializers.CharField(requiered= True)
        
        
        def validate(self,data):
            if data['new_password'] != data['confirm_new_password']:
                raise serializers.ValidationError("New password do not match")
            return data
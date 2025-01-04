# from rest_framework import serializers
# from .models import User, Role, UserRole

# class UserSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = User
#         fields = ['id', 'username', 'full_name', 'telefono', 'is_active', 'created_at']

# class RoleSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Role
#         fields = ['id', 'name', 'description']

# class UserRoleSerializer(serializers.ModelSerializer):
#     user = UserSerializer()
#     role = RoleSerializer()

#     class Meta:
#         model = UserRole
#         fields = ['id', 'user', 'role']

from rest_framework import serializers 
from .models import * 
from django.contrib.auth import get_user_model 
User = get_user_model()

class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()

    def to_representation(self, instance):
        ret = super().to_representation(instance)
        ret.pop('password', None)
        return ret


class RegisterSerializer(serializers.ModelSerializer):
    class Meta: 
        model = User
        fields = ('id','email','password')
        extra_kwargs = { 'password': {'write_only':True}}
    
    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user

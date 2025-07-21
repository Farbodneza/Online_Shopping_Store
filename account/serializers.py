from rest_framework import serializers
from account.models import CustomUser


class CustomuserRegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'password', 'phone_number']
    def create(self, validated_data):
        user = CustomUser(
            username=validated_data['username'],
            email=validated_data['email'],
            phone_number = validated_data['phone_number']
            )
        user.set_password(validated_data['password'])
        user.save()
        return user
    
    def validate(self, attrs):
        if attrs["username"] == attrs["password"]:
            raise serializers.ValidationError('username and password should be deferent')
        return attrs
    
    
class CustomuserLoginSerializer(serializers.Serializer):
    username = serializers.CharField(required=True)
    password = serializers.CharField(required=True, write_only=True)


class OTPRequestSerializer(serializers.Serializer):
    email = serializers.EmailField()


class OTPVerifySerializer(serializers.Serializer):
    email = serializers.EmailField()    
    otp = serializers.CharField()


class CustomUserEditProfile(serializers.Serializer):
    bio = serializers.CharField(required=False)
    profile_picture = serializers.ImageField(required=False)
    username = serializers.CharField(required=False)
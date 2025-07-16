from rest_framework import serializers
from account.models import Customer


class CustomuserRegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = ['username', 'email', 'password']
    def create(self, validated_data):
        user = Customer(
            username=validated_data['username'],
            email=validated_data['email']
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

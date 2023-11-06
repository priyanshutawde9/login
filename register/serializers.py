from .models import  User
from rest_framework import serializers

class UserSerializer(serializers.ModelSerializer):
    username= serializers.CharField(required=True)
    email=serializers.EmailField(required=True)
    password = serializers.CharField(required=True)
    employee_id = serializers.CharField(required=True)

    class Meta:
        model= User
        fields =('username', 'password', 'email', 'employee_id') 
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def validate(self, data):
            username = data.get('username')
            password = data.get('password')
            email = data.get('email')
            employee_id = data.get('employee_id')

            if not username or not password:
                raise serializers.ValidationError("Username and password are required.")

            if User.objects.filter(username=username).exists():
                raise serializers.ValidationError("Username already exists. Please choose a different one.")

            if User.objects.filter(email=email).exists():
                raise serializers.ValidationError("Email address already exists. Please choose a different one.")

            if employee_id and User.objects.filter(employee_id=employee_id).exists():
                raise serializers.ValidationError("Employee ID already exists. Please choose a different one.")

            return data
    




from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from .serializers import UserSerializer
from django.contrib.auth import authenticate
from rest_framework import status
from rest_framework.permissions import IsAuthenticated 
from .models import User
from django.http import JsonResponse
from rest_framework_simplejwt.tokens import RefreshToken
import jwt
from django.conf import settings

def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)
    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }



@api_view(['POST'])
@permission_classes([IsAuthenticated])
def Registration(request):
   if request.method == 'POST':
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            # The serializer has validated the data
            validated_data = serializer.validated_data

            username = validated_data['username']
            password = validated_data['password']
            email = validated_data['email']
            employee_id = validated_data['employee_id']
            user = User.objects.create_user(username=username, password=password, email=email, employee_id=employee_id)
            if user:
                user_data = {
                    "username": username,
                    "password": password,
                    "email": email,
                    "employee_id": employee_id,
                }

                token = jwt.encode(user_data, settings.SECRET_KEY, algorithm="HS256")
                host_url = request.build_absolute_uri('/')[:-1]

                auto_login_link = f"{host_url}/login?token={token}"
                user.registration_token = token
                user.save()

                return Response({"auto_login_link": auto_login_link}, status=status.HTTP_201_CREATED)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        
@api_view(['POST','GET'])
def login_user(request):
        if request.method == 'POST':   
            req_data = request.data
         
            serializer = UserSerializer(data=req_data)
            if serializer.is_valid(raise_exception=True):
                username = request.data.get('username')
                password = request.data.get('password') 
            
                user = authenticate(request, username=username, password=password)

                if user:
                    token=get_tokens_for_user(user)
                    return JsonResponse({'token': token})
                else:
                    return JsonResponse({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)
            else:
                return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
        
        
        if request.method == "GET":
            token = request.query_params.get("token")

            if not token:
                return Response({"error": "Token missing"}, status=status.HTTP_400_BAD_REQUEST)

            
            # Decode the token and get the user data
            user_data = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
            username = user_data.get("username")
            password = user_data.get("password")

            user = User.objects.filter(username=username)
            if not user.exists():
                return Response("Invalid User", status=status.HTTP_404_NOT_FOUND)

            token = get_tokens_for_user(user[0])
            user_serializer = UserSerializer(user[0])  # Serialize the User object
            serialized_user = user_serializer.data  # Get the serialized data
            data = {"token": token, "user": serialized_user} 
            
            return Response(data, status=status.HTTP_200_OK)
        else:
            return JsonResponse({'error': 'user already exists'}, status=405)
        




from django.contrib.auth import authenticate
from django.contrib.auth.backends import ModelBackend
from django.contrib.auth.models import User
from django.http import JsonResponse
from rest_framework import status
from rest_framework.decorators import api_view, renderer_classes
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response

from api.models import UserProfile


@api_view(['POST'])
def register(request):
    username = request.data.get('username')
    password = request.data.get('password')
    email = request.data.get('email')
    preferred_language = request.data.get('preferred_language')
    skill_level = request.data.get('skill_level')

    if not username or not password:
        return Response({'error': 'Username and password are required.'}, status=status.HTTP_400_BAD_REQUEST)

    user = User.objects.create_user(
        username=username,
        password=password,
        email=email

    )

    # Create a new UserProfile instance linked to the User instance
    UserProfile.objects.create(
        user=user,
        preferred_language=preferred_language,
        skill_level=skill_level
    )

    return Response({'message': 'User registered successfully.'}, status=status.HTTP_201_CREATED)


@api_view(['POST'])
def login(request):
    email = request.data.get('email')
    password = request.data.get('password')

    print(email)
    print(password)

    if not email or not password:
        return Response({'error': 'Email and password are required.'}, status=status.HTTP_400_BAD_REQUEST)

    user = authenticate(email=email, password=password)

    if not user:
        return Response({'error': 'Invalid credentials.'}, status=status.HTTP_401_UNAUTHORIZED)

    # You can generate and return a token here if you're using token-based authentication.
    return Response({'message': 'Login successful.'})


class EmailBackend(ModelBackend):
    def authenticate(self, request, email=None, password=None, **kwargs):
        print(email)
        print(password)
        try:
            user = UserProfile.objects.get(email=email)
            if user.check_password(password):
                return user
        except UserProfile.DoesNotExist:
            return None

    def get_user(self, user_id):
        try:
            return UserProfile.objects.get(pk=user_id)
        except UserProfile.DoesNotExist:
            return None

    def get_users(self,):
        try:
            return UserProfile.objects.all()
        except UserProfile.DoesNotExist:
            return None


@api_view(['GET'])
@renderer_classes([JSONRenderer])
def get_registered_users(request):
    users = User.objects.all()
    user_list = []

    for user in users:
        try:
            user_profile = UserProfile.objects.get(user=user)
            user_data = {
                'username': user.username,
                'email': user.email,
                'preferred_language': user_profile.preferred_language,
                'skill_level': user_profile.skill_level
            }
            user_list.append(user_data)
        except UserProfile.DoesNotExist:
            pass

    return Response(user_list)


@api_view(['GET'])
def get_csrf_token(request):
    return JsonResponse({"csrfToken": request.COOKIES["csrftoken"]})

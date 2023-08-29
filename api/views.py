from django.contrib.auth import authenticate
from django.contrib.auth.backends import ModelBackend
from django.contrib.auth.models import User
from django.http import JsonResponse, HttpResponse
from rest_framework import status
from rest_framework.decorators import api_view, renderer_classes
from rest_framework.generics import get_object_or_404
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response

from api.models import UserProfile, SavedWord
from api.serializers import SavedWordSerializer


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

    response = HttpResponse("Logged in successfully")
    response.set_cookie('user_id_cookie', user.id)
    print('USER ID: ' + str(user.id))
    return response


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

    def get_users(self, ):
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
                'id': user.id,
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


@api_view(['GET', 'POST'])
def save_word(request, user_id, *args, **kwargs):
    user = get_object_or_404(User, id=user_id)

    if request.method == 'POST':
        serializer = SavedWordSerializer(data=request.data)
        if serializer.is_valid():
            saved_word = serializer.save(user=user)
            return Response({"message": "Word saved successfully.", "id": saved_word.id},
                            status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'GET':
        saved_words = SavedWord.objects.filter(user=user)
        serializer = SavedWordSerializer(saved_words, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['GET'])
def get_profile(request):
    try:
        cookie = request.COOKIES['user_id_cookie']

        if cookie:
            return JsonResponse({"cookie_name": cookie})
        else:
            return JsonResponse({"cookie_name": "UNAVAILABLE"})

    except:
        return JsonResponse({"cookie_name": "UNAVAILABLE"})


@api_view(['GET'])
def get_cookie(request):
    try:
        cookie = request.COOKIES['cookie_name']

        if cookie:
            return JsonResponse({"cookie_name": cookie})
        else:
            return JsonResponse({"cookie_name": "UNAVAILABLE"})

    except:
        return JsonResponse({"cookie_name": "UNAVAILABLE"})


@api_view(['POST'])
def set_cookie(request, user_id):
    response = HttpResponse("Setting the cookie")
    response.set_cookie('cookie_name', 'cookie_value: ' + str(user_id))
    return response

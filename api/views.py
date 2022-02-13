from rest_framework import status
from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response

from api.helper import get_user_from_db, create_user_in_db, get_filtered_logs_from_db


@api_view(['POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAdminUser])
def register(request):
    """Регистрация нового пользователя, доступна только администраторам"""
    if ('username' or 'password') not in request.data:
        return Response({'status': 'error', 'description': 'missing parameters'}, status=status.HTTP_400_BAD_REQUEST)
    user = create_user_in_db(request)
    if not user:
        return Response({'status': 'error', 'description': 'not unique username'}, status=status.HTTP_404_NOT_FOUND)
    token, created = Token.objects.get_or_create(user=user)
    return Response({'status': 'success', 'token': token.key, 'username': user.username}, status=status.HTTP_201_CREATED)


@api_view(['POST'])
def get_token(request):
    """Получения токена, зарегистрированного пользователя"""
    if ('username' or 'password') not in request.data:
        return Response({'status': 'error', 'description': 'missing parameters'}, status=status.HTTP_400_BAD_REQUEST)
    user = get_user_from_db(request)
    if not user:
        return Response({'status': 'error', 'description': 'not found'}, status=status.HTTP_404_NOT_FOUND)
    token, created = Token.objects.get_or_create(user=user)
    return Response({'status': 'success', 'token': token.key, 'username': user.username}, status=status.HTTP_200_OK)


@api_view(['POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def get_logs(request):
    """Получения логов, согласно параметрам запроса"""
    logs = get_filtered_logs_from_db(request)
    return Response({'status': 'success', 'data': logs}, status=status.HTTP_200_OK)



from rest_framework import generics
from rest_framework import status
from rest_framework.response import Response
from api.account.serializers import LoginEUSerializer,RefreshTokenSerializer,UserDetailSerializer
from drf_yasg.utils import swagger_auto_schema
from utils.constant import *
from apps.account import service as account_service
from api.messages import*
from utils.common import dispatch_response,get_cookies
import jwt 
from apps.account.models import Account
# Create your views here

class LoginEU(generics.GenericAPIView):
    allowed_methods = ("POST",)
    serializer_class = LoginEUSerializer

    @swagger_auto_schema(
        operation_description="\
            <b>Username: </b> <a style='text-decoration:none !important; color:black; pointer-events:none;'>admin@addnectar.com </a> <br><br> \
            <b>Pasword: </b> Add@2023",
        
        tags=[API_AUTH]
    )

    def post(self, request):
        serializer = LoginEUSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        data = serializer.validated_data
        res = account_service.login_eu(data['username'], data['password'])
        return dispatch_response(res)
    
class RefreshTokenEU(generics.GenericAPIView):
    allowed_methods = ("POST",)
    serializer_class = RefreshTokenSerializer
    @swagger_auto_schema(
        operation_description="\
            <b>Note: </b> it will return refresh token & access token",
        tags=[API_AUTH]
    )

    def post(self, request):
        serializer = RefreshTokenSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        data = serializer.data
        res = account_service.refresh_token_eu(data['refresh'])
        return dispatch_response(res)
    

class LogoutEU(generics.GenericAPIView):
    allowed_methods = ("POST",)
    #permission_classes = (IsAuthenticated, )
    serializer_class = RefreshTokenSerializer
    @swagger_auto_schema(
        operation_description="\
            <b>Note: </b> It will clean player id and blacklist refresh token",
        tags=[API_AUTH]
    )
    def post(self, request):
        serializer = RefreshTokenSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        data = serializer.data
        res = account_service.logout_eu(data['refresh'])
        return dispatch_response(res)


class CommonUserMixins:
    def get_user(self, request):
        access_token, refresh_token = get_cookies(request)
        if access_token:
            try:
                decoded_token = jwt.decode(access_token, algorithms=['HS256'], options={"verify_signature": False})
                user_id = decoded_token['user_id']
                user_obj = Account.objects.filter(id =user_id).first()
                return user_obj
            except jwt.ExpiredSignatureError:
                
                pass
            except jwt.DecodeError:
              
                pass
            except jwt.InvalidTokenError:
                pass
        return None




        




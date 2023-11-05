import os,json
from .models import Account
from rest_framework_simplejwt.tokens import  RefreshToken
from api.account.serializers import UserDetailSerializer
from datetime import datetime,timezone
from django.db.models import Q
from django.conf import settings
from dotenv import load_dotenv
from utils.common import makePostCall
load_dotenv()
env = os.getenv

def get_tokens_for_user(user):
    try:
        refresh = RefreshToken.for_user(user)

        return {
            'refresh': refresh,
            'access': refresh.access_token,
        }
    except:
        return 1005
def refresh_token_eu(token):
    try:
        refresh = RefreshToken(token)
        return {
            'refresh_token': str(refresh),
            'access_token': str(refresh.access_token),
        }
    except:
        return 1005
def login_eu(username, password):
    try:
        username = username.lower()
        #User can login either from their email or mobile
        user = Account.objects.get(username=username)
        
        if not user:
            return 1004
        
        if not user.is_active:
            return 1001

        if not user.check_password(password):
            return 1004

        #JWT authorization
        jwt_response = get_tokens_for_user(user)

        if not jwt_response:
            return 1003              

        else:  
            user_detail_serializer = UserDetailSerializer(user)
            #add prefix to the generated jwt token values
            bearer_token = {key: f"{settings.AUTH_PREFIX} {val}" for key, val in jwt_response.items()}
            user.last_login = datetime.now().replace(tzinfo=timezone.utc)
            user.save()
            return {
                        'token': bearer_token,
                        'data' : user_detail_serializer.data,
                    }

    except Account.DoesNotExist:
        return 1004
    

def call_refresh_api(data):
    base_url=env('BASE_URL') + 'accounts/refresh/'
    payload = json.dumps(data)
    res = makePostCall(base_url,payload)
    status_code = res.status_code
    if status_code == 500:
        return "Oops! something went wrong"
    
    elif status_code != 200:
        msg = json.loads(res.text)
        return msg['msg']
    
    elif status_code == 200:
        data = json.loads(res.text)
        return data
    return ""

def logout_eu(token):
    try:
        refresh = RefreshToken(token)
        refresh.blacklist()
        return 4000
    except Exception as e:
        print(e)
        return 4000
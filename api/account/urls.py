from django.urls import path
from api.account import views as api_account_view
urlpatterns = [
    path('login/', api_account_view.LoginEU.as_view(), name='auth_login'),
    path('refresh/', api_account_view.RefreshTokenEU.as_view(), name='refresh'),
    path('logout/', api_account_view.LogoutEU.as_view(), name='logout'),
]
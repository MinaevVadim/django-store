from django.urls import path

from app_users.views import AccountList, LoginUserView, RegisterList, UpdatePassword, \
    restore_password, logout_function, update_user_profile

urlpatterns = [
    path('account/', AccountList.as_view(), name='account'),
    path('registration/', RegisterList.as_view(), name='register_user'),
    path('login/', LoginUserView.as_view(), name='login_user'),
    path('logout/', logout_function, name='logout'),
    path('profile/', update_user_profile, name='profile'),
    path('change_password/', UpdatePassword.as_view(), name='change_password'),
    path('restore_password/', restore_password, name='restore_password'),
]

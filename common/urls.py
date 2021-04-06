from django.urls import path
from django.contrib.auth import views as auth_views

#네임 스페이스
from common import views

app_name = 'common'

urlpatterns = [
    #LoginView는 registration이라는 템플릿 디렉터리에서 login.html 파일을 찾는다.
    #->common 디렉터리에 로그인/로그아웃 기능을 구현하여야 하므로, as_view 함수에 원하는 경로를 지정한 template_name 인자를 넣어준다.
    path('login/', auth_views.LoginView.as_view(template_name='common/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('signup/', views.signup, name='signup'),
]
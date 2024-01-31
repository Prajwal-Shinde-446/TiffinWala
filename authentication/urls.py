from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.home, name="home"),
    path('login/', views.login, name="login"),
    path('signup/',views.Register , name="Register"),
    path('verify-otp/<int:user_id>/', views.verify_otp, name='verify_otp'),


]+ static(settings.MEDIA_URL,document_root = settings.MEDIA_ROOT)
from django.urls import path
from . import views
from django.contrib.auth.views import LoginView, LogoutView
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [path('register', views.register, name='register'),
               path('logout', LogoutView.as_view(), name='logout'),
               path('login', LoginView.as_view(template_name='login.html'), name='login'),
               path('', views.index, name='index'),
               path('pic<str:pk>', views.edit_image, name='edit_image'),
               path('delete<str:pk>', views.delete_image, name='delete_image'),]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
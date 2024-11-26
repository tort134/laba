from django.urls import path, include
from .views import user_login, user_logout, register, survey_list, vote
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('login/', user_login, name='login'),
    path('logout/', user_logout, name='logout'),
    path('register/', register, name='register'),
    path('survey_list', survey_list, name='survey_list'),
    path('<int:survey_id>/', vote, name='vote'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

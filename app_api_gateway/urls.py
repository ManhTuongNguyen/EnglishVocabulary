from django.urls import path, include
from rest_framework.routers import DefaultRouter

from app_authentication.views import CustomTokenView, RegisterView
from app_translate.views import Translate
from app_vocabulary.views import EnglishVocabularyViewSet

router = DefaultRouter()

router.register('vocabulary', EnglishVocabularyViewSet, basename='vocabulary')
router.register('register', RegisterView, basename='register')

urlpatterns = [
    path('o/token/', CustomTokenView.as_view(), name='token'),
    path('o/', include('oauth2_provider.urls', namespace='oauth2_provider')),
    path('translate/', Translate.as_view(), name='translate'),
]

urlpatterns += router.urls

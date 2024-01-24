from django.urls import path, include
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView, SpectacularRedocView
from rest_framework.routers import DefaultRouter

from app_authentication.views import RegisterView, CustomTokenView
from app_translate.views import Translate
from app_vocabulary.views import EnglishVocabularyViewSet

router = DefaultRouter()

router.register('vocabulary', EnglishVocabularyViewSet, basename='vocabulary')
router.register('register', RegisterView, basename='register')

urlpatterns = [
    path('o/token/', CustomTokenView.as_view(), name='token'),
    path('o/', include('oauth2_provider.urls', namespace='oauth2_provider')),
    path('schema/', SpectacularAPIView.as_view(), name='schema'),
    # Optional UI:
    path('schema/swagger-ui/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('schema/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
    path('translate/', Translate.as_view(), name='translate'),
]

urlpatterns += router.urls

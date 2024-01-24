from rest_framework.routers import DefaultRouter

from app_authentication.views import RegisterView
from app_vocabulary.views import EnglishVocabularyViewSet

router = DefaultRouter()

router.register('vocabulary', EnglishVocabularyViewSet, basename='vocabulary')
router.register('register', RegisterView, basename='register')

urlpatterns = router.urls

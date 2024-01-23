from django.contrib.auth.models import User
from django.utils.decorators import method_decorator
from django.views.decorators.debug import sensitive_post_parameters
from drf_spectacular.utils import extend_schema
from oauth2_provider.views import TokenView
from rest_framework import generics
from rest_framework.permissions import AllowAny
from rest_framework.viewsets import ViewSet

from Vocabulary.settings import O2AuthClient
from app_authentication.serializers import RegisterSerializer


class CustomTokenView(TokenView):
    @method_decorator(sensitive_post_parameters("password"))
    def post(self, request, *args, **kwargs):
        data = request.POST.copy()
        if not data.get('client_id') or not data.get('client_secret'):
            data['client_id'] = O2AuthClient['client_id']
            data['client_secret'] = O2AuthClient['client_secret']
        if not data.get('grant_type'):
            data['grant_type'] = 'password'
        request.POST = data
        return super().post(request, *args, **kwargs)


@extend_schema(tags=['Register'], operation_id='register')
class RegisterView(generics.CreateAPIView, ViewSet):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = [AllowAny]

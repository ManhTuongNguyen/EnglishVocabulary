from django.contrib.auth.models import User
from django.utils.decorators import method_decorator
from django.views.decorators.debug import sensitive_post_parameters
from drf_spectacular.utils import extend_schema, inline_serializer, OpenApiResponse
from oauth2_provider.views import TokenView
from rest_framework import generics, serializers
from rest_framework.permissions import AllowAny
from rest_framework.views import APIView
from rest_framework.viewsets import ViewSet

from Vocabulary.settings import O2AuthClient
from app_authentication.serializers import RegisterSerializer


@extend_schema(tags=['Token'], operation_id='token')
class CustomTokenView(TokenView, APIView):
    @method_decorator(sensitive_post_parameters("password"))
    @extend_schema(
        request=inline_serializer(
            name="InlineTokenSerializer",
            fields={
                "username": serializers.CharField(required=False),
                "password": serializers.CharField(required=False),
                "refresh_token": serializers.CharField(required=False),
                "grant_type": serializers.CharField(required=False, default="password",
                                                    help_text="Example: password, refresh_token"),
                "client_id": serializers.CharField(required=False, help_text='Nullable'),
                "client_secret": serializers.CharField(required=False, help_text='Nullable'),
            },
        ),
        responses={
            200: inline_serializer(
                name='TokenSerializer',
                fields={
                    'access_token': serializers.CharField(),
                    'expires_in': serializers.IntegerField(),
                    'token_type': serializers.CharField(),
                    'scope': serializers.CharField(),
                    'refresh_token': serializers.CharField(),
                }
            ),
            400: OpenApiResponse(),
        },
        description='Get token using username and password or refresh_token',
    )
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

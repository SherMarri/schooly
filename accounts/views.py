from rest_auth.registration.serializers import VerifyEmailSerializer
from rest_auth.registration.views import APIView, ConfirmEmailView
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from allauth.socialaccount.providers.facebook.views import FacebookOAuth2Adapter
from allauth.socialaccount.providers.google.views import GoogleOAuth2Adapter
from rest_auth.registration.views import SocialLoginView
from django.shortcuts import render

class CustomVerifyEmailView(APIView, ConfirmEmailView):
    permission_classes = (AllowAny,)
    allowed_methods = ('POST', 'OPTIONS', 'HEAD')

    def get_serializer(self, *args, **kwargs):
        return VerifyEmailSerializer(*args, **kwargs)

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            self.kwargs['key'] = serializer.validated_data['key']
        confirmation = self.get_object()
        confirmation.confirm(self.request)
        return Response({'result': 'Email address has been successfully verified.'}, status=status.HTTP_200_OK)


class FacebookLoginView(SocialLoginView):
    """
    View for providing social login using Facebook OAuth2
    """
    adapter_class = FacebookOAuth2Adapter


class GoogleLoginView(SocialLoginView):
    """
    View for providing social login using Facebook OAuth2
    """
    adapter_class = GoogleOAuth2Adapter


def social_login(request):
    return render(request,'account/social_login.html')


def reset_password_form(request, uidb64, token):
    context = {
        'uid': uidb64,
        'token': token
    }
    return render(request,'account/password_reset_form.html', context=context)

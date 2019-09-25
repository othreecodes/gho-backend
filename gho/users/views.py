from rest_framework import viewsets, mixins
from rest_framework.permissions import AllowAny
from .models import User, NewUserPhoneVerification
from .permissions import IsUserOrReadOnly
from .serializers import CreateUserSerializer, UserSerializer, SendNewPhonenumberSerializer
from rest_framework.views import APIView

class UserViewSet(mixins.RetrieveModelMixin,
                  mixins.UpdateModelMixin,
                  viewsets.GenericViewSet):
    """
    Updates and retrieves user accounts
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (IsUserOrReadOnly,)


class UserCreateViewSet(mixins.CreateModelMixin,
                        viewsets.GenericViewSet):
    """
    Creates user accounts
    """
    queryset = User.objects.all()
    serializer_class = CreateUserSerializer
    permission_classes = (AllowAny,)


class SendNewPhonenumberVerifyViewSet(mixins.CreateModelMixin,viewsets.GenericViewSet):

    """
    Sending of verification code
    """
    queryset = NewUserPhoneVerification.objects.all()
    serializer_class = SendNewPhonenumberSerializer
    permission_classes = (AllowAny,)

class VerifySignUpVerificationCodeView(APIView):

    """
    Verify Sign up code
    """
    permission_classes = (AllowAny,)

    def post(self, request, format=None):
        phone_number = request.data.get("phone_number", None)
        code = request.data.get("code", None)
        
        
        pass
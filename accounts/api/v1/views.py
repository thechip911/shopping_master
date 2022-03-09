from django.contrib.auth import get_user_model
from django.db.models import Q
from django.shortcuts import get_object_or_404
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.status import (
    HTTP_200_OK,
    HTTP_201_CREATED,
    HTTP_400_BAD_REQUEST,
    HTTP_403_FORBIDDEN,
    HTTP_404_NOT_FOUND,
)
from rest_framework.viewsets import ModelViewSet
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView

from accounts.api.v1.serializers import UserModelSerializer, ProfileUpdateModelSerializer
from core_libs.messages import ERROR_MESSAGES, MAIL_SUBJECTS, SUCCESS_MESSAGES
from core_libs.template_names import PASSWORD_RESET_TEMPLATE
from core_libs.utils import send_email

User = get_user_model()


class UserViewSet(ModelViewSet):
    serializer_class = UserModelSerializer

    def get_queryset(self) -> Response:
        if self.request.user.is_authenticated and self.request.user.is_superuser:
            queryset = User.objects.all()
        elif self.request.user.is_authenticated:
            queryset = User.objects.filter(id=self.request.user.id)
        else:
            queryset = User.objects.none()

        if self.request.GET.get("first_name"):
            first_name = self.request.GET.get("first_name")
            queryset = queryset.filter(first_name__istartswith=first_name)

        if self.request.GET.get("last_name"):
            last_name = self.request.GET.get("last_name")
            queryset = queryset.filter(last_name__istartswith=last_name)

        if self.request.GET.get("mobile_number"):
            mobile_number = self.request.GET.get("mobile_number")
            queryset = queryset.filter(mobile_number__istartswith=mobile_number)

        if self.request.GET.get("email"):
            email = self.request.GET.get("email")
            queryset = queryset.filter(email__istartswith=email)

        query = self.request.GET.get("q")
        if query:
            queryset = queryset.filter(
                Q(first_name__icontains=query) | Q(last_name__icontains=query) | Q(email__icontains=query)
            )

        return queryset

    def get_permissions(self) -> list:
        if self.request.method == "POST":
            self.permission_classes = [AllowAny]
        return super().get_permissions()

    def get_object(self) -> object:
        queryset = self.get_queryset()
        obj = get_object_or_404(queryset, id=self.request.user.id)
        return obj

    @action(detail=False, methods=["get"])
    def login(self, request) -> Response:
        if self.request.user.is_authenticated:
            user_detail = self.serializer_class(self.request.user, context={"request": request}).data
            return Response(data={"data": user_detail}, status=HTTP_200_OK)
        return Response(
            data={"data": ERROR_MESSAGES["USER_NOT_AUTHENTICATED"]},
            status=HTTP_403_FORBIDDEN,
        )

    @action(detail=False, methods=["post"])
    def signup(self, request, *args, **kwargs) -> Response:
        super(UserViewSet, self).create(request, *args, **kwargs)
        return Response({"data": SUCCESS_MESSAGES["ACCOUNT_CREATED"]}, status=HTTP_201_CREATED)

    @action(detail=False, methods=["patch"])
    def change_password(self, request, *args, **kwargs) -> Response:
        if self.request.user.is_authenticated:
            super(UserViewSet, self).update(request, *args, **kwargs)
            return Response({"data": SUCCESS_MESSAGES["PASSWORD_CHANGED"]}, status=HTTP_200_OK)
        return Response(
            data={"data": ERROR_MESSAGES["USER_NOT_AUTHENTICATED"]},
            status=HTTP_403_FORBIDDEN,
        )


class ProfileUpdateModelViewSet(ModelViewSet):
    serializer_class = ProfileUpdateModelSerializer
    http_method_names = ["patch", "delete"]

    def get_queryset(self) -> Response:
        queryset = User.objects.none()
        if self.request.user.is_authenticated:
            queryset = User.objects.filter(id=self.request.user.id)
        return queryset


class ResetPassword(TokenObtainPairView):
    def get_tokens_for_user(self, user_obj):
        refresh = RefreshToken.for_user(user_obj)
        access_token = str(refresh.access_token)
        return access_token

    def post(self, request, *args, **kwargs) -> Response:
        template_name = PASSWORD_RESET_TEMPLATE
        email = request.data.get("email")
        user_obj = User.objects.filter(email=email).first()
        if not email:
            return Response(
                data={"data": ERROR_MESSAGES["ENTER_EMAIL"]},
                status=HTTP_400_BAD_REQUEST,
            )
        if email and user_obj:
            token = self.get_tokens_for_user(user_obj)
            send_email(
                email=email,
                template_name=template_name,
                data=token,
                subject=MAIL_SUBJECTS["RESET_PASSWORD_MAIL"],
            )
            return Response(
                data={"data": SUCCESS_MESSAGES["PASSWORD_RESET_MAIL_SENT"]},
                status=HTTP_200_OK,
            )
        return Response(
            data={"data": ERROR_MESSAGES["USER_NOT_FOUND"]},
            status=HTTP_404_NOT_FOUND,
        )

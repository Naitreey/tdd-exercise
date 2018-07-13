from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import default_token_generator


UserModel = get_user_model()


class TokenBackend:

    def get_user(self, user_id):
        try:
            return UserModel.objects.get(pk=user_id)
        except UserModel.DoesNotExist:
            return None

    def authenticate(self, request, uidb64=None, token=None):
        if uidb64 is None or token is None:
            return None
        try:
            user = UserModel.objects.get_by_uidb64(uidb64)
        except (TypeError, ValueError, OverflowError, UserModel.DoesNotExist):
            return None
        if default_token_generator.check_token(user, token):
            return user
        return None

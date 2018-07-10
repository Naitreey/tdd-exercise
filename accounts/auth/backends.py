from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import default_token_generator


UserModel = get_user_model()


class TokenBackend:

    token_generator = default_token_generator

    def get_user(self, user_id):
        try:
            user = UserModel._default_manager.get(pk=user_id)
        except UserModel.DoesNotExist:
            return None
        else:
            return user

    def authenticate(self, request, uidb64, token):
        try:
            user = UserModel._default_manager.get_by_uidb64(uidb64)
        except UserModel.DoesNotExist:
            pass
        else:
            if token_generator.check_token(user, token):
                return user
        return None

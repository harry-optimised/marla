from django.contrib.auth.backends import BaseBackend
from your_app.models import User, LoginCode


class EmailCodeBackend(BaseBackend):
    def authenticate(self, request, email=None, code=None, **kwargs):
        try:
            user = User.objects.get(email=email)
            login_code = LoginCode.objects.filter(
                user=user, code=code, is_used=False
            ).latest("created_at")
            if login_code:
                return user
        except User.DoesNotExist:
            return None
        except LoginCode.DoesNotExist:
            return None

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None

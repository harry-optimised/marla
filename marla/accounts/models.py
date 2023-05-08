from django.db import models
from django.contrib.auth.models import User, AbstractUser


class User(AbstractUser):
    api_key = models.UUIDField(null=False, blank=False, unique=True)
    is_premium = models.BooleanField(default=False)
    remaining_questions = models.IntegerField(default=10)
    stripe_customer_id = models.CharField(max_length=50, blank=True, null=True)

    def has_quota(self):
        if self.is_premium:
            return True
        return self.remaining_questions > 0

    def use_quota(self):
        if self.is_premium:
            return
        self.remaining_questions -= 1
        self.save()


class LoginCode(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    code = models.CharField(max_length=6)
    created_at = models.DateTimeField(auto_now_add=True)
    is_used = models.BooleanField(default=False)

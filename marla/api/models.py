from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class Context(models.Model):
    api_key = models.UUIDField()
    content = models.TextField()
    chatbot_name = models.CharField(max_length=255, default="Marla")
    business_name = models.CharField(max_length=255, default="Business")
    tone_of_voice = models.CharField(max_length=255, default="polite & curteous")

    def get_user(self):
        return User.objects.get(api_key=self.api_key)

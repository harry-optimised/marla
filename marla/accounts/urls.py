from django.urls import path
from .views import (
    SendLoginCodeView,
    ValidateLoginCodeView,
    create_checkout_session,
    stripe_webhook,
    cancel_subscription,
)

urlpatterns = [
    path("send_login_code/", SendLoginCodeView.as_view(), name="send_login_code"),
    path(
        "validate_login_code/",
        ValidateLoginCodeView.as_view(),
        name="validate_login_code",
    ),
    path(
        "create-checkout-session/",
        create_checkout_session,
        name="create_checkout_session",
    ),
    path("stripe-webhook/", stripe_webhook, name="stripe_webhook"),
    path("cancel-subscription/", cancel_subscription, name="cancel_subscription"),
]

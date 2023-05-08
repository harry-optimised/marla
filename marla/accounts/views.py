import stripe
import random
from django.contrib.auth import login
from django.core.mail import send_mail
from django.http import JsonResponse
from django.views import View
from .models import LoginCode
from uuid import uuid4
from api.models import Context
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from pathlib import Path

from django.contrib.auth import get_user_model

User = get_user_model()


class SendLoginCodeView(View):
    def post(self, request):
        email = request.POST.get("email")

        # If user doesn't exist, create.
        if not User.objects.filter(email=email).exists():
            api_key = uuid4()
            User.objects.create_user(
                email=email,
                username=email,
                api_key=api_key,
                is_staff=True,
                is_superuser=True,
            )
            # Create a default context for the user.
            default = Path(__file__).resolve().parent / "default_context.txt"
            content = open(str(default), "r").read()
            Context.objects.create(api_key=api_key, content=content)

        user = User.objects.get(email=email)
        code = f"{random.randint(100000, 999999)}"
        LoginCode.objects.create(user=user, code=code)

        # Send the login code to the user's email address
        # send_mail(
        #    "Your Login Code",
        #    f"Your login code is: {code}",
        #    "no-reply@example.com",
        #    [email],
        #    fail_silently=False,
        # )

        print(code)
        return JsonResponse({"status": "ok"})


class ValidateLoginCodeView(View):
    def post(self, request):
        email = request.POST.get("email")
        code = request.POST.get("code")

        try:
            user = User.objects.get(email=email)
            login_code = LoginCode.objects.filter(
                user=user, code=code, is_used=False
            ).latest("created_at")

            if login_code:
                login(request, user)
                login_code.is_used = True
                login_code.save()
                return JsonResponse({"status": "ok"})

        except User.DoesNotExist:
            pass
        except LoginCode.DoesNotExist:
            pass

        return JsonResponse({"status": "error"})


stripe.api_key = settings.STRIPE_SECRET_KEY


@csrf_exempt
def create_checkout_session(request):
    if request.method == "POST":
        try:
            checkout_session = stripe.checkout.Session.create(
                payment_method_types=["card"],
                line_items=[
                    {
                        "price": "price_1N5WAIH451kFmPn75SKLXlOS",
                        "quantity": 1,
                    }
                ],
                mode="subscription",
                success_url="http://localhost:8000/account/",
                cancel_url="http://localhost:8000/account/",
            )
            print(checkout_session.id)
            return JsonResponse({"sessionId": checkout_session.id})
        except Exception as e:
            print(e)
            return JsonResponse({"error": str(e)})


@csrf_exempt
@require_POST
def stripe_webhook(request):
    payload = request.body
    sig_header = request.META.get("HTTP_STRIPE_SIGNATURE")

    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, settings.STRIPE_WEBHOOK_SECRET
        )
    except ValueError:
        return HttpResponse(status=400)
    except stripe.error.SignatureVerificationError:
        return HttpResponse(status=400)

    if event.type == "checkout.session.completed":
        session = event.data.object
        user = User.objects.get(email=session.customer_details.email)
        user.is_premium = True
        user.stripe_customer_id = session.customer
        user.save()
    elif event.type == "customer.subscription.deleted":
        subscription = event.data.object
        customer = stripe.Customer.retrieve(subscription.customer)
        user = User.objects.get(email=customer.email)
        user.is_premium = False
        user.save()

    return HttpResponse(status=200)


@login_required
def cancel_subscription(request):
    if request.user.is_premium and request.user.stripe_customer_id:
        subscriptions = stripe.Subscription.list(
            customer=request.user.stripe_customer_id
        )

        if subscriptions.data:
            subscription = subscriptions.data[0]
            stripe.Subscription.delete(subscription.id)
            request.user.is_premium = False
            request.user.save()
            redirect("accounts")
        else:
            redirect("accounts")
    else:
        redirect("accounts")
    return redirect("accounts")

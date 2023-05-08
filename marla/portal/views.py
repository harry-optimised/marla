from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from api.models import Context


def home(request):
    return render(request, "home.html")


@login_required(login_url="/")
def settings(request):
    context = Context.objects.get(api_key=request.user.api_key)
    return render(request, "settings.html", {"user": request.user, "context": context})


@login_required(login_url="/")
def account(request):
    max_questions = 10
    remaining_questions = request.user.remaining_questions
    return render(
        request,
        "account.html",
        {"max_questions": max_questions, "remaining_questions": remaining_questions},
    )


@login_required(login_url="/")
def integrations(request):
    return render(
        request,
        "integrations.html",
    )

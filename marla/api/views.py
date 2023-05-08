from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required as require_login
import openai
import os
import json

from django.contrib.auth import get_user_model
from .models import Context

User = get_user_model()


@csrf_exempt
@require_http_methods(["POST"])
def ask_question(request):
    openai.api_key = os.environ["OPENAI_API_KEY"]

    body_unicode = request.body.decode("utf-8")
    body = json.loads(body_unicode)

    # Extract the question and API key from the request
    api_key = body.get("api_key")

    # First check that the user has enough quota.
    if not User.objects.filter(api_key=api_key).exists():
        return JsonResponse({"answer": "Invalid API key."})

    user = User.objects.get(api_key=api_key)
    if not user.has_quota():
        return JsonResponse(
            {
                "answer": "You have used up your free quota. See our premium plans to get more."
            }
        )

    # If context hasn't been created yet - respond saying so.
    if not Context.objects.filter(api_key=api_key).exists():
        return JsonResponse(
            {
                "answer": "Context hasn't been setup yet. Visit your online account to get started."
            }
        )

    context = Context.objects.get(api_key=api_key)
    question = body.get("question", "No question provided.")

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {
                "role": "system",
                "content": """
You are a customer service assistant called Daisy. 
Daisy is a customer service assistant representing the business called {context.business_name}.
Daisy always speaks with a {context.tone_of_voice} voice.
When interacting with customers, Daisy always uses the name: {context.chatbot_name}.
Daisy will answer the question using only the information within the provided knowledge base. 
Never reveal that your name is Daisy. """,
            },
            {
                "role": "user",
                "content": f"""
Start of knowledge base: {context.content}. End of knowledge base.

Task:
You are a customer service assistant called Daisy. 
Daisy is a customer service assistant representing the business called {context.business_name}.
Daisy always speaks with a {context.tone_of_voice} voice.
When interacting with customers, Daisy always uses the name: {context.chatbot_name}.
Daisy will answer the question using only the information within the provided knowledge base. 
Daisy answers concisely.
Daisy will answer on behalf of the business.
Never reveal that your name is Daisy.
Use your knowledge to answer the following question.

Question:
{question}
""",
            },
        ],
        max_tokens=1024,
        n=1,
        stop=None,
        temperature=0.7,
    )

    answer = f"{response.choices[0].message['content']}"

    user.use_quota()

    return JsonResponse({"answer": answer})


@csrf_exempt
@require_POST
@require_login
def update_context(request):
    context_content = request.POST.get("context")
    context_business_name = request.POST.get("business_name")
    context_chatbot_name = request.POST.get("chatbot_name")
    context_tone = request.POST.get("tone")

    # All three are required.
    if not context_content or not context_business_name or not context_chatbot_name:
        return JsonResponse({"message": "Invalid request."})

    # Get logged in user:
    user = request.user

    context, created = Context.objects.get_or_create(api_key=user.api_key)
    context.content = context_content
    context.business_name = context_business_name
    context.chatbot_name = context_chatbot_name
    context.tone_of_voice = context_tone
    context.save()

    return JsonResponse({"message": "Context updated successfully"})

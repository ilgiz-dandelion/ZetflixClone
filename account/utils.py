from django.core.mail import send_mail
from zetflix_api._celery import app


@app.task
def send_activation_code(email, activation_code):

    message = f"""Спасибо за регистрацию.Активируйте свой аккаунт по ссылке:
    http://127.0.0.1:8000/api/v1/account/activation/{activation_code}"""
    send_mail(
        'Активация аккаунта',
        message,
        'test@myproject.com',
        [email, ],
        fail_silently=False
    )
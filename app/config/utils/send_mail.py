from django.core.mail import send_mail
from django.contrib.auth.models import User

from config import settings


def send_activation_mail(user):
    
    html_msg = '''
        <h1> Welcome {} </h1>
        <br>
        Thanks for signing in silicon robot!! Click
        <a href='{}'> here </a> to activate your
        account.
        <br>
        Patrick Concepcion
        <br>
        Developer
    '''.format(
        user.first_name or user.username,
        'http://localhost:8000/api/users/{}/activate'.format(user.id),
    )

    send_mail(
        'Silicon Robot Account Activation',
        message='',
        html_message=html_msg,
        from_email=settings.EMAIL_HOST_USER,
        recipient_list=[user.email],
        fail_silently=False)

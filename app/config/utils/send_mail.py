from django.core.mail import send_mail
from django.contrib.auth.models import User

from config import settings


def send_activation_mail(token):
    activation_link = ('http://localhost:8000/' +
        'api/users/{}/activate?temp={}'.format
        (token.user.id, token.token)
    )
    
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
        token.user.first_name or token.user.username,
        activation_link
    )

    send_mail(
        'Silicon Robot Account Activation',
        message='',
        html_message=html_msg,
        from_email=settings.EMAIL_HOST_USER,
        recipient_list=[token.user.email],
        fail_silently=False)

from django.core.mail import EmailMultiAlternatives
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.contrib.auth.tokens import default_token_generator
from django.contrib.sites.shortcuts import get_current_site
from .models import User


def update_user(*, user, **user_data):
    for attr, value in user_data.items():
        setattr(user, attr, value)
    user.save()
    return user


def encode_uid(pk):
    return force_str(urlsafe_base64_encode(force_bytes(pk)))


def decode_uid(pk):
    return force_str(urlsafe_base64_decode(pk))

def get_reset_password_url(request, user):
    site = get_current_site(request)
    protocol = 'https' if request.is_secure() else 'http'
    domain = site.domain
    uid = encode_uid(user.pk)
    token = default_token_generator.make_token(user)
    return f'{protocol}://{domain}/reset/{uid}/{token}'


def send_reset_password_email(request, user):
    recipient = user.email
    subject, from_email, to = recipient, 'admin@example.com', recipient
    reset_password_url = get_reset_password_url(request=request, user=user)

    text_content = f'You can reset password here {reset_password_url}'
    html_content = f'<p>You can reset password <a href="{reset_password_url}">here</a></p>'
    
    msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
    msg.attach_alternative(html_content, "text/html")
    msg.send()

from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.conf import settings

def send_verification_email(user, request):
    token = default_token_generator.make_token(user)
    uid = urlsafe_base64_encode(force_bytes(user.pk))
    current_site = request.get_host()
    link = f"http://{current_site}/users/verify-email/{uid}/{token}/"

    subject = "Verify your email"
    message = f"Hi {user.username}, click the link to verify your email: {link}"
    send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [user.email])
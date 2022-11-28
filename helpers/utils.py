from django.core.mail import EmailMessage

from applications.models import ApplicationEmail
from job_star import settings


def send_application_success_mail(recipient):
    try:
        email = ApplicationEmail.objects.get(
            type__iexact='completed_application'
        )
        subject = email.subject
        message = f"{email.salutation} {recipient.first_name},\n {email.body}"

        mail = EmailMessage(
            subject,
            message,
            to=[recipient.email],
            from_email=settings.EMAIL_HOST_USER
        )
        status = mail.send()
        # print("Mail status:", status)
    except ApplicationEmail.DoesNotExist:
        pass
    return


def send_application_shortlisted_mail(recipient):
    try:
        email = ApplicationEmail.objects.get(
            type__iexact='shortlisted'
        )
        subject = email.subject
        message = f"{email.salutation} {recipient.first_name},\n {email.body}"

        mail = EmailMessage(
            subject,
            message,
            to=[recipient.email],
            from_email=settings.EMAIL_HOST_USER
        )
        status = mail.send()
        # print("Mail status:", status)
    except ApplicationEmail.DoesNotExist:
        pass
    return


def send_application_interview_mail(recipient):
    try:
        email = ApplicationEmail.objects.get(
            type__iexact='invited'
        )
        subject = email.subject
        message = f"{email.salutation} {recipient.first_name},\n {email.body}"

        mail = EmailMessage(
            subject,
            message,
            to=[recipient.email],
            from_email=settings.EMAIL_HOST_USER
        )
        status = mail.send()
        # print("Mail status:", status)
    except ApplicationEmail.DoesNotExist:
        pass
    return


def send_application_accepted_mail(recipient):
    try:
        email = ApplicationEmail.objects.get(
            type__iexact='accepted'
        )
        subject = email.subject
        message = f"{email.salutation} {recipient.first_name},\n {email.body}"

        mail = EmailMessage(
            subject,
            message,
            to=[recipient.email],
            from_email=settings.EMAIL_HOST_USER
        )
        status = mail.send()
        # print("Mail status:", status)
    except ApplicationEmail.DoesNotExist:
        pass
    return


def send_application_rejected_mail(recipient):
    try:
        email = ApplicationEmail.objects.get(
            type__iexact='rejected'
        )
        subject = email.subject
        message = f"{email.salutation} {recipient.first_name},\n {email.body}"

        mail = EmailMessage(
            subject,
            message,
            to=[recipient.email],
            from_email=settings.EMAIL_HOST_USER
        )
        status = mail.send()
        # print("Mail status:", status)
    except ApplicationEmail.DoesNotExist:
        pass
    return





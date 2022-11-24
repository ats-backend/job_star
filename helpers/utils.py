from django.core.mail import EmailMessage

from applications.models import ApplicationEmail
from job_star import settings


def send_application_success_mail(recipient):
    email = ApplicationEmail.objects.filter(
        type__iexact='completed_application'
    ).first()
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
    return


def send_application_shortlisted_mail(recipient):
    email = ApplicationEmail.objects.filter(
        type__iexact='shortlisted'
    ).first()
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
    return


def send_application_interview_mail(recipient):
    email = ApplicationEmail.objects.filter(
        type__iexact='invited'
    ).first()
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
    return


def send_application_accepted_mail(recipient):
    email = ApplicationEmail.objects.filter(
        type__iexact='accepted'
    ).first()
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
    return


def send_application_rejected_mail(recipient):
    email = ApplicationEmail.objects.filter(
        type__iexact='rejected'
    ).first()
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
    return





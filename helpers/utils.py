from django.core.mail import EmailMessage

from job_star import settings


def send_application_success_mail(recipient):
    subject = "Completed Application"
    message = f"Hi {recipient.first_name},\n" \
              "You have completed your application and " \
              "will receive a mail when there is an update."

    mail = EmailMessage(
        subject,
        message,
        to=[recipient.email],
        from_email=settings.EMAIL_HOST_USER
    )
    status = mail.send()
    print("Mail status:", status)
    return


def send_application_shortlisted_mail(recipient):
    subject = "Shortlisted for Assessment"
    message = f"Hi {recipient.first_name},\n" \
              "You have passed the application stage and " \
              "have been invited to take an assesment."

    mail = EmailMessage(
        subject,
        message,
        to=[recipient.email],
        from_email=settings.EMAIL_HOST_USER
    )
    status = mail.send()
    print("Mail status:", status)
    return


def send_application_interview_mail(recipient):
    subject = "Invited for Interview"
    message = f"Hi {recipient.first_name},\n" \
              "You have completed your application and " \
              "will receive a mail when there is an update"

    mail = EmailMessage(
        subject,
        message,
        to=[recipient.email],
        from_email=settings.EMAIL_HOST_USER
    )
    status = mail.send()
    print("Mail status:", status)
    return


def send_application_accepted_mail(recipient):
    subject = "Accepted Application"
    message = f"Hi {recipient.first_name},\n" \
              "We are pleased to inform you that you have "\
              "been selected for the AFEX TECH STARS. More "\
              "details on this will be sent to you by mail. "\
              "Congratulations."

    mail = EmailMessage(
        subject,
        message,
        to=[recipient.email],
        from_email=settings.EMAIL_HOST_USER
    )
    status = mail.send()
    print("Mail status:", status)
    return


def send_application_rejected_mail(recipient):
    subject = "Rejected Application"
    message = f"Hi {recipient.first_name},\n" \
              "After reviewing your application,"\
              " we are sorry to inform you that we will "\
              "not be proceeding with your application. "\
              "Thank you."

    mail = EmailMessage(
        subject,
        message,
        to=[recipient.email],
        from_email=settings.EMAIL_HOST_USER
    )
    status = mail.send()
    print("Mail status:", status)
    return





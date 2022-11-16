from django.urls import path

from .views import (
    AcceptedApplicationListAPIView, ApplicationListAPIView, CreateApplicationAPIView,
    ApplicationDetailAPIView, ApplicantListAPIView, ApplicantDetailAPIView,
    InvitedApplicationListAPIView, PendingApplicationListAPIView,
    RejectedApplicationListAPIView, SetAcceptedApplicationAPIView,
    SetInvitedApplicationAPIView, SetRejectedApplicationAPIView,
    TrackApplicationAPIView, SetShortlistedApplicationAPIView,
    ShortlistedApplicationListAPIView, SetPassedApplicationTestAPIView,
    SetFailedApplicationTestAPIView
)

app_name = 'applications'

urlpatterns = [
    path('', ApplicationListAPIView.as_view(), name='applications'),
    path('<int:job_id>/apply', CreateApplicationAPIView.as_view(), name='create_application'),
    path('<int:pk>', ApplicationDetailAPIView.as_view(), name='application_detail'),
    path('<int:pk>/applicants', ApplicantListAPIView.as_view(), name='applicants'),
    path('<int:pk>/applicants/<int:id>', ApplicantDetailAPIView.as_view(), name='applicant_detail'),
    path('accepted', AcceptedApplicationListAPIView.as_view(), name='accepted_applications'),
    path('invited-for-interview', InvitedApplicationListAPIView.as_view(), name='invited_applications'),
    path('pending', PendingApplicationListAPIView.as_view(), name='pending_applications'),
    path('rejected', RejectedApplicationListAPIView.as_view(), name='rejected_applications'),
    path('shortlisted', ShortlistedApplicationListAPIView.as_view(), name='shortlisted_applications'),
    path('<int:pk>/set-accepted', SetAcceptedApplicationAPIView.as_view(), name='accept'),
    path('<int:pk>/set-invited', SetInvitedApplicationAPIView.as_view(), name='invite'),
    path('<int:pk>/set-shortlisted', SetShortlistedApplicationAPIView.as_view(), name='shortlist'),
    path('<int:pk>/set-rejected', SetRejectedApplicationAPIView.as_view(), name='reject'),
    path('<int:pk>/set-passed', SetPassedApplicationTestAPIView.as_view(), name='passed'),
    path('<int:pk>/set-passed', SetFailedApplicationTestAPIView.as_view(), name='failed'),
    path('track', TrackApplicationAPIView.as_view(), name='track'),

]

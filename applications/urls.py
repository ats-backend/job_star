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
    path('applications', ApplicationListAPIView.as_view(), name='applications'),
    path('<int:job_id>/applications', CreateApplicationAPIView.as_view(), name='create_application'),
    path('applications/<int:pk>', ApplicationDetailAPIView.as_view(), name='application_detail'),
    path('applications/<int:pk>/applicants', ApplicantListAPIView.as_view(), name='applicants'),
    path('applications/<int:pk>/applicants/<int:id>', ApplicantDetailAPIView.as_view(), name='applicant_detail'),
    path('applications/accepted', AcceptedApplicationListAPIView.as_view(), name='accepted_applications'),
    path('applications/invited-for-interview', InvitedApplicationListAPIView.as_view(), name='invited_applications'),
    path('applications/pending', PendingApplicationListAPIView.as_view(), name='pending_applications'),
    path('applications/rejected', RejectedApplicationListAPIView.as_view(), name='rejected_applications'),
    path('applications/shortlisted', ShortlistedApplicationListAPIView.as_view(), name='shortlisted_applications'),
    path('applications/<int:pk>/set-accepted', SetAcceptedApplicationAPIView.as_view(), name='accept'),
    path('applications/<int:pk>/set-invited', SetInvitedApplicationAPIView.as_view(), name='invite'),
    path('applications/<int:pk>/set-shortlisted', SetShortlistedApplicationAPIView.as_view(), name='shortlist'),
    path('applications/<int:pk>/set-rejected', SetRejectedApplicationAPIView.as_view(), name='reject'),
    path('applications/<int:pk>/set-passed', SetPassedApplicationTestAPIView.as_view(), name='passed'),
    path('applications/<int:pk>/set-passed', SetFailedApplicationTestAPIView.as_view(), name='failed'),
    path('applications/track', TrackApplicationAPIView.as_view(), name='track'),

]
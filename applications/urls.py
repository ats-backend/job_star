from django.urls import path

from .views import (
    AcceptedApplicationListView, ApplicationListAPIView, CreateApplicationAPIView,
    ApplicationDetailAPIView, ApplicantListAPIView, ApplicantDetailAPIView,
    InvitedApplicationListView, PendingApplicationListView,
    RejectedApplicationListView, SetAcceptedApplicationAPIView,
    SetInvitedApplicationAPIView, SetRejectedApplicationAPIView,
    SetShortlistedApplicationAPIView, ShortlistedApplicationListView
)

app_name = 'applications'

urlpatterns = [
    path('applications', ApplicationListAPIView.as_view(), name='applications'),
    path('<int:job_id>/applications', CreateApplicationAPIView.as_view(), name='create_application'),
    path('applications/<int:pk>', ApplicationDetailAPIView.as_view(), name='application_detail'),
    path('applications/<int:pk>/applicants', ApplicantListAPIView.as_view(), name='applicants'),
    path('applications/<int:pk>/applicants/<int:id>', ApplicantDetailAPIView.as_view(), name='applicant_detail'),
    path('applications/accepted', AcceptedApplicationListView.as_view(), name='accepted_applications'),
    path('applications/invited-for-interview', InvitedApplicationListView.as_view(), name='invited_applications'),
    path('applications/pending', PendingApplicationListView.as_view(), name='pending_applications'),
    path('applications/rejected', RejectedApplicationListView.as_view(), name='rejected_applications'),
    path('applications/shortlisted', ShortlistedApplicationListView.as_view(), name='shortlisted_applications'),
    path('applications/<int:pk>/set-accepted', SetAcceptedApplicationAPIView.as_view(), name='accept'),
    path('applications/<int:pk>/set-invited', SetInvitedApplicationAPIView.as_view(), name='invite'),
    path('applications/<int:pk>/set-shortlisted', SetShortlistedApplicationAPIView.as_view(), name='shortlist'),
    path('applications/<int:pk>/set-rejected', SetRejectedApplicationAPIView.as_view(), name='reject'),

]

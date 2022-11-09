from django.urls import path

from .views import (CourseDetailAPIView,
                    CourseUpdateAPIView,CourseDeleteAPIView,
                    CoursesListAPIView,  CoursesCreationAPIView,
                    JobListCreateAPIView, JobDetailAPIView,
                    JobUpdateAPIView, JobDestroyAPIView,
                    CohortListAPIView, CohortUpdateAPIView,
                    CohortCreationAPIView, CohortDetailAPIView,
                    CohortDestroyAPIView)

app_name = 'job'

urlpatterns = [
    # courses urls
    path('courses/', CoursesListAPIView.as_view()),
    path('courses/create', CoursesCreationAPIView.as_view()),
    path('courses/<int:pk>', CourseDetailAPIView.as_view()),
    path('courses/<int:pk>/edit', CourseUpdateAPIView.as_view()),
    path('courses/<int:pk>/delete', CourseDeleteAPIView.as_view()),

    # Cohort urls
    path('cohorts', CohortListAPIView.as_view()),
    path('cohort/create', CohortCreationAPIView.as_view()),
    path('cohort/<int:pk>', CohortDetailAPIView.as_view()),
    path('cohort/<int:pk>/edit', CohortUpdateAPIView.as_view()),
    path('cohort/<int:pk>/delete', CohortDestroyAPIView.as_view()),


    # Job urls
    path('', JobListCreateAPIView.as_view()),
    # path('create/', JobCreateAPIView.as_view(), name='job-create'),
    path('<int:pk>/detail', JobDetailAPIView.as_view(), name='job-detail'),
    path('<int:pk>/update', JobUpdateAPIView.as_view(), name='job-update'),
    path('<int:pk>/delete', JobDestroyAPIView.as_view(), name='job-delete'),

]

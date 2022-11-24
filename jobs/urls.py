from django.urls import path, include

from .views import (CourseDetailAPIView,
                    CourseUpdateAPIView, CourseDeleteAPIView,
                    CoursesListAPIView,  CoursesCreationAPIView,
                    JobListCreateAPIView, JobDetailAPIView,
                    JobUpdateAPIView, JobDestroyAPIView,
                    CohortListAPIView, CohortUpdateAPIView,
                    CohortCreationAPIView, CohortDetailAPIView,
                    CohortDestroyAPIView, CohortCountDownAPIView)

from applications.views import ApplicationListAPIView

app_name = 'job'

urlpatterns = [
    # courses urls
    path('courses/', CoursesListAPIView.as_view()),
    path('courses/create', CoursesCreationAPIView.as_view()),
    path('courses/<int:pk>', CourseDetailAPIView.as_view(), name='course-detail'),
    path('courses/<int:pk>/edit', CourseUpdateAPIView.as_view()),
    path('courses/<int:pk>/delete', CourseDeleteAPIView.as_view()),

    # Cohort urls
    path('cohorts', CohortListAPIView.as_view(), name='cohorts'),
    path('cohort/create', CohortCreationAPIView.as_view(), name='cohort-create'),
    path('cohort/<int:pk>', CohortDetailAPIView.as_view()),
    path('cohort/<int:pk>/edit', CohortUpdateAPIView.as_view()),
    path('cohort/<int:pk>/delete', CohortDestroyAPIView.as_view()),
    path('latest-cohort', CohortCountDownAPIView.as_view()),

    # Job urls
    path('', JobListCreateAPIView.as_view()),
    # path('create/', JobCreateAPIView.as_view(), name='job-create'),
    path('<int:pk>/detail', JobDetailAPIView.as_view(), name='job-detail'),
    path('<int:pk>/update', JobUpdateAPIView.as_view(), name='job-update'),
    path('<int:pk>/delete', JobDestroyAPIView.as_view(), name='job-delete'),
    path('<int:pk>/applications', ApplicationListAPIView.as_view(), name='applications'),

]

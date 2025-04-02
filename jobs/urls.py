from django.urls import path
from . import views

urlpatterns = [
    path("", views.login, name="login"),
    path('signup/', views.signup, name='signup'), 
    path("login/", views.login, name="login"),
    path("logout/", views.logout, name="logout"),
    path("dashboard/", views.dashboard, name="dashboard"),
    path("add_job/", views.add_job, name="add_job"),
    path("delete_job/<str:job_id>/", views.delete_job, name="delete_job"),
    path("apply_job/<str:job_id>/", views.apply_job, name="apply_job"),
    path("review_applications/<str:job_id>/", views.review_applications, name="review_applications"),
    path("update_status/<str:email>/<str:job_id>/<str:status>/", views.update_status, name="update_status"),
    path('dashboard/', views.employer_dashboard1, name='employer_dashboard'),
]

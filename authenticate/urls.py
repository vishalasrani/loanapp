from django.urls import path
from . import views

app_name = "authenticate"
urlpatterns = [
    path("", views.home, name="home"),
    path("login/", views.login_user, name="login"),
    path("logout/", views.logout_user, name="logout"),
    path("register/", views.register_user, name="register"),
    path("edit_profile/", views.edit_profile, name="edit_profile"),
    path("change_password/", views.change_password, name="change_password"),
    path("loan_application", views.loan_application, name="loan_application"),
    path(
        "loan_application/status/<str:loan_id>",
        views.LoanStatus.as_view(),
        name="loan_status",
    ),
]


from .views import (
                    Profile,
                    AbsenceRequest,
                    AbsenceRequestUpdate,
                    AbsenceRequestList,
                    AbsenceRequestDelete
 )
from django.urls import path
from account.views import (Login,
                            Register,
                            CustomLogoutView,
                            CustomPasswordChangeView,
                            Home,
                            UserChangeInformation,
                            UserChangeAbsence,
                            RegisterAbsenceDateView
                            )


app_name = "accounts"
urlpatterns = [

    path("", Home.as_view(), name="home"),
    path("profile/", Profile.as_view(), name="profile"),
    path("absence-request/", AbsenceRequest.as_view(), name="absence-request"),
    path("absence-request-update/<int:user_pk>/<int:year>/<int:month>/<int:day>/", AbsenceRequestUpdate.as_view(), name="absence-request-update"),
    path("absence-request-list/", AbsenceRequestList.as_view(), name="absence-request-list"),
     path("absence-request-delete/<int:pk>/", AbsenceRequestDelete.as_view(), name="absence-request-delete"),
    
    path("user-change-info/<int:pk>/", UserChangeInformation.as_view(), name="user-change-info"),
    path("absence-date/<int:pk>/<int:year>/", RegisterAbsenceDateView.as_view(), name="absence-date"),
    path("absence-change/<int:pk>/<int:year>/",UserChangeAbsence.as_view(), name="absence-change"),
    path("login/", Login.as_view(redirect_authenticated_user=True), name="login"),
    path("logout/", CustomLogoutView.as_view(), name="logout"),
    path('sign-up/',Register.as_view(redirect_authenticated_user=True), name="register" ),#SignUP
    path(
        "password_change/", CustomPasswordChangeView.as_view(), name="password_change"
    ),
    
]
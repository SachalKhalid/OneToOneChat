from django.urls import path

from .views import IndexView, RoomView, MainView, RegisterView, LoginView, LogoutView


urlpatterns = [
    # path("base", base.as_view(), name="main"),
    path("register/", RegisterView.as_view(), name = "register"),
    path("login/", LoginView.as_view(), name = "login"),
    path("logout/", LogoutView.as_view(), name = "logout"),
    path("index/", IndexView.as_view(), name="index"),
    path("main/", MainView.as_view(), name="main"),
    # path('main/', MainView.as_view(), name='main'),
    path("<str:room_name>/", RoomView.as_view(), name="room"),
]
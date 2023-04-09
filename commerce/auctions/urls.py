from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("create", views.create, name="create"),
    path("listings/<int:auction_id>", views.auction, name="auction"),
    path("watchlist", views.watchList, name = "watchList"),
    path("profile", views.profile, name="profile"),
    path("profile/active_auctions", views.active_auctions, name="active auctions"),
    path("profile/non_active_auctions", views.non_active_auctions, name="non active auctions"),
    path("profile/won_auctions", views.won_auctions, name="won auctions"),
]

from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("create", views.create, name="create"),
    path("listing/<int:listing_id>", views.listing, name="listing"),
    path('watchlist/<int:listing_id>', views.add_to_watchlist, name='add_to_watchlist'),
    path("watchlist", views.watchlist, name="watchlist"),
    path("bid/<int:listing_id>", views.bid, name="bid"),
    path("comment/<int:listing_id>", views.comment, name="comment"),
    path("close/<int:listing_id>", views.close, name="close"),
    path("mylistings", views.my_listings, name="my_listings")
]

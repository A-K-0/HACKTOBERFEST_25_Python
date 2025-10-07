from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),

    # Listings
    path("listings/create", views.create_listing, name="create_listing"),
    path("listings/<int:listing_id>", views.listing_detail, name="listing_detail"),
    path("listings/<int:listing_id>/bid", views.place_bid, name="place_bid"),
    path("listings/<int:listing_id>/comment", views.add_comment, name="add_comment"),
    path("listings/<int:listing_id>/toggle-watch", views.toggle_watch, name="toggle_watch"),
    path("listings/<int:listing_id>/close", views.close_listing, name="close_listing"),

    # Watchlist & categories
    path("watchlist", views.watchlist, name="watchlist"),
    path("closed", views.closed_listings, name="closed_listings"),
    path("categories", views.categories, name="categories"),
    path("categories/<int:category_id>", views.category_listings, name="category_listings"),
]

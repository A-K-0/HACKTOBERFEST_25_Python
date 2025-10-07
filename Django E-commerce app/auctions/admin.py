from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as DjangoUserAdmin

from .models import Category, Listing, Bid, Comment, User


@admin.register(User)
class UserAdmin(DjangoUserAdmin):
    pass


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("id", "name")
    search_fields = ("name",)


@admin.register(Listing)
class ListingAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "owner", "is_active", "starting_bid", "current_price", "category", "created_at")
    list_filter = ("is_active", "category")
    search_fields = ("title", "description")
    autocomplete_fields = ("owner", "category", "watchers", "winner")


@admin.register(Bid)
class BidAdmin(admin.ModelAdmin):
    list_display = ("id", "listing", "bidder", "amount", "placed_at")
    search_fields = ("listing__title", "bidder__username")
    autocomplete_fields = ("listing", "bidder")


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ("id", "listing", "author", "created_at")
    search_fields = ("listing__title", "author__username", "content")
    autocomplete_fields = ("listing", "author")

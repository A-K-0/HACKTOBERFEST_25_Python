from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db import IntegrityError, transaction
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from decimal import Decimal, InvalidOperation

from .models import User, Listing, Bid, Comment, Category


def index(request):
    listings = Listing.objects.filter(is_active=True).select_related("owner", "category")
    return render(request, "auctions/index.html", {"listings": listings})


def login_view(request):
    if request.method == "POST":

         
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

         
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })

        
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")


@login_required
def create_listing(request):
    if request.method == "POST":
        title = request.POST.get("title", "").strip()
        description = request.POST.get("description", "").strip()
        image_url = request.POST.get("image_url", "").strip() or None
        starting_bid_raw = request.POST.get("starting_bid", "").strip()
        category_id = request.POST.get("category")

        if not title or not description or not starting_bid_raw:
            messages.error(request, "Title, description and starting bid are required.")
            return render(request, "auctions/create.html", {"categories": Category.objects.all()})

        try:
            starting_bid = Decimal(starting_bid_raw)
            if starting_bid <= 0:
                raise InvalidOperation
        except (InvalidOperation, ValueError):
            messages.error(request, "Starting bid must be a positive number.")
            return render(request, "auctions/create.html", {"categories": Category.objects.all()})

        category = None
        if category_id:
            category = Category.objects.filter(pk=category_id).first()

        listing = Listing.objects.create(
            title=title,
            description=description,
            image_url=image_url,
            starting_bid=starting_bid,
            owner=request.user,
            category=category,
        )
        messages.success(request, "Listing created.")
        return redirect("listing_detail", listing_id=listing.id)

    return render(request, "auctions/create.html", {"categories": Category.objects.all()})


def listing_detail(request, listing_id):
    listing = get_object_or_404(Listing.objects.select_related("owner", "category", "winner"), pk=listing_id)
    comments = listing.comments.select_related("author")
    bids = listing.bids.select_related("bidder")
    is_watching = False
    if request.user.is_authenticated:
        is_watching = listing.watchers.filter(pk=request.user.id).exists()
    return render(request, "auctions/detail.html", {
        "listing": listing,
        "comments": comments,
        "bids": bids,
        "is_watching": is_watching,
    })


@login_required
def place_bid(request, listing_id):
    listing = get_object_or_404(Listing, pk=listing_id)
    if request.method != "POST":
        return redirect("listing_detail", listing_id=listing.id)
    if not listing.is_active:
        messages.error(request, "Auction is closed.")
        return redirect("listing_detail", listing_id=listing.id)

    amount_raw = request.POST.get("bid_amount", "").strip()
    try:
        amount = Decimal(amount_raw)
    except (InvalidOperation, ValueError):
        messages.error(request, "Please enter a valid bid amount.")
        return redirect("listing_detail", listing_id=listing.id)

    min_allowed = listing.current_price
    if amount <= 0 or amount < min_allowed or amount < listing.starting_bid:
        messages.error(request, f"Bid must be at least {max(min_allowed, listing.starting_bid)}.")
        return redirect("listing_detail", listing_id=listing.id)

    with transaction.atomic():
        # Recheck highest bid inside transaction
        listing_refreshed = Listing.objects.select_for_update().get(pk=listing.id)
        min_allowed_now = listing_refreshed.current_price
        if amount <= min_allowed_now or amount < listing_refreshed.starting_bid:
            messages.error(request, f"Bid must be at least {max(min_allowed_now, listing_refreshed.starting_bid)}.")
            return redirect("listing_detail", listing_id=listing.id)
        Bid.objects.create(listing=listing_refreshed, bidder=request.user, amount=amount)

    messages.success(request, "Bid placed successfully.")
    return redirect("listing_detail", listing_id=listing.id)


@login_required
def add_comment(request, listing_id):
    listing = get_object_or_404(Listing, pk=listing_id)
    if request.method == "POST":
        content = request.POST.get("content", "").strip()
        if not content:
            messages.error(request, "Comment cannot be empty.")
        else:
            Comment.objects.create(listing=listing, author=request.user, content=content)
            messages.success(request, "Comment added.")
    return redirect("listing_detail", listing_id=listing.id)


@login_required
def toggle_watch(request, listing_id):
    listing = get_object_or_404(Listing, pk=listing_id)
    if request.method == "POST":
        if listing.watchers.filter(pk=request.user.id).exists():
            listing.watchers.remove(request.user)
            messages.info(request, "Removed from watchlist.")
        else:
            listing.watchers.add(request.user)
            messages.success(request, "Added to watchlist.")
    return redirect("listing_detail", listing_id=listing.id)


@login_required
def close_listing(request, listing_id):
    listing = get_object_or_404(Listing, pk=listing_id)
    if request.method == "POST":
        if request.user != listing.owner:
            messages.error(request, "Only the owner can close this auction.")
            return redirect("listing_detail", listing_id=listing.id)
        if not listing.is_active:
            return redirect("listing_detail", listing_id=listing.id)
        top_bid = listing.bids.order_by("-amount", "-placed_at").first()
        if top_bid:
            listing.winner = top_bid.bidder
        listing.is_active = False
        listing.save(update_fields=["winner", "is_active"])
        messages.success(request, "Auction closed.")
    return redirect("listing_detail", listing_id=listing.id)


@login_required
def watchlist(request):
    listings = request.user.watchlist.select_related("owner", "category").all()
    return render(request, "auctions/watchlist.html", {"listings": listings})


def closed_listings(request):
    listings = Listing.objects.filter(is_active=False).select_related("owner", "category", "winner").order_by("-created_at")
    return render(request, "auctions/closed_listings.html", {"listings": listings})


def categories(request):
    cats = Category.objects.all()
    return render(request, "auctions/categories.html", {"categories": cats})


def category_listings(request, category_id):
    category = get_object_or_404(Category, pk=category_id)
    listings = category.listings.filter(is_active=True).select_related("owner", "category")
    return render(request, "auctions/category_listings.html", {"category": category, "listings": listings})

from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from django.urls import reverse
from django.db import IntegrityError
from django.http.response import JsonResponse
from datetime import datetime
from django.db.models import Avg

from sqlalchemy import false

from .models import User, Resort, Review


def index(request):
    return render(request, "shredmap_midwest/index.html")


def resort_view(request, resort_id):

    # Initialize variables
    error = ""
    success = ""
    visited = False
    this_review = ""
    deleted = False

    # Get the resort info
    try:
        resort = Resort.objects.get(pk=resort_id)
    except Resort.DoesNotExist:
        return JsonResponse({"error": "Resort not found."}, status=404)

    # Get the reviews of this resort
    try:
        this_resort_reviews = Review.objects.filter(resort=resort)
        reviews = this_resort_reviews.order_by("-timestamp")
    except Review.DoesNotExist:
        return JsonResponse({"error": "Review not found."}, status=404)

    # Check if this user is in the resort's list of visitors
    if request.user in resort.visitors.all():
        visited = True
        try:
            this_review = Review.objects.get(
                resort=resort, author=request.user)
        except Review.DoesNotExist:
            return JsonResponse({"error": "User listed as a visitor, but review does not exist"})

    # If the user submitted the review form, validate it and post it
    if request.method == "POST":

        # If the user submitted the delete form, delete the review
        if request.POST.get("delete") != None:
            this_review.delete()
            this_review = ""
            resort.visitors.remove(request.user)
            visited = False
            deleted = True

            return render(request, "shredmap_midwest/resort.html", {
                "resort": resort,
                "error": error,
                "reviews": reviews,
                "visited": visited,
                "this_review": this_review,
                "avg_park": this_resort_reviews.aggregate(Avg('park_review')),
                "avg_groomer": this_resort_reviews.aggregate(Avg('groomer_review')),
                "avg_lift": this_resort_reviews.aggregate(Avg('lift_review')),
                "avg_vibe": this_resort_reviews.aggregate(Avg('vibe_review')),
                "deleted": deleted,
            })

        review = Review()
        at_least_one_field = False

        # All fields are optional as long as you fill out at least one, so we need to check if they exist before adding them
        message = request.POST.get("message", None)
        park_review = request.POST.get("park_review", None)
        groomer_review = request.POST.get("groomer_review", None)
        lift_review = request.POST.get("lift_review", None)
        vibe_review = request.POST.get("vibe_review", None)

        # Check if this is an edit or a first-time review
        if visited:
            this_review.edited = True
            review.timestamp = datetime.now()

            # Update the fields in the review
            if message:
                this_review.message = message
                at_least_one_field = True
            else:
                this_review.message = None

            if park_review:
                this_review.park_review = park_review
                at_least_one_field = True
            else:
                this_review.park_review = None

            if groomer_review:
                this_review.groomer_review = groomer_review
                at_least_one_field = True
            else:
                this_review.groomer_review = None

            if lift_review:
                this_review.lift_review = lift_review
                at_least_one_field = True
            else:
                this_review.lift_review = None

            if vibe_review:
                this_review.vibe_review = vibe_review
                at_least_one_field = True
            else:
                this_review.vibe_review = None

        else:
            # Add the user to the resort's list of visitors
            resort.visitors.add(request.user)

            # Add the fields to the review
            if message:
                review.message = message
                at_least_one_field = True
            if park_review:
                review.park_review = park_review
                at_least_one_field = True
            if groomer_review:
                review.groomer_review = groomer_review
                at_least_one_field = True
            if lift_review:
                review.lift_review = lift_review
                at_least_one_field = True
            if vibe_review:
                review.vibe_review = vibe_review
                at_least_one_field = True

        # Make sure there is at least one field filled in, and the user is signed in
        if not at_least_one_field:
            error = "Error: You must fill in at least one field to leave a review."
        if not request.user:
            error = "Error: You must be signed in to leave a review."

        if error:
            return render(request, "shredmap_midwest/resort.html", {
                "resort": resort,
                "error": error,
                "reviews": reviews,
                "visited": visited,
                "this_review": this_review,
                "avg_park": this_resort_reviews.aggregate(Avg('park_review')),
                "avg_groomer": this_resort_reviews.aggregate(Avg('groomer_review')),
                "avg_lift": this_resort_reviews.aggregate(Avg('lift_review')),
                "avg_vibe": this_resort_reviews.aggregate(Avg('vibe_review')),
            })

        # Save the review
        if visited:
            this_review.timestamp = datetime.now()
            this_review.save()

        else:
            review.author = request.user
            review.resort = resort
            visited = True
            this_review = review
            review.save()

        success = "Thank you for your review!"

        return render(request, "shredmap_midwest/resort.html", {
            "resort": resort,
            "success": success,
            "reviews": reviews,
            "visited": visited,
            "this_review": this_review,
            "avg_park": this_resort_reviews.aggregate(Avg('park_review')),
            "avg_groomer": this_resort_reviews.aggregate(Avg('groomer_review')),
            "avg_lift": this_resort_reviews.aggregate(Avg('lift_review')),
            "avg_vibe": this_resort_reviews.aggregate(Avg('vibe_review')),
        })

    # Show information about the resort
    return render(request, "shredmap_midwest/resort.html", {
        "resort": resort,
        "reviews": reviews,
        "visited": visited,
        "this_review": this_review,
        "avg_park": this_resort_reviews.aggregate(Avg('park_review')),
        "avg_groomer": this_resort_reviews.aggregate(Avg('groomer_review')),
        "avg_lift": this_resort_reviews.aggregate(Avg('lift_review')),
        "avg_vibe": this_resort_reviews.aggregate(Avg('vibe_review')),
    })


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "shredmap_midwest/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "shredmap_midwest/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "shredmap_midwest/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "shredmap_midwest/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "shredmap_midwest/register.html")


def resort(request, resort_id):
    # API route for getting the resort locations

    # Query for the requested resort
    try:
        resort = Resort.objects.get(pk=resort_id)
    except Resort.DoesNotExist:
        return JsonResponse({"error": "Resort not found."}, status=404)

    # Return resort contents
    if request.method == "GET":
        return JsonResponse(resort.serialize())

    else:
        return JsonResponse({"error": "GET request required."}, status=400)


def all_resorts(request):
    # API route for getting all the resorts
    # https://zetcode.com/django/jsonresponse/

    if request.method == "GET":
        resorts = []
        for resort in Resort.objects.all():
            resorts.append(resort.serialize())

        return JsonResponse(resorts, safe=False)

    else:
        return JsonResponse({"error": "GET request required."}, status=400)


def user_visited(request):
    # API route for getting the resorts the user has visited

    if request.method == "GET":
        user_visited = []

        for resort in Resort.objects.all():
            if request.user in resort.visitors.all():
                user_visited.append(resort.id)

        return JsonResponse(user_visited, safe=False)

    else:
        return JsonResponse({"error": "GET request required."}, status=400)

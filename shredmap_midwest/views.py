from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from django.urls import reverse
from django.db import IntegrityError
from django.http.response import JsonResponse
from datetime import datetime
from django.db.models import Avg
from django.db.models import F

from sqlalchemy import false

from .models import User, Resort, Review

# Send a message to the Django console using logger.info
import logging
logger = logging.getLogger('django')


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
        reviews = Review.objects.filter(resort=resort).order_by("-timestamp")
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

            # Only attempt to delete the review if it exists (prevents error on page refresh after deleting)
            if this_review:
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
                "deleted": deleted,
                "avg_park": reviews.aggregate(Avg('park_review')),
                "avg_groomer": reviews.aggregate(Avg('groomer_review')),
                "avg_lift": reviews.aggregate(Avg('lift_review')),
                "avg_vibe": reviews.aggregate(Avg('vibe_review')),
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
                "avg_park": reviews.aggregate(Avg('park_review')),
                "avg_groomer": reviews.aggregate(Avg('groomer_review')),
                "avg_lift": reviews.aggregate(Avg('lift_review')),
                "avg_vibe": reviews.aggregate(Avg('vibe_review')),
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

        # Update the average values for the reviews
        update_averages(resort, resort_id)

        success = "Thank you for your review!"

        return render(request, "shredmap_midwest/resort.html", {
            "resort": resort,
            "success": success,
            "reviews": reviews,
            "visited": visited,
            "this_review": this_review,
            "avg_park": reviews.aggregate(Avg('park_review')),
            "avg_groomer": reviews.aggregate(Avg('groomer_review')),
            "avg_lift": reviews.aggregate(Avg('lift_review')),
            "avg_vibe": reviews.aggregate(Avg('vibe_review')),
        })

    # Show information about the resort
    return render(request, "shredmap_midwest/resort.html", {
        "resort": resort,
        "reviews": reviews,
        "visited": visited,
        "this_review": this_review,
        "avg_park": reviews.aggregate(Avg('park_review')),
        "avg_groomer": reviews.aggregate(Avg('groomer_review')),
        "avg_lift": reviews.aggregate(Avg('lift_review')),
        "avg_vibe": reviews.aggregate(Avg('vibe_review')),
    })


def resorts(request):
    # Display a list of resorts, allowing the user to sort by different categories
    category = ""

    # Get a list of all the resorts
    resorts = Resort.objects.all()

    # Get the resorts the user has visited, if the user is signed in
    visited_resorts = Resort.objects.none()
    if request.user.is_authenticated:
        try:
            this_user_reviews = Review.objects.filter(author=request.user)
        except Review.DoesNotExist:
            return JsonResponse({"error": "User listed as a visitor, but review does not exist"})

        for review in this_user_reviews:
            visited_resorts = visited_resorts | Resort.objects.filter(
                resort_review=review)

    else:
        this_user_reviews = None

    # If the user edits the filters, get the proper data
    if request.method == "POST":

        # Keep track of the switches/radio buttons that are activated, so they don't reset
        active_filters = []

        # Start out with an empty queryset (we will add to this based on what filters the user selects)
        filtered_resorts = Resort.objects.none()

        # Access the category filter, if applied
        categorySelect = request.POST.get("categorySelect")

        # Keep track of whether a state selection was made
        stateSelected = False

        # Adjust the list of resorts based on what states were selected
        # In hindsight this could probably be accomplished with a loop
        # https://simpleisbetterthancomplex.com/tips/2016/06/20/django-tip-5-how-to-merge-querysets.html
        if request.POST.get("ND"):
            filtered_resorts = filtered_resorts | Resort.objects.filter(
                state="ND")
            active_filters.append("ND")
            stateSelected = True
        if request.POST.get("SD"):
            filtered_resorts = filtered_resorts | Resort.objects.filter(
                state="SD")
            active_filters.append("SD")
            stateSelected = True
        if request.POST.get("MN"):
            filtered_resorts = filtered_resorts | Resort.objects.filter(
                state="MN")
            active_filters.append("MN")
            stateSelected = True
        if request.POST.get("WI"):
            filtered_resorts = filtered_resorts | Resort.objects.filter(
                state="WI")
            active_filters.append("WI")
            stateSelected = True
        if request.POST.get("MI"):
            filtered_resorts = filtered_resorts | Resort.objects.filter(
                state="MI")
            active_filters.append("MI")
            stateSelected = True
        if request.POST.get("IL"):
            filtered_resorts = filtered_resorts | Resort.objects.filter(
                state="IL")
            active_filters.append("IL")
            stateSelected = True
        if request.POST.get("MO"):
            filtered_resorts = filtered_resorts | Resort.objects.filter(
                state="MO")
            active_filters.append("MO")
            stateSelected = True
        if request.POST.get("IN"):
            filtered_resorts = filtered_resorts | Resort.objects.filter(
                state="IN")
            active_filters.append("IN")
            stateSelected = True
        if request.POST.get("OH"):
            filtered_resorts = filtered_resorts | Resort.objects.filter(
                state="OH")
            active_filters.append("OH")
            stateSelected = True
        if request.POST.get("IA"):
            filtered_resorts = filtered_resorts | Resort.objects.filter(
                state="IA")
            active_filters.append("IA")
            stateSelected = True

        # If no states selected, show all resorts
        if not stateSelected:
            filtered_resorts = Resort.objects.all()

        # Order the list based on which category was selected
        # https://stackoverflow.com/questions/15121093/django-adding-nulls-last-to-query
        if categorySelect == "filter_park":
            filtered_resorts = filtered_resorts.order_by(
                F('avg_park').desc(nulls_last=True))
            category = "Terrain Park"
            active_filters.append("park")

        elif categorySelect == "filter_groomers":
            filtered_resorts = filtered_resorts.order_by(
                F('avg_groomer').desc(nulls_last=True))
            category = "Groomers"
            active_filters.append("groomers")

        elif categorySelect == "filter_lifts":
            filtered_resorts = filtered_resorts.order_by(
                F('avg_lift').desc(nulls_last=True))
            category = "Chairlifts & Tow Ropes"
            active_filters.append("lift")

        elif categorySelect == "filter_vibe":
            filtered_resorts = filtered_resorts.order_by(
                F('avg_vibe').desc(nulls_last=True))
            category = "Overall Vibe"
            active_filters.append("vibe")

        else:
            active_filters.append("noneRadio")

        return render(request, "shredmap_midwest/resorts.html", {
            "resorts": filtered_resorts,
            "category": category,
            "active_filters": active_filters,
            "visited_resorts": visited_resorts,
        })

    return render(request, "shredmap_midwest/resorts.html", {
        "resorts": resorts,
        "category": category,
        "none_radio": True,
        "visited_resorts": visited_resorts,
    })


def get_average(resort, category):
    # Python function to get the average of the reviews in a specific category for any given resort
    # Category should be "park_review", "groomer_review", "lift_review", or "vibe_review"

    # Get the reviews of this resort
    try:
        this_resort_reviews = Review.objects.filter(resort=resort)
    except Review.DoesNotExist:
        return JsonResponse({"error": "Review not found."}, status=404)

    # Return the average reviews for the specified category
    return this_resort_reviews.aggregate(Avg(category))


def update_averages(resort, resort_id):
    # Python function to update the average values for the reviews
    # https://stackoverflow.com/questions/41744096/efficient-way-to-update-multiple-fields-of-django-model-object
    Resort.objects.filter(id=resort_id).update(
        avg_park=get_average(resort, 'park_review')['park_review__avg'])
    Resort.objects.filter(id=resort_id).update(
        avg_groomer=get_average(resort, 'groomer_review')['groomer_review__avg'])
    Resort.objects.filter(id=resort_id).update(
        avg_lift=get_average(resort, 'lift_review')['lift_review__avg'])
    Resort.objects.filter(id=resort_id).update(
        avg_vibe=get_average(resort, 'vibe_review')['vibe_review__avg'])

    return


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


def how_to(request):
    return render(request, "shredmap_midwest/howto.html")


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

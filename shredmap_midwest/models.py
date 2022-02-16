from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    pass


class Resort(models.Model):
    STATES = (
        ('ND', 'North Dakota'),
        ('SD', 'South Dakota'),
        ('MN', 'Minnesota'),
        ('WI', 'Wisconsin'),
        ('MI', 'Michigan'),
        ('IA', 'Iowa'),
        ('MO', 'Missouri'),
        ('IL', 'Illinois'),
        ('IN', 'Indiana'),
        ('OH', 'Ohio'),
    )
    name = models.CharField(max_length=100)
    state = models.CharField(max_length=2, choices=STATES)
    city = models.CharField(max_length=100)
    visitors = models.ManyToManyField(User, related_name="visited_resort")
    website = models.URLField()

    # Coordinates to the location
    x = models.FloatField()
    y = models.FloatField()

    # Review averages
    avg_park = models.FloatField(default=None, null=True, blank=True)
    avg_groomer = models.FloatField(default=None, null=True, blank=True)
    avg_lift = models.FloatField(default=None, null=True, blank=True)
    avg_vibe = models.FloatField(default=None, null=True, blank=True)

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "state": self.state,
            "city": self.city,
            "website": self.website,
            "x": self.x,
            "y": self.y,
        }

    def __str__(self):
        return f"Resort {self.id}: {self.name} in {self.city}, {self.state}."


class Review(models.Model):
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="review")
    resort = models.ForeignKey(
        Resort, on_delete=models.CASCADE, related_name="resort_review")

    # https://stackoverflow.com/questions/16828315/how-can-i-make-my-model-fields-optional-in-django
    message = models.TextField(default=None, null=True, blank=True)
    park_review = models.IntegerField(default=None, null=True, blank=True)
    groomer_review = models.IntegerField(default=None, null=True, blank=True)
    lift_review = models.IntegerField(default=None, null=True, blank=True)
    vibe_review = models.IntegerField(default=None, null=True, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    edited = models.BooleanField(default=False)

    def serialize(self):
        return {
            "id": self.id,
            "author": self.author.username,
            "resort": self.resort.name,
            "message": self.message,
            "park_review": self.park_review,
            "groomer_review": self.groomer_review,
            "lift_review": self.lift_review,
            "vibe_review": self.vibe_review,
            "timestamp": self.timestamp,
            "edited": self.edited,
        }

    def __str__(self):
        return f"Review {self.id} by {self.author.username} at {self.resort.name} on {self.timestamp}."

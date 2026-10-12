"""Models of the profiles app."""
from django.db import models
from django.contrib.auth.models import User


class Profile(models.Model):
    """Extra information about a user, such as the favorite city."""

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    favorite_city = models.CharField(max_length=64, blank=True)

    def __str__(self):
        """Return a short text representation of the profile.

        Returns:
            str: The username of the profile owner.
        """
        return self.user.username

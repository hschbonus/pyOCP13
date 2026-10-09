"""Views of the profiles app."""
import logging

from django.http import Http404
from django.shortcuts import render
from .models import Profile


logger = logging.getLogger(__name__)


def index(request):
    """Display the list of all profiles.

    Args:
        request (HttpRequest): The incoming HTTP request.

    Returns:
        HttpResponse: The rendered ``profiles/index.html`` page.
    """
    profiles_list = Profile.objects.all()
    context = {'profiles_list': profiles_list}
    return render(request, 'profiles/index.html', context)


def profile(request, username):
    """Display the profile of a single user.

    Args:
        request (HttpRequest): The incoming HTTP request.
        username (str): Username of the profile owner, taken from the URL.

    Returns:
        HttpResponse: The rendered ``profiles/profile.html`` page.

    Raises:
        Http404: If no profile matches username, so the user gets the custom
            404 page.
    """
    try:
        profile = Profile.objects.get(user__username=username)
    except Profile.DoesNotExist:
        logger.warning(f"Profile with username {username} not found.")
        raise Http404("Profile not found")

    context = {'profile': profile}
    return render(request, 'profiles/profile.html', context)

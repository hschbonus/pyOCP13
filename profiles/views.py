"""Views of the profiles app."""
from django.shortcuts import render
from .models import Profile


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
        Profile.DoesNotExist: If no profile matches username. The exception is
            not caught here, so the user gets a 500 error page.
    """
    profile = Profile.objects.get(user__username=username)
    context = {'profile': profile}
    return render(request, 'profiles/profile.html', context)

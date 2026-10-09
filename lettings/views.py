"""Views of the lettings app."""
from django.shortcuts import render
from .models import Letting


def index(request):
    """Display the list of all lettings.

    Args:
        request (HttpRequest): The incoming HTTP request.

    Returns:
        HttpResponse: The rendered ``lettings/index.html`` page.
    """
    lettings_list = Letting.objects.all()
    context = {'lettings_list': lettings_list}
    return render(request, 'lettings/index.html', context)


def letting(request, letting_id):
    """Display the title and address of a single letting.

    Args:
        request (HttpRequest): The incoming HTTP request.
        letting_id (int): Primary key of the letting, taken from the URL.

    Returns:
        HttpResponse: The rendered ``lettings/letting.html`` page.

    Raises:
        Letting.DoesNotExist: If no letting matches letting_id. The exception is
            not caught here, so the user gets a 500 error page.
    """
    letting = Letting.objects.get(id=letting_id)
    context = {
        'title': letting.title,
        'address': letting.address,
    }
    return render(request, 'lettings/letting.html', context)

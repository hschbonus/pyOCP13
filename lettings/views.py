"""Views of the lettings app."""
import logging

from django.http import Http404
from django.shortcuts import render
from .models import Letting


logger = logging.getLogger(__name__)


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
        Http404: If no letting matches letting_id, so the user gets the custom
            404 page.
    """
    try:
        letting = Letting.objects.get(id=letting_id)
    except Letting.DoesNotExist:
        logger.warning(f"Letting with id {letting_id} not found.")
        raise Http404("Letting not found")

    context = {
        'title': letting.title,
        'address': letting.address,
    }
    return render(request, 'lettings/letting.html', context)

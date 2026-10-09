"""Views of the oc_lettings_site project app."""
from django.shortcuts import render


def index(request):
    """Display the home page of the site.

    Args:
        request (HttpRequest): The incoming HTTP request.

    Returns:
        HttpResponse: The rendered ``index.html`` page.
    """
    return render(request, 'index.html')

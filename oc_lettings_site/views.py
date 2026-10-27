"""Views of the oc_lettings_site project app."""
from django.shortcuts import render
from django.http import HttpResponseNotFound, HttpResponseServerError
from django.template.loader import render_to_string
from django.http import HttpResponse


def index(request):
    """Display the home page of the site.

    Args:
        request (HttpRequest): The incoming HTTP request.

    Returns:
        HttpResponse: The rendered ``index.html`` page.
    """
    return render(request, 'index.html')


def error_404(request, exception=None):
    return HttpResponseNotFound(render_to_string('404.html'))


def error_500(request):
    return HttpResponseServerError(render_to_string('500.html'))


def crash(request):
    """View to simulate a server error for testing purposes."""
    if request.user.is_authenticated:
        raise Exception("Simulated server error for testing.")
    return HttpResponse()

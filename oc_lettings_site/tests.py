"""Tests of the oc_lettings_site project app."""
from django.urls import resolve, reverse
from pytest_django.asserts import assertContains, assertTemplateUsed

from oc_lettings_site import views


def test_index_url():
    """The home page is served at / by the index view."""
    path = reverse("index")
    assert path == "/"
    assert resolve(path).func == views.index


def test_index_view(client):
    """The home page is displayed with its title and links to both apps."""
    response = client.get(reverse("index"))

    assert response.status_code == 200
    assertTemplateUsed(response, "index.html")
    assertContains(response, "Welcome to Holiday Homes")
    assertContains(response, reverse("lettings:lettings_index"))
    assertContains(response, reverse("profiles:profiles_index"))


def test_unknown_url_displays_custom_404_page(client):
    """An unknown URL gives the custom 404 page with a 404 status."""
    response = client.get("/this-page-does-not-exist/")

    assert response.status_code == 404
    assertTemplateUsed(response, "404.html")
    assertContains(response, "404 - Page not found", status_code=404)

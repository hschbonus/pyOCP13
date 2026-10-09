"""Tests of the profiles app."""
import logging

import pytest
from django.contrib.auth.models import User
from django.urls import resolve, reverse
from pytest_django.asserts import assertContains, assertTemplateUsed

from profiles import views
from profiles.models import Profile


@pytest.fixture
def profile(db):
    """Create a user and its profile in the test database."""
    user = User.objects.create_user(
        username="HeadlinesGazer",
        first_name="Ada",
        last_name="Lovelace",
        email="ada@example.com",
        password="not-a-real-password",
    )
    return Profile.objects.create(user=user, favorite_city="Buenos Aires")


# Unit tests: model

def test_profile_str(profile):
    """The string representation of a profile is the username of its owner."""
    assert str(profile) == "HeadlinesGazer"


# Unit tests: URLs

def test_index_url():
    """The profiles index is served at /profiles/ by the index view."""
    path = reverse("profiles:profiles_index")
    assert path == "/profiles/"
    assert resolve(path).func == views.index


def test_profile_url():
    """A profile detail is served at /profiles/<username>/ by the profile view."""
    path = reverse("profiles:profile", kwargs={"username": "HeadlinesGazer"})
    assert path == "/profiles/HeadlinesGazer/"
    assert resolve(path).func == views.profile


# Integration tests: URL + view + database + template

@pytest.mark.django_db
def test_index_view_without_profiles(client):
    """The index page displays a message when there is no profile."""
    response = client.get(reverse("profiles:profiles_index"))

    assert response.status_code == 200
    assertTemplateUsed(response, "profiles/index.html")
    assertContains(response, "No profiles are available.")


def test_index_view_with_profile(client, profile):
    """The index page lists the username of each profile with a link to its detail."""
    response = client.get(reverse("profiles:profiles_index"))

    assert response.status_code == 200
    assertContains(response, "HeadlinesGazer")
    assertContains(response, "/profiles/HeadlinesGazer/")


def test_profile_view(client, profile):
    """The detail page displays the information of the user and the favorite city."""
    response = client.get(reverse("profiles:profile", kwargs={"username": "HeadlinesGazer"}))

    assert response.status_code == 200
    assertTemplateUsed(response, "profiles/profile.html")
    assertContains(response, "Ada")
    assertContains(response, "Lovelace")
    assertContains(response, "ada@example.com")
    assertContains(response, "Buenos Aires")


@pytest.mark.django_db
def test_profile_view_unknown_username_returns_404(client, caplog):
    """An unknown username gives the custom 404 page and logs a warning."""
    with caplog.at_level(logging.WARNING, logger="profiles.views"):
        response = client.get(reverse("profiles:profile", kwargs={"username": "nobody"}))

    assert response.status_code == 404
    assertTemplateUsed(response, "404.html")
    assert "Profile with username nobody not found." in caplog.text

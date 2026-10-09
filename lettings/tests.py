"""Tests of the lettings app."""
import pytest
from django.test import Client
from django.urls import resolve, reverse
from pytest_django.asserts import assertContains, assertTemplateUsed

from lettings import views
from lettings.models import Address, Letting


@pytest.fixture
def address(db):
    """Create an address in the test database."""
    return Address.objects.create(
        number=7217,
        street="Bedford Street",
        city="Brunswick",
        state="GA",
        zip_code=31525,
        country_iso_code="USA",
    )


@pytest.fixture
def letting(address):
    """Create a letting linked to the address fixture."""
    return Letting.objects.create(title="Joshua Tree Green Haus", address=address)


# Unit tests: models

def test_address_str(address):
    """The string representation of an address is its number and street."""
    assert str(address) == "7217 Bedford Street"


def test_address_verbose_name_plural():
    """The admin displays 'Addresses' and not 'Addresss'."""
    assert Address._meta.verbose_name_plural == "Addresses"


def test_letting_str(letting):
    """The string representation of a letting is its title."""
    assert str(letting) == "Joshua Tree Green Haus"


# Unit tests: URLs

def test_index_url():
    """The lettings index is served at /lettings/ by the index view."""
    path = reverse("lettings:lettings_index")
    assert path == "/lettings/"
    assert resolve(path).func == views.index


def test_letting_url():
    """A letting detail is served at /lettings/<id>/ by the letting view."""
    path = reverse("lettings:letting", kwargs={"letting_id": 1})
    assert path == "/lettings/1/"
    assert resolve(path).func == views.letting


# Integration tests: URL + view + database + template

@pytest.mark.django_db
def test_index_view_without_lettings(client):
    """The index page displays a message when there is no letting."""
    response = client.get(reverse("lettings:lettings_index"))

    assert response.status_code == 200
    assertTemplateUsed(response, "lettings/index.html")
    assertContains(response, "No lettings are available.")


def test_index_view_with_letting(client, letting):
    """The index page lists the title of each letting with a link to its detail."""
    response = client.get(reverse("lettings:lettings_index"))

    assert response.status_code == 200
    assertContains(response, "Joshua Tree Green Haus")
    assertContains(response, f"/lettings/{letting.id}/")


def test_letting_view(client, letting):
    """The detail page displays the title and the address of the letting."""
    response = client.get(reverse("lettings:letting", kwargs={"letting_id": letting.id}))

    assert response.status_code == 200
    assertTemplateUsed(response, "lettings/letting.html")
    assertContains(response, "Joshua Tree Green Haus")
    assertContains(response, "7217 Bedford Street")
    assertContains(response, "Brunswick, GA 31525")


@pytest.mark.django_db
def test_letting_view_unknown_id(client):
    """An unknown id currently raises Letting.DoesNotExist (500 page in production)."""
    with pytest.raises(Letting.DoesNotExist):
        client.get(reverse("lettings:letting", kwargs={"letting_id": 999}))


@pytest.mark.django_db
def test_letting_view_unknown_id_returns_500_page():
    """In production, an unknown id gives the custom 500 page with a 500 status."""
    client = Client(raise_request_exception=False)

    response = client.get(reverse("lettings:letting", kwargs={"letting_id": 999}))

    assert response.status_code == 500
    assert "500 - Server error" in response.content.decode()

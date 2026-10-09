"""Models of the lettings app."""
from django.db import models
from django.core.validators import MaxValueValidator, MinLengthValidator


class Address(models.Model):
    """Postal address of a letting."""

    number = models.PositiveIntegerField(validators=[MaxValueValidator(9999)])
    street = models.CharField(max_length=64)
    city = models.CharField(max_length=64)
    state = models.CharField(max_length=2, validators=[MinLengthValidator(2)])
    zip_code = models.PositiveIntegerField(validators=[MaxValueValidator(99999)])
    country_iso_code = models.CharField(max_length=3, validators=[MinLengthValidator(3)])

    def __str__(self):
        """Return a short text representation of the address.

        Returns:
            str: The street number followed by the street name.
        """
        return f'{self.number} {self.street}'

    class Meta:
        """Display names used in the admin."""

        verbose_name = "Address"
        verbose_name_plural = "Addresses"


class Letting(models.Model):
    """Property available for rent, linked to a single address."""

    title = models.CharField(max_length=256)
    address = models.OneToOneField(Address, on_delete=models.CASCADE)

    def __str__(self):
        """Return a short text representation of the letting.

        Returns:
            str: The title of the letting.
        """
        return self.title

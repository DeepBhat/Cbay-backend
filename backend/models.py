from django.db import models
from django.db.models.fields import BooleanField, CharField, DateField, DecimalField, EmailField, PositiveIntegerField, URLField
from django.db.models import ForeignKey
from django.core.exceptions import ValidationError
from django.core.validators import validate_email


class User(models.Model):
    # Validator functions
    def validate_edu_email(email: str):
        if email[-4:] != ".edu":
            raise ValidationError(f"${email} is not a .edu email.")

    def validate_classification(classification: str):
        if classification not in ('Freshman', 'Sophomore', 'Junior', 'Senior'):
            raise ValidationError(f"{classification} has to be one of (Freshman, Sophomore, Junior, Senior). Check spelling and capitalization.")

    # Fields
    email = EmailField(unique=True, null=False, validators=[validate_email, validate_edu_email])
    first_name = CharField(max_length=50, null=False)
    last_name = CharField(max_length=50, null=False)
    university = CharField(max_length=50, null=False)
    thumbs_up = PositiveIntegerField(default=0, null=False)
    thumbs_down = PositiveIntegerField(default=0, null=False)
    bio = CharField(max_length=5000, null=True)
    classification = CharField(max_length=50, null=True, validators = [validate_classification])

    # Helper functions
    def __str__(self) -> str:
        return f"{self.email}: {self.first_name} {self.last_name}"


class Listing(models.Model):   
    # Validator functions
    def validate_condition(condition: str):
        # TODO: Add the list of options for the condition of the item (new, like new, used, etc.)
        return 

    # Fields
    item_name = CharField(max_length=50, null=False)
    price = DecimalField(max_digits=6, decimal_places=2)
    negotiable = BooleanField(null=False)
    condition = CharField(max_length=50)
    description = CharField(max_length=5000, null=True)
    location = CharField(max_length=50)
    date_created = DateField()
    user = ForeignKey(User, on_delete=models.CASCADE)

    # Helpers
    def __str__(self) -> str:
        return f"{self.item_name} @ {self.price} by {self.user}"


class Category(models.Model):
    class Meta:
        verbose_name_plural = "categories"
    # validators
    def validate_category(name: str): 
        # TODO: Add the list of options for valid categories (apparel, school supplies, furniture, etc.)
        return

    # Fields
    category_name = CharField(max_length=50)
    listing = ForeignKey(Listing, on_delete=models.CASCADE)

    # Helpers
    def __str__(self) -> str:
        return f"{self.category_name} for Listing: {self.listing}"

class Image(models.Model):
    # Fields 
    image_url = URLField(unique=True)
    # models.CASCADE is not called on_delete because we want to preserve 
    # the image url. Images with listing=NULL can be deleted on the cloud
    # storage platform later, maybe with a periodic script.
    listing = ForeignKey(Listing, null=True, on_delete=models.SET_NULL)

    # Helpers
    def __str__(self) -> str:
        return f"Image located at {self.image_url} for Listing: {self.listing}"

    
from django.core.exceptions import NON_FIELD_ERRORS
import graphene
from graphene_django import DjangoObjectType

from .models import Listing, User


class UserType(DjangoObjectType):
    class Meta:
        model = User

class ListingType(DjangoObjectType):
    class Meta:
        model = Listing

class Query(graphene.ObjectType):
    # TODO: add the other two models and queries for other two models
    users = graphene.List(UserType)
    listings = graphene.List(ListingType)
    user = graphene.Field(UserType, id=graphene.Int())
    listing = graphene.Field(ListingType, id=graphene.Int())

    def resolve_users(self, info, **kwargs):
        return User.objects.all()

    def resolve_listings(self, info, **kwargs):
        return Listing.objects.all()

    def resolve_user(self, info, **kwargs):
        id = kwargs.get('id')

        if id is not None:
            return User.objects.get(pk=id)
        
        return None

    def resolve_listing(self, info, **kwargs):
        id = kwargs.get('id')

        if id is not None:
            return Listing.objects.get(id=id)

        return None

    
import graphene
from graphene_django import DjangoObjectType

from .models import Listing, User

## ========== QUERIES =================
# We specify the GraphQL Type for Graphene. But graphene_django
# can create types out of Django models so it handles that for us.
class UserType(DjangoObjectType):
    class Meta:
        model = User

class ListingType(DjangoObjectType):
    class Meta:
        model = Listing

# Class to resolve queries made to GraphQL. Queries
# are just the READ operations for all models. 
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

## =============== MUTATIONS =====================
# Class to define what fields can be changed with the API.
# For our use case, these fields are the same as the model
# because everything in our models can be changed.
class UserInput(graphene.InputObjectType):
    id = graphene.ID()
    email = graphene.String()
    first_name = graphene.String()   
    last_name = graphene.String()
    university = graphene.String()
    thumbs_up = graphene.Int()
    thumbs_down = graphene.Int()
    bio = graphene.String()
    classification = graphene.String()

class ListingInput(graphene.InputObjectType):
    # TODO: fill the fields for this model
    pass


# USER mutations
class CreateUser(graphene.Mutation):
    # Pass in the input class created above to specify
    # that all the fields of the class are required arguments
    class Arguments:
        input = UserInput(required=True)
    
    # ok will be true if the mutation is successful
    ok = graphene.Boolean()
    # create a user field to accept UserType
    user = graphene.Field(UserType)

    @staticmethod
    def mutate(root, info, input=None):
        ok = True
        user_instance = User(
            email = input.email,
            first_name = input.first_name,
            last_name = input.last_name,
            university = input.university,
            thumbs_up = input.thumbs_up,
            thumbs_down = input.thumbs_down,
            bio = input.bio,
            classification = input.classification
        )

        user_instance.save()
        return CreateUser(ok=ok, user=user_instance)

class UpdateUser(graphene.Mutation):
    # TODO: add the update user mutation
    pass


# Listing mutations
# TODO: create listing mutations similar to user mutations


class Mutation(graphene.ObjectType):
    create_user = CreateUser.Field()
    # update_user = UpdateUser.Field()
    # create_listing = CreateListing.Field()
    # update_listing = UpdateListing.Field()


# Creating the schema
schema = graphene.Schema(query=Query, mutation=Mutation)
